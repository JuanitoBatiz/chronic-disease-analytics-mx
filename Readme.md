# Aplicacion de Ciencia de Datos para la Deteccion y Analisis de Patrones de Diabetes y Cancer en Mexico (2013–2023)

## Descripción del Proyecto

Este proyecto aplica técnicas de **Ciencia de Datos** para analizar relaciones y patrones dentro del área de **salud**, enfocándose principalmente en dos enfermedades de alta incidencia en México: **diabetes** y **cáncer**.

Se utilizaron bases de datos abiertas proporcionadas por la [Dirección General de Información en Salud (DGIS)](http://www.dgis.salud.gob.mx/contenidos/basesdedatos/Datos_Abiertos_gobmx.html), abarcando el periodo de **2013 a 2023**.

El flujo de trabajo siguió las etapas clásicas de la ciencia de datos:

- **ETL (Extract, Transform, Load)**: selección, limpieza y transformación de los datos.
- **Análisis Exploratorio de Datos (EDA)**: identificación de comportamientos, valores atípicos, distribuciones, correlaciones y tendencias.

Para este análisis se usaron herramientas y bibliotecas como:
- `Python`
- `Pandas`
- `NumPy`
- `Plotly`
- Ejecutado principalmente en `Jupyter Notebook`.

Como producto final, se desarrolló un **prototipo web interactivo** que permite visualizar de forma clara y accesible los hallazgos más relevantes. Este sistema fue construido con:

- `HTML`
- `CSS`
- `Bootstrap`

El objetivo del prototipo es facilitar el acceso a información clave sobre el comportamiento de estas enfermedades a lo largo del tiempo, ayudando a **investigadores**, **profesionales de la salud** y **tomadores de decisiones** a consultar estos datos fácilmente.

Este trabajo fue desarrollado en colaboración con un equipo de **tres integrantes**, logrando identificar **patrones geográficos, demográficos, clínicos, entre otros.** que pueden apoyar estrategias más efectivas de **prevención**, **detección** y **control** de enfermedades en México.

Los resultados obtenidos sientan las bases para futuros estudios o políticas públicas fundamentadas en evidencia.


## Tabla de Contenidos

- [Descripción del Proyecto](#descripción-del-proyecto)
- [Características](#características)
- [Uso](#uso)
  - [I. Introducción](#i-introducción)
  - [II. Acceso a la página web](#ii-acceso-a-la-página-web)
  - [III. Estructura de la página web](#iii-estructura-de-la-página-web)
    - [3.1. Menú de navegación principal](#31-menú-de-navegación-principal)
    - [3.2. Secciones](#32-secciones)
      - [3.2.1. Explorar por enfermedad](#321-explorar-por-enfermedad)
      - [3.2.2. Distribución geográfica](#322-distribución-geográfica)
      - [3.2.3. Comparar datos por años](#323-comparar-datos-por-años)
      - [3.2.4. Descargar reporte PDF](#324-descargar-reporte-pdf)
- [Tecnologías utilizadas](#tecnologías-utilizadas)
- [Contribuciones](#contribuciones)
- [Licencia](#licencia)
- [Créditos](#créditos)
- [Contacto](#contacto)
- [Roadmap / Funcionalidades futuras](#roadmap--funcionalidades-futuras)


## Características

- Analiza datos de salud enfocados en diabetes y cáncer en México.
- Extrae, transforma y carga datos desde fuentes abiertas (ETL completo).
- Realiza análisis exploratorio de datos (EDA) para encontrar patrones relevantes.
- Genera visualizaciones interactivas de alta calidad (gráficas, mapas, tendencias).
- Permite consultar estadísticas por año, entidad federativa y variables demográficas.
- Presenta hallazgos mediante un prototipo web de fácil navegación.
- Facilita el uso del análisis para investigadores, médicos o tomadores de decisiones.
- Soporta la interpretación de datos con visualizaciones dinámicas y filtrables.
- Implementado en Python (Jupyter Notebook) con librerías como Pandas, NumPy y Plotly.
- Interfaz web desarrollada con HTML, CSS y Bootstrap.


## Uso

### I. Introducción

Este prototipo web interactivo permite visualizar de forma clara y accesible los hallazgos más relevantes del análisis. Facilita el acceso a información clave sobre el comportamiento de enfermedades crónicas como cáncer y diabetes a lo largo del tiempo, permitiendo que investigadores, profesionales de la salud y tomadores de decisiones consulten los datos de manera sencilla.

Los resultados abren la puerta a un análisis más profundo por parte de especialistas en salud, quienes podrán aprovechar esta base para generar nuevos enfoques de estudio y políticas públicas basadas en evidencia.

---

### II. Acceso a la página web

Para acceder a la página web, se proporcionará un código QR que lleva directamente al sitio, o bien una URL que se puede ingresar manualmente en cualquier navegador moderno (Google Chrome, Edge, Firefox, etc.).

Es necesario contar con una conexión estable a internet para el correcto funcionamiento del prototipo.

---

### III. Estructura de la página web

#### 3.1. Menú de navegación principal

El menú principal cuenta con cuatro secciones, desde donde se pueden visualizar gráficas y dashboards relacionados con las enfermedades crónicas (cáncer y diabetes).

#### 3.2. Secciones

##### 3.2.1. Explorar por enfermedad

Esta sección contiene dos subsecciones: **Cáncer** y **Diabetes**. Cada una muestra datos generales como egresos hospitalarios, edad promedio, defunciones y distribución por sexo.

Al desplazarse hacia abajo, se presentan gráficas interactivas con datos estadísticos relevantes y breves descripciones. Para explorar la información, basta con hacer clic en las gráficas para visualizar los datos correspondientes.

##### 3.2.2. Distribución geográfica

Aquí se visualiza el comportamiento de las enfermedades en diferentes regiones de México a través de mapas interactivos, acompañados de descripciones breves.

##### 3.2.3. Comparar datos por años

Esta sección permite comparar datos entre años seleccionados. Primero se elige la enfermedad (por ejemplo, cáncer) y luego se seleccionan los años a analizar. Posteriormente, se muestran gráficos comparativos de los años elegidos.

##### 3.2.4. Descargar reporte PDF

En esta sección es posible generar y descargar un reporte en formato PDF para una enfermedad específica. 

Para hacerlo, se debe:

1. Seleccionar la enfermedad (cáncer o diabetes).
2. Elegir el año de inicio y el año de fin.
3. Pulsar el botón “Descargar PDF”.

Esto iniciará la descarga de un archivo PDF que contiene una gráfica correspondiente al rango de años seleccionado.


## Tecnologías utilizadas

### Lenguaje y entorno
- **Python 3.10** – Lenguaje principal del proyecto.
- **Jupyter Notebook** – Plataforma para análisis interactivo y documentación.
- **Flask 3.0.3** – Framework ligero para desplegar el prototipo web.

### Bibliotecas de análisis y visualización
- **Pandas 2.3.1** – Manipulación y análisis de datos tabulares.
- **NumPy 2.3.1** – Operaciones numéricas avanzadas.
- **Plotly 6.2.0** – Visualizaciones interactivas de datos.

### Generación de reportes
- **ReportLab 4.1.0** – Creación de reportes en PDF.

### Desarrollo web
- **HTML5, CSS3, Bootstrap 5** – Estructura y estilo del prototipo web.

### Control de versiones y colaboración
- **Git** y **GitHub** – Para gestión del código fuente y trabajo colaborativo.


## Contribuciones

Este proyecto fue desarrollado como parte de una iniciativa académica colaborativa.  
Actualmente no se aceptan contribuciones externas.

Sin embargo, si deseas compartir sugerencias, correcciones o ideas para futuras mejoras, puedes contactarnos a través de los correos proporcionados en la sección [Contacto](#Contacto).


## Licencia

Este repositorio es solo para consulta y uso informativo.  
No se permite la copia, modificación, distribución ni uso comercial sin autorización previa por escrito de los autores.


## Créditos

Este proyecto ha sido posible gracias al apoyo y colaboración de diversas instituciones y personas. Agradecemos especialmente a:

- **Secretaría de Salud / Dirección General de Información en Salud (DGIS)**  
  Se utilizaron bases de datos abiertas proporcionadas por esta institución.  
  **Fuente: SS/DGIS, SINAIS. Fecha de actualización: 2023.**

- **Programa Delfín**  
  Programa Interinstitucional para el Fortalecimiento de la Investigación y el Posgrado del Pacífico, por brindar el espacio académico y de colaboración para el desarrollo del presente proyecto.

- **Instituto Politécnico Nacional (IPN)**  
  Por su compromiso con la formación científica y tecnológica de calidad.

- **Unidad Profesional Interdisciplinaria en Ingeniería y Tecnologías Avanzadas (UPIITA)**  
  Por proporcionar las condiciones técnicas y académicas necesarias para el trabajo de investigación.

- **Asesor académico:** Dr. Miguel Félix Mata Rivera

- **Estudiantes participantes:**
  - Estudiante: Curiel García Juan Jesus
  - Estudiante: Miranda Rodríguez Ana Sofía
  - Estudiante: Vargas Montero Ulises


 ## Contacto

- **Asesor:** Dr. Miguel Felix Mata Rivera
  **Contacto:** migfel@gmail.com

- **Estudiante:** Curiel García Juan Jesús 
  **Contacto:** curielgarciajuanjesus@gmail.com

- **Estudiante:** Miranda Rodriguez Ana Sofía  
  **Contacto:** miranda.rodriguez.anasofia.19@gmail.com

- **Estudiante:** Vargas Montero Ulises
  **Contacto:** uvm88gato@gmail.com


 ## Roadmap / Funcionalidades futuras

Este proyecto tiene un gran potencial de crecimiento y aplicación en el campo de la salud. A continuación se listan las líneas de trabajo propuestas para futuras fases:

- **Colaboración multidisciplinaria**  
  Integrar a estudiantes y profesionales del área médica para aportar una visión clínica que permita desarrollar herramientas más alineadas con las necesidades reales del personal de salud.

- **Diseño de herramientas de apoyo clínico**  
  Desarrollar funcionalidades que ayuden a realizar diagnósticos más oportunos, apoyar estrategias de prevención y fortalecer la toma de decisiones en instituciones de salud.

- **Aplicación de modelos de machine learning**  
  Implementar modelos predictivos que permitan identificar tendencias emergentes, poblaciones en riesgo y factores comunes entre enfermedades como cáncer y diabetes.

- **Fortalecimiento de la base de datos**  
  Ampliar el volumen y diversidad de los datos, incluyendo:
  - Registros más actuales y más antiguos
  - Nuevas variables relacionadas con determinantes sociales, económicos, ambientales y de acceso a servicios médicos

- **Transformación del análisis descriptivo en predictivo**  
  Evolucionar de un enfoque exploratorio hacia un enfoque analítico y predictivo con control de errores y métricas de precisión.

- **Ampliación del sistema web**  
  Añadir nuevas secciones al prototipo web para que permita consultar modelos predictivos, indicadores sociales o mapas interactivos.

---

Estas líneas estratégicas buscan transformar este estudio preliminar en una herramienta útil para la investigación aplicada y la intervención efectiva en el sistema de salud mexicano.


