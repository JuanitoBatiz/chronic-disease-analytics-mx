import json
from flask import Flask, render_template, send_file, jsonify
import os, glob, io, tempfile
import pandas as pd
import plotly.express as px
from flask import send_file, request
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.utils import ImageReader
 

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/explorar")
def explorar():
    return render_template("explorar.html")

@app.route("/api/enfermedad/<nombre>")
def datos_enfermedad(nombre):
    enfermedad = nombre.lower()
    base = "datos"

    respuesta = {
        "enfermedad": enfermedad.capitalize(),
        "graficas": {
            "defunciones": [],
            "egresos": [],
            "afecciones": []
        },
        "datos": {
            "defunciones": 0,
            "egresos": 0,
            "edad_promedio": 0,
            "sexo": {}
        }
    }

    # Cargar descripciones 
    try:
        with open("static/descripcion_graficas.json", encoding="utf-8") as f:
            descripciones = json.load(f)
    except:
        descripciones = {}

    # Buscar gráficas en graficas/explorar/{enfermedad}/{tipo}
    for tipo in ["defunciones", "egresos", "afecciones"]:
        ruta = f"static/graficas/explorar/{enfermedad}/{tipo}"
        if os.path.exists(ruta):
            for archivo in sorted(os.listdir(ruta)):
                if archivo.endswith(".html"):
                    respuesta["graficas"][tipo].append({
                        "archivo": archivo,
                        "ruta": f"/static/graficas/explorar/{enfermedad}/{tipo}/{archivo}",
                        "descripcion": descripciones.get(enfermedad, {}).get(archivo, "")
                    })

    # Leer datos
    rutas = {
        "defunciones": f"{base}/defunciones/{enfermedad}",
        "egresos": f"{base}/egresos/{enfermedad}"
    }

    # DEFUNCIONES
    if os.path.exists(rutas["defunciones"]):
        archivos = glob.glob(f"{rutas['defunciones']}/*.csv")
        if archivos:
            df = pd.concat([pd.read_csv(f) for f in archivos], ignore_index=True)
            if "edad_anios" in df.columns:
                respuesta["datos"]["edad_promedio"] = round(df["edad_anios"].mean(), 1)
            if "sexo" in df.columns:
                sexo = df["sexo"].map({1: "Hombre", 2: "Mujer"}).value_counts(normalize=True) * 100
                respuesta["datos"]["sexo"] = {k: round(v, 1) for k, v in sexo.items()}
            respuesta["datos"]["defunciones"] = len(df)

    # EGRESOS
    if os.path.exists(rutas["egresos"]):
        archivos = glob.glob(f"{rutas['egresos']}/*.csv")
        if archivos:
            df = pd.concat([pd.read_csv(f) for f in archivos], ignore_index=True)
            if "SEXO" in df.columns:
                sexo = df["SEXO"].map({1: "Hombre", 2: "Mujer"}).value_counts(normalize=True) * 100
                for k, v in sexo.items():
                    if k in respuesta["datos"]["sexo"]:
                        respuesta["datos"]["sexo"][k] = round(respuesta["datos"]["sexo"][k] + v, 1)
                    else:
                        respuesta["datos"]["sexo"][k] = round(v, 1)
            if "EDAD" in df.columns:
                edad_total = respuesta["datos"]["edad_promedio"]
                edad_nueva = round(df["EDAD"].mean(), 1)
                if edad_total == 0:
                    respuesta["datos"]["edad_promedio"] = edad_nueva
                else:
                    respuesta["datos"]["edad_promedio"] = round((edad_total + edad_nueva) / 2, 1)
            respuesta["datos"]["egresos"] = len(df)

    return jsonify(respuesta)

@app.route("/visualizar")
def visualizar():
    return render_template("visualizar.html")

@app.route("/api/mapas")
def obtener_descripciones_mapas():
    try:
        with open("static/descripcion_mapas.json", encoding="utf-8") as f:
            data = json.load(f)
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/comparar")
def comparar():
    return render_template("comparar.html")

@app.route("/api/comparar/<enfermedad>/<anio1>/<anio2>")
def comparar_anios(enfermedad, anio1, anio2):
    anio1, anio2 = int(anio1), int(anio2)

    if enfermedad == "diabetes":
        generar_graficas_automaticamente("diabetes", anio1, anio2)
    elif enfermedad == "cancer":
        generar_graficas_automaticamente_cancer(anio1, anio2)

    base_path = f"/static/graficas/comparar/{enfermedad}/{anio1}_{anio2}"
    try:
        with open("static/descripcion_comparacion.json", encoding="utf-8") as f:
            descripciones = json.load(f)
    except:
        descripciones = {}

    graficas = []
    for nombre in ["evolucion_casos", "cambios_mortalidad", "variacion_grupo_edad"]:
        ruta = f"{base_path}/{nombre}.html"
        graficas.append({
            "ruta": ruta,
            "descripcion": descripciones.get(nombre, "")
        })

    explicacion = descripciones.get("explicacion", "Comparación entre los años seleccionados.")
    return jsonify({"graficas": graficas, "explicacion": explicacion})

@app.route("/descargar/<enfermedad>/<int:anio1>/<int:anio2>")
def descargar_csv(enfermedad, anio1, anio2):
    base_path = "datos"
    sufijos = {
        "afecciones": "AFECDIABETES" if enfermedad == "diabetes" else "AFECCANCER",
        "egresos": "EGRESDIABETES" if enfermedad == "diabetes" else "EGRESCANCER",
        "defunciones": "DEFUNDIABETES" if enfermedad == "diabetes" else "DEFUNCANCER"
    }

    dfs = []
    for tipo, prefijo in sufijos.items():
        for anio in [anio1, anio2]:
            ruta = f"{base_path}/{tipo}/{enfermedad}/{prefijo}{anio}.csv"
            if os.path.exists(ruta):
                df = pd.read_csv(ruta)
                df["tipo"] = tipo
                df["año"] = anio
                dfs.append(df)

    if dfs:
        df_final = pd.concat(dfs, ignore_index=True)
        ruta_salida = f"temp_reporte_{enfermedad}_{anio1}_{anio2}.csv"
        df_final.to_csv(ruta_salida, index=False)
        return send_file(ruta_salida, as_attachment=True)
    else:
        return "No se encontraron datos para los años seleccionados.", 404
    
def generar_graficas_automaticamente(enfermedad, anio1, anio2):
    base_path = "datos"
    sufijos = {
        "afecciones": "AFECCIONESDIABETES",
        "egresos": "EGRESOSDIABETES",
        "defunciones": "DEFUNCIONESDIABETES"
    }

    carpeta = f"static/graficas/comparar/{enfermedad}/{anio1}_{anio2}"
    os.makedirs(carpeta, exist_ok=True)

    rango = list(range(anio1, anio2 + 1))

    archivos = {
        tipo: {
            anio: f"{base_path}/{tipo}/{enfermedad}/{sufijos[tipo]}{anio}.csv"
            for anio in rango
        }
        for tipo in ["afecciones", "egresos", "defunciones"]
    }

    resumen = []
    for tipo, por_anio in archivos.items():
        temp = []
        for anio, ruta in por_anio.items():
            if os.path.exists(ruta):
                df = pd.read_csv(ruta)
                df["Año"] = anio
                temp.append(df)
        if temp:
            df_tipo = pd.concat(temp)
            conteo = df_tipo.groupby("Año").size().reset_index(name="Cantidad")
            for _, row in conteo.iterrows():
                resumen.append({
                    "Año": int(row["Año"]),
                    "Tipo": tipo.capitalize(),
                    "Cantidad": int(row["Cantidad"])
                })

    df_resumen = pd.DataFrame(resumen)

    
    # Gráfica 1: Evolución de casos

    fig1 = px.line(
        df_resumen,
        x="Año", y="Cantidad", color="Tipo", markers=True,
        title=f"Evolución de casos por {enfermedad.capitalize()}",
        labels={"Cantidad": "Número de casos"},
    )
    fig1.update_traces(mode="lines+markers")
    fig1.write_html(f"{carpeta}/evolucion_casos.html")

    # Gráfica 2: Cambios en mortalidad
    def_df = df_resumen[df_resumen["Tipo"] == "Defunciones"]
    fig2 = px.bar(
        def_df,
        x="Año", y="Cantidad", color="Tipo",
        title=f"Cambios en mortalidad por {enfermedad.capitalize()}",
        text="Cantidad"
    )
    fig2.update_traces(textposition="outside")
    fig2.write_html(f"{carpeta}/cambios_mortalidad.html")

    # Gráfica 3: Variación por grupo de edad
    path1 = archivos["defunciones"][anio1]
    path2 = archivos["defunciones"][anio2]
    if os.path.exists(path1) and os.path.exists(path2):
        df1 = pd.read_csv(path1)
        df1["Año"] = anio1
        df2 = pd.read_csv(path2)
        df2["Año"] = anio2
        df_total = pd.concat([df1, df2])
        columna_edad = "edad" if "edad" in df_total.columns else "EDAD" if "EDAD" in df_total.columns else None
        if columna_edad:
            fig3 = px.box(
                df_total,
                x="Año", y=columna_edad, points="all",
                title=f"Distribución de edad de defunciones por {enfermedad.capitalize()}",
                labels={columna_edad: "Edad al fallecer"}
            )
            fig3.write_html(f"{carpeta}/variacion_grupo_edad.html")


def generar_graficas_automaticamente_cancer(anio1, anio2):
    base_path = "datos"
    enfermedad = "cancer"
    sufijos = {
        "afecciones": "AFECCANCER",
        "egresos": "EGRESCANCER",
        "defunciones": "DEFUNCANCER"
    }

    carpeta = f"static/graficas/comparar/{enfermedad}/{anio1}_{anio2}"
    os.makedirs(carpeta, exist_ok=True)

    
    rango = list(range(anio1, anio2 + 1))

    archivos = {
        tipo: {
            anio: f"{base_path}/{tipo}/{enfermedad}/{sufijos[tipo]}{anio}.csv"
            for anio in rango
        }
        for tipo in ["afecciones", "egresos", "defunciones"]
    }

    resumen = []
    for tipo, por_anio in archivos.items():
        temp = []
        for anio, ruta in por_anio.items():
            if os.path.exists(ruta):
                df = pd.read_csv(ruta)
                df["Año"] = anio
                temp.append(df)
        if temp:
            df_tipo = pd.concat(temp)
            conteo = df_tipo.groupby("Año").size().reset_index(name="Cantidad")
            for _, row in conteo.iterrows():
                resumen.append({
                    "Año": int(row["Año"]),
                    "Tipo": tipo.capitalize(),
                    "Cantidad": int(row["Cantidad"])
                })
    
    df_resumen = pd.DataFrame(resumen)

    # Gráfica 1: Evolución de casos
    fig1 = px.line(
        df_resumen,
        x="Año", y="Cantidad", color="Tipo", markers=True,
        title="Evolución de casos por Cáncer",
        labels={"Cantidad": "Número de casos"},
    )
    fig1.update_traces(mode="lines+markers")
    fig1.write_html(f"{carpeta}/evolucion_casos.html")

    # Gráfica 2: Cambios en mortalidad
    def_df = df_resumen[df_resumen["Tipo"] == "Defunciones"]
    fig2 = px.bar(
        def_df,
        x="Año", y="Cantidad", color="Tipo",
        title="Cambios en mortalidad por Cáncer",
        text="Cantidad"
    )
    fig2.update_traces(textposition="outside")
    fig2.write_html(f"{carpeta}/cambios_mortalidad.html")

    # Gráfica 3: Variación por grupo de edad
    path1 = archivos["defunciones"][anio1]
    path2 = archivos["defunciones"][anio2]
    if os.path.exists(path1) and os.path.exists(path2):
        df1 = pd.read_csv(path1)
        df1["Año"] = anio1
        df2 = pd.read_csv(path2)
        df2["Año"] = anio2
        df_total = pd.concat([df1, df2])
        columna_edad = "edad" if "edad" in df_total.columns else "EDAD" if "EDAD" in df_total.columns else None
        if columna_edad:
            fig3 = px.box(
                df_total,
                x="Año", y=columna_edad, points="all",
                title="Distribución de edad de defunciones por Cáncer",
                labels={columna_edad: "Edad al fallecer"}
            )
            fig3.write_html(f"{carpeta}/variacion_grupo_edad.html")


@app.route("/reporte")
def vista_reporte():
    return render_template("reporte.html")


@app.route("/generar-reporte")
def descargar_reporte():
    # 1. Obtener parámetros
    enfermedad = request.args.get("enfermedad", "diabetes").lower()
    anio_inicio = int(request.args.get("inicio", 2013))
    anio_fin = int(request.args.get("fin", 2023))
    entidad = request.args.get("entidad", "").strip()

    # 2. Cargar y unir archivos CSV
    ruta = f"datos/defunciones/{enfermedad}/*.csv"
    archivos = sorted(glob.glob(ruta))
    
    if not archivos:
        return f"No se encontraron archivos en {ruta}", 400

    try:
        dfs = []
        for archivo in archivos:
            anio = int(os.path.basename(archivo).strip().split(".")[0][-4:])
            df_temp = pd.read_csv(archivo)
            df_temp["AÑO"] = anio
            dfs.append(df_temp)
        df = pd.concat(dfs, ignore_index=True)
    except Exception as e:
        return f"Error leyendo los archivos CSV: {e}", 500

    if "AÑO" not in df.columns:
        return "No se encontró la columna AÑO.", 400
    
    # 3. Filtrar por año y entidad (si aplica)
    df = df[(df["AÑO"] >= anio_inicio) & (df["AÑO"] <= anio_fin)]
    if entidad and "ENTIDAD" in df.columns:
        df = df[df["ENTIDAD"].str.upper() == entidad.upper()]

    if df.empty:
        return "No hay datos disponibles para los filtros seleccionados.", 400

    # 4. Agrupar y graficar
    conteo = df.groupby("AÑO").size().reset_index(name="Total")
    fig = px.line(conteo, x="AÑO", y="Total", title=f"Defunciones por {enfermedad.capitalize()}")
    
    tmp_img = tempfile.NamedTemporaryFile(suffix=".png", delete=False)
    fig.write_image(tmp_img.name)

    # 5. Crear PDF
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    c.setFont("Helvetica-Bold", 14)
    c.drawString(50, 750, "📄 Reporte de Enfermedades Crónicas")
    c.setFont("Helvetica", 12)
    c.drawString(50, 730, f"Enfermedad: {enfermedad.capitalize()}")
    c.drawString(50, 715, f"Años: {anio_inicio} - {anio_fin}")
    c.drawString(50, 700, f"Entidad: {entidad if entidad else 'Nacional'}")
    c.drawString(50, 685, "Fuente: INEGI, SSA")

    # 6. Insertar gráfica
    c.drawImage(ImageReader(tmp_img.name), 50, 400, width=500, height=250)
    c.showPage()
    c.save()
    buffer.seek(0)

    # 7. Limpiar archivo temporal
    tmp_img.close()
    os.unlink(tmp_img.name)

    return send_file(
        buffer,
        as_attachment=True,
        download_name="reporte.pdf",
        mimetype="application/pdf"
    )


if __name__ == "__main__":
    app.run(debug=True)
