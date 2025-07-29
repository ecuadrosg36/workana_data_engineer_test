# 🧠 Workana Data Engineer - Technical Test

Este repositorio contiene la estructura base para resolver la prueba técnica de Data Engineer para Workana, utilizando PostgreSQL como base de datos.

## 📁 Estructura del Proyecto

- `dags/`: DAGs de Airflow para orquestación local
- `etl/`: Scripts ETL en Python
- `sql/`: Consultas SQL y scripts de creación
- `modeling/`: Esquema dimensional y scripts relacionados
- `data/`: Datos de entrada y salida
- `ci/`: Archivos de configuración para CI/CD
- `tests/`: Pruebas unitarias e integración
- `logs/` y `output/`: Salidas del sistema y resultados

## ⚙️ Requisitos

- Python 3.12
- SQLite
- Airflow (opcionalmente en Docker)
- Librerías: ver `requirements.txt`

## ▶️ Uso rápido

```bash
python3 -m venv .venv
source venv/bin/activate
pip install -r requirements.txt
```

## 🧪 Pruebas

```bash
pytest tests/
```

## 🚀 Orquestación

Airflow o alternativa compatible. Inicia los DAGs desde `airflow_dags/`.

## 📌 Notas

Este proyecto usa SQLite como base de datos por defecto.

# ✅ Plan de Acción: Ejercicio 1 - Orquestación local

## 🎯 Objetivo

Crear un workflow end-to-end local que procese `sample_transactions.csv`, lo transforme con Python y lo cargue a una base de datos local (SQLite o PostgreSQL), usando una herramienta de orquestación como Airflow.

---

## ✅ Checklist de pasos

### 🛠️ Preparación del entorno

- [X] Crear entorno virtual (`venv`, `conda`, etc.)

```
PS C:\Users\enman\Downloads\COLFONDOS> & C:/Users/enman/Downloads/COLFONDOS/.venv/Scripts/Activate.ps1
(.venv) PS C:\Users\enman\Downloads\COLFONDOS> & C:\Users\enman\Downloads\COLFONDOS\.venv\Scripts\Activate.ps1
(.venv) PS C:\Users\enman\Downloads\COLFONDOS> cd C:\Users\enman\Downloads\COLFONDOS\workana_data_engineer_project
```

- [X] Instalar dependencias: `apache-airflow`, `pandas`, `sqlalchemy`, `psycopg2` (si usas PostgreSQL)

```
(.venv) PS C:\Users\enman\Downloads\COLFONDOS\workana_data_engineer_project> pip install -r requirements.txt
```

- [X] Crear estructura de carpetas del proyecto
  - `airflow_dags/`
  - `etl/`
  - `tests/`
  - `scripts/`
  - `data/`

### 🔁 Descarga y lectura de datos

- [X] Crear script para descargar `sample_transactions.csv`➜ `scripts/download_csv.py`
- [X] Implementar sensor de espera de archivo (con tamaño mínimo)
  ➜ `etl/sensors.py`

### 🧹 Transformación de datos

- [X] Crear función de transformación con `pandas` (lectura por chunks opcional)
  ➜ `etl/transform.py`

## 📌 Control de versiones y push a rama remota

Durante el desarrollo de esta prueba técnica, utilicé **Git** como sistema de control de versiones y **GitHub** como repositorio remoto. Para mantener el historial de cambios limpio y reflejar el avance del proyecto, ejecuté los siguientes comandos manualmente desde el entorno local:

```bash
git init
git add .
git commit -m "Initial commit - Workana Data Engineer challenge (SQLite)"
git branch -M main
git remote add origin https://github.com/ecuadrosg36/workana-data-engineer-test.git
git push -u origin main
```

### 🗄️ Carga a base de datos

- [X] Configurar conexión a SQLite

![1753651696522](image/README/1753651696522.png)

- [X] Crear función para carga a DB
  ➜ `etl/load.py`

![1753658977385](image/README/1753658977385.png)

![1753659062275](image/README/1753659062275.png)

![1753659089795](image/README/1753659089795.png)

## 🧠 Por qué SQLite

Inicialmente se planeó usar PostgreSQL, pero se optó por SQLite como alternativa práctica. SQLite no requiere instalación, es compatible con SQLAlchemy y permite ejecutar el pipeline completo localmente.

El código está preparado para cambiar fácilmente a PostgreSQL si se desea.

### ⚙️ Orquestación con Airflow

- [X] Crear DAG con tareas:

  - Descargar archivo
  - Esperar archivo y tamaño
  - Transformar datos
  - Cargar a DB

## 🐳 Ejecución con Docker + Airflow (recomendado)

- [X] Esta configuración inicia Airflow (webserver + scheduler) y PostgreSQL como backend.

```
docker-compose up
```

  Esto realiza lo siguiente:

* Inicia PostgreSQL como base de datos de Airflow
* Inicializa Airflow
* Crea el usuario admin
* Expone la interfaz en: [http://localhost:8080](http://localhost:8080)

  **Credenciales de acceso:**
* Usuario: `admin`
* Contraseña: `admin`

---

## 🧠 Decisiones técnicas

* **SQLite** se utiliza como base de datos de carga por simplicidad y portabilidad.
* **Airflow en Docker** permite orquestación reproducible sin depender del sistema operativo.
* **Modularidad y pruebas** : el proyecto está dividido en componentes reutilizables (`scripts/`, `etl/`, `dags/`) con logging, validaciones y manejo de errores.

  ![1753663082080](image/README/1753663082080.png)

![1753663132046](image/README/1753663132046.png)

![1753663219056](image/README/1753663219056.png)

- [X] Agregar sensores y reintentos a las tareas
  ➜ `airflow_dags/etl_transactions_dag.py`

  ![1753666490954](image/README/1753666490954.png)

  ![1753718989694](image/README/1753718989694.png)

  ![1753719590824](image/README/1753719590824.png)

### 🧪 Testing

- [X] Escribir tests unitarios para transformación y carga➜ `tests/test_transform.py`➜ `tests/test_load.py`
- [X] Escribir test de integración para el DAG completo

  ![1753721641888](image/README/1753721641888.png)

### 📈 Logging y métricas

- [X] Registrar logs detallados por tarea
- [X] Medir tiempo de ejecución por paso
- [X] Registrar cantidad de registros procesados

![1753723944617](image/README/1753723944617.png)

### 📬 Validaciones y alertas

- [X] Validar si tabla destino está vacía
- [X] Generar alerta/log en caso de error

![1753723993609](image/README/1753723993609.png)

## 🚀 Extras

- [ ] Lectura eficiente con `pandas.read_csv(..., chunksize=...)`
- [ ] Soporte para `.csv.gz` con `compression='gzip'`
- [ ] Replicar el pipeline con Prefect o Dagster y comparar resultados

# ✅ Plan de Acción: Ejercicio 2 - SQL y análisis

## 🎯 Objetivo

Ejecutar consultas SQL sobre los datos ya cargados en la base de datos (desde el Ejercicio 1), para generar reportes, identificar errores, y proponer mejoras de rendimiento.

---

## ✅ Checklist de pasos

### 📄 1. Crear vista/tabla resumen por día y estado

- [X] Definir estructura: fecha, estado, cantidad de transacciones
- [X] Crear script SQL➜ `sql/view_summary_by_date_status.sql`
- [X] Ejecutar script y verificar contenido

  ![1753735003870](image/README/1753735003870.png)

  ![1753726040297](image/README/1753726040297.png)

  ![1753726094325](image/README/1753726094325.png)

### 🔍 2. Query para usuarios con >3 transacciones fallidas en últimos 7 días

- [X] Identificar campo `status` o equivalente para marcar transacción fallida
- [X] Escribir query con `GROUP BY user_id`, `HAVING COUNT > 3`, `WHERE fecha >= current_date - 7`
- [X] Guardar como
  ➜ `sql/query_frequent_failures.sql`

  ![1753735061263](image/README/1753735061263.png)

  ![1753726979327](image/README/1753726979327.png)

  ![1753735117333](image/README/1753735117333.png)

### 📈 3. Detección de anomalías (incrementos anómalos)

- [X] Crear query que compare conteo diario con el promedio de días anteriores
- [X] Definir umbral de alerta (ej: +100% sobre la media de los últimos 3 días)
- [X] Guardar como➜ `sql/query_detect_anomalies.sql`
- [X] Simular alerta/log si se detecta

  ![1753737058422](image/README/1753737058422.png)

![1753735749694](image/README/1753735749694.png)

![1753736991138](image/README/1753736991138.png)

![1753737583919](image/README/1753737583919.png)

![1753737767035](image/README/1753737767035.png)

![1753737837298](image/README/1753737837298.png)

### 🧱 4. Índices y triggers

- [X] Crear índices sobre columnas claves (ej: `user_id`, `status`, `timestamp`)➜ `sql/create_indexes.sql`
- [X] Diseñar triggers para:
  - [X] Detectar valores fuera de rango (ej: fecha futura)
  - [X] Detectar intentos de inserción duplicada
    ➜ `sql/create_triggers.sql`
    ![1753735724226](image/README/1753735724226.png)

    ![1753735806273](image/README/1753735806273.png)

    ![1753735871487](image/README/1753735871487.png)

    ![1753737292890](image/README/1753737292890.png)

### 📂 5. Particionamiento lógico

- [X] Documentar propuesta de particionado (ej: por mes usando `timestamp`)
- [X] Simularlo si DB lo permite (ej: `CREATE TABLE datos_2025_07` + `UNION ALL`)
- [X] Explicar ventajas esperadas en rendimiento

![1753738157029](image/README/1753738157029.png)

![1753738408434](image/README/1753738408434.png)

![1753738427024](image/README/1753738427024.png)

![1753738497420](image/README/1753738497420.png)

![1753739014804](image/README/1753739014804.png)

![1753739034947](image/README/1753739034947.png)

![1753739060873](image/README/1753739060873.png)

* **Estrategia:** partición lógica por `mes` usando `strftime('%Y_%m', ts)`.
* **Implementación:** tablas físicas por mes + vista `all_transactions`.
* **Ventajas:** filtros por rango de fechas más rápidos, archivado y borrado por mes sencillo, aislamiento físico.
* **Limitación en SQLite:** no soporta particionamiento nativo ni triggers dinámicos → se gestiona desde el ETL.

---

## 📝 Extras (si hay tiempo)

- [ ] Automatizar queries en script Python con SQLAlchemy o `psycopg2`
- [ ] Graficar resultados con `matplotlib` o `plotly` (opcional)
- [ ] Simular monitoreo con logs diarios

# ✅ Plan de Acción: Ejercicio 3 - ETL Python para archivo grande

## 🎯 Objetivo

Procesar un archivo `sample.log.gz` (~5 millones de líneas en formato JSONL) en modo streaming, filtrando errores y generando métricas agregadas por hora y endpoint.

---

## ✅ Checklist de pasos

### 📦 1. Preparar entorno y archivo

- [X] Descomprimir o validar lectura directa del archivo `.gz`
- [X] Validar estructura JSONL: una línea = un JSON
- [X] Crear carpeta para scripts ETL
  ➜ `etl/large_log_etl.py`

  ![1753754900593](image/README/1753754900593.png)

### 🧾 2. Leer archivo por streaming

- [X] Implementar lectura línea a línea desde `.gz`➜ Usar `gzip.open()` + `json.loads()`
- [X] Filtrar solo líneas con `status_code >= 500`
- [X] Manejar errores de parseo JSON con try/except

  ![1753756480339](image/README/1753756480339.png)

### 🧹 3. Limpiar y parsear campos

- [X] Validar y limpiar campos clave (`timestamp`, `endpoint`, `status_code`)
- [X] Convertir timestamp a datetime y redondear por hora

### 📊 4. Agregaciones por hora y endpoint

- [X] Agrupar por `(hora, endpoint)` y calcular:
  - [X] Total requests
  - [X] Total con errores
  - [X] Porcentaje de error
- [X] Guardar en estructura tipo `pandas.DataFrame`

### 💾 5. Exportar resultados

- [X] Exportar resultados a archivo Parquet comprimido (`Snappy`)➜ `output/errors_summary.parquet`
- [X] Usar exportación por chunks si el DataFrame es muy grande
  ![1753756796981](image/README/1753756796981.png)

### ⚙️ 6. Performance y escalabilidad

- [X] Implementar versión alternativa con `multiprocessing`
- [X] Probar versiones con `polars` y/o `dask`
- [X] Medir tiempos de ejecución y uso de memoria (profiling)

  ![1753796367296](image/README/1753796367296.png)

  ![1753796441384](image/README/1753796441384.png)

  ![1753796522486](image/README/1753796522486.png)

  ![1753796582364](image/README/1753796582364.png)

  ![1753797404018](image/README/1753797404018.png)

  ![1753798442652](image/README/1753798442652.png)

  ![1753798462361](image/README/1753798462361.png)

### 🐛 7. Logging y manejo de errores

- [X] Configurar `logging` para registrar:
  - [X] Errores de parseo
  - [X] Métricas por batch
  - [X] Tiempos de proceso
- [X] Guardar logs en archivo (`logs/etl_run.log`)

![1753760384920](image/README/1753760384920.png)

![1753797518494](image/README/1753797518494.png)

---

## 🧪 Extras (si hay tiempo)

- [ ] Escribir pruebas unitarias para funciones clave (parsing, filtrado, agregación)
- [ ] Graficar las métricas por hora con `matplotlib` o `seaborn`
- [ ] Integrar este ETL como parte del DAG general

# ✅ Plan de Acción: Ejercicio 4 - Modelado de Datos

## 🎯 Objetivo

Diseñar un modelo dimensional (estrella o copo de nieve) para representar las transacciones del archivo CSV, poblar las tablas desde los datos crudos, e implementar buenas prácticas de modelado analítico.

---

## ✅ Checklist de pasos

### 🧱 1. Diseño del modelo dimensional

- [X] Identificar campos para la **tabla de hechos**: transacciones (ej: `monto`, `fecha`, `estado`, `user_id`)
- [X] Identificar posibles **dimensiones**:

  - Dimensión tiempo (fecha/hora)
  - Dimensión usuario
  - Dimensión estado de transacción
- [X] Elegir entre modelo **estrella (star)** o **copo de nieve (snowflake)** y justificar decisión
- [X] Diagramar el modelo (opcional con [dbdiagram.io](https://dbdiagram.io) o similar)

Para el modelado de datos, se identificaron los campos principales que constituyen los hechos de negocio. En este caso, la **tabla de hechos** corresponde a las transacciones realizadas en la plataforma. Los campos seleccionados fueron:

* `order_id`: identificador único de la transacción.
* `user_id`: referencia al usuario que realizó la transacción.
* `amount`: monto de la transacción.
* `ts` (timestamp): fecha y hora de la transacción.
* `status`: estado final de la transacción (ejemplo: completed, failed, pending).

Estos campos permiten analizar el comportamiento de las transacciones y vincular cada hecho con sus dimensiones relevantes.

Se identificaron las siguientes **dimensiones** clave para enriquecer el análisis y facilitar las consultas analíticas:

* **Dimensión tiempo** : permite analizar transacciones por año, mes, día o cualquier agrupamiento temporal relevante.
* **Dimensión usuario** : facilita segmentar, agrupar y analizar el comportamiento de cada usuario a lo largo del tiempo.
* **Dimensión estado de transacción** : ayuda a monitorear y comparar el porcentaje de transacciones exitosas, fallidas o pendientes, y detectar patrones o problemas recurrentes.

Estas dimensiones se modelan en tablas separadas y se relacionan con la tabla de hechos a través de claves foráneas, siguiendo las mejores prácticas de modelado dimensional.

Para este ejercicio se optó por un  **modelo estrella (star schema)** , debido a las siguientes razones:

* El modelo estrella simplifica la estructura del esquema, al conectar directamente la tabla de hechos con las dimensiones mediante claves foráneas.
* Facilita la consulta y el análisis de datos, ya que las uniones (joins) son directas y más rápidas, lo que mejora el rendimiento para la mayoría de queries analíticos.
* Dado que las dimensiones identificadas (usuario, tiempo y estado) no presentan jerarquías complejas ni requieren normalización adicional, el modelo estrella resulta más eficiente y sencillo de mantener.
* El modelo estrella es ampliamente recomendado para soluciones analíticas y de BI en escenarios donde la simplicidad y la velocidad de consulta son prioritarias.

  ![1753748426901](image/README/1753748426901.png)

### 🗄️ 2. Creación de las tablas

- [X] Crear script SQL para tablas:

  - `fact_transacciones`
  - `dim_user`
  - `dim_date`
  - `dim_status`
- [X] Usar claves primarias en dimensiones y claves foráneas en la tabla de hechos
  ➜ `sql/model_tables_star.sql`

![1753747619372](https://file+.vscode-resource.vscode-cdn.net/c%3A/Users/enman/Downloads/COLFONDOS/workana_data_engineer_project/image/README/1753747619372.png)

### 🚀 3. Carga inicial desde CSV

- [X] Escribir script Python para poblar dimensiones y hechos desde `sample_transactions.csv`➜ `etl/load_star_model.py`
- [X] Asegurar inserción sin duplicados en dimensiones
- [X] Resolver dependencias entre tablas (poblar primero dimensiones)

  ![1753753589461](image/README/1753753589461.png)

  ![1753748736908](image/README/1753748736908.png)

  ![1753748757454](image/README/1753748757454.png)

  ![1753748801239](image/README/1753748801239.png)

  ![1753748841569](image/README/1753748841569.png)

  ![1753748868524](image/README/1753748868524.png)

### 🌀 4. Estrategia SCD (Slowly Changing Dimensions)

- [X] Elegir e implementar SCD Tipo 1 o Tipo 2 en al menos una dimensión (ej: `dim_user`)
- [X] Documentar cómo se maneja el historial y actualizaciones
- [X] Incluir campos `scd_version`, `scd_start_ts`, `scd_end_ts` si es SCD Tipo 2

<details>
<summary><strong>Detalle de la Estrategia SCD en la dimensión usuario</strong></summary>

- Se implementó **SCD Tipo 2** en la tabla `dim_user` para mantener el historial de cambios relevantes en los datos de usuario.
- Cuando un usuario presenta un cambio en datos relevantes, se cierra la versión vigente (actualizando el campo `valid_to` con la fecha/hora del cambio y marcando `is_current = 0`).
- Se inserta un nuevo registro con la nueva información, la versión incrementada, `valid_from` (fecha/hora del cambio), `valid_to = NULL` y `is_current = 1`, indicando que es la versión vigente.
- Los campos utilizados para el control de versiones son:
  - `scd_version` (o `version`)
  - `scd_start_ts`: fecha/hora desde la que el registro es válido
  - `scd_end_ts`: fecha/hora hasta la que el registro fue válido (NULL si es vigente)
  - `is_current`: indica si el registro es la versión activa (1) o histórica (0)
- Las operaciones se realizan mediante el script Python `etl/update_user_scd.py`, lo que garantiza la trazabilidad de todos los cambios históricos para cada usuario.

</details>

**Justificación:**
Se optó por SCD Tipo 2 porque permite mantener un registro histórico completo de los cambios en la dimensión usuario. Esto es esencial para auditorías, análisis de tendencias y cumplimiento de requisitos regulatorios, ya que posibilita conocer el estado de la información de cada usuario en cualquier momento pasado.

![1753749180237](image/README/1753749180237.png)

![1753749137254](image/README/1753749137254.png)

![1753749302336](image/README/1753749302336.png)

![1753749329897](image/README/1753749329897.png)

![1753749734085](image/README/1753749734085.png)

![1753749843895](image/README/1753749843895.png)

![1753749890570](image/README/1753749890570.png)

![1753749922264](image/README/1753749922264.png)

### 📦 5. Particionamiento lógico y archivado

- [X] Simular partición lógica de la tabla de hechos por mes (`YYYYMM`)
- [X] Documentar ventajas para el rendimiento (lectura selectiva, limpieza, mantenimiento)
- [X] Simular archivado (ej: mover datos viejos a otra tabla o archivo externo)

![1753751493511](image/README/1753751493511.png)

**Detalle de la estrategia de particionamiento y archivado**

#### Decisiones de rendimiento

- **Índices:** Se crearon índices sobre la columna `period` en las tablas `fact_transactions` y `archive_transactions`, optimizando las consultas por rango temporal.
- **Particionamiento lógico:** En vez de crear múltiples tablas, se agregó una columna `period` (`YYYYMM`) para simular el particionamiento por mes. Esto permite filtrar, consultar y mantener grandes volúmenes de datos de forma eficiente.
- **Archiving:** Se movieron los registros antiguos (`period` < 202505) a la tabla `archive_transactions`, manteniendo la tabla principal densa y optimizada para operaciones recientes.
- **Densidad:** La tabla de hechos se mantiene compacta y relevante al transferir datos antiguos a un archivo o tabla de respaldo, mejorando el rendimiento general de las consultas analíticas.

![1753751554413](image/README/1753751554413.png)

![1753751576167](image/README/1753751576167.png)

### ⚙️ 6. Performance y optimización

- [X] Crear índices sobre claves foráneas y campos de filtro frecuentes (`fecha`, `estado`)
- [X] Documentar decisiones de optimización (densidad de claves, índices, orden de carga)
- [X] Validar que las relaciones estén bien formadas

#### Decisiones de optimización y performance

- **Índices:** Se crearon índices sobre las columnas usadas como claves foráneas (`user_id`, `status`, `date_id`) y sobre el campo de partición lógica (`period`). Esto mejora notablemente la velocidad de joins y filtros en consultas frecuentes.
- **Densidad de claves:** Se aseguraron valores no nulos y únicos para las claves primarias y foráneas, lo que incrementa la eficiencia y coherencia de los datos.
- **Orden de carga:** Primero se cargan las dimensiones (usuarios, estados, fechas) y luego los hechos (`fact_transactions`), garantizando que todas las referencias existan y las relaciones estén correctamente formadas.
- **Compactación (archivado):** Los datos antiguos se mueven a una tabla de archivo para mantener la tabla principal liviana, acelerando análisis sobre datos recientes.

  ![1753752456170](image/README/1753752456170.png)

  ![1753752550889](image/README/1753752550889.png)

  ![1753752617795](image/README/1753752617795.png)

![1753753795184](image/README/1753753795184.png)

![1753753810873](image/README/1753753810873.png)

![1753753827560](image/README/1753753827560.png)

![1753753706920](image/README/1753753706920.png)

---

## 🧪 Extras (si hay tiempo)

- [ ] Probar queries analíticas sobre la tabla de hechos (ej: KPIs por usuario/mes)
- [ ] Automatizar carga con Airflow
- [ ] Exportar modelo como `.erdiagram`, `.pdf` o imagen

# ✅ Plan de Acción: Ejercicio 5 - Git + CI/CD

## 🎯 Objetivo

Organizar todo el proyecto en un repositorio Git con estructura clara y reproducible, incluyendo automatización de pruebas, chequeos de calidad, y (opcionalmente) contenedores y orquestación local.

---

## ✅ Checklist de pasos

### 📁 1. Estructura modular del repositorio

- [X] Crear las siguientes carpetas base:

  - `airflow/` → DAGs y configuración de Airflow (aqui es llamado `dags/` se podria modificar pero tomaria un tiempo)
  - `etl/` → scripts ETL generales
  - `sql/` → scripts SQL y creación de modelo
  - `modeling/` → documentación del modelo dimensional
  - `data/` → archivos de entrada, comprimidos y resultados
  - `ci/` → archivos de configuración para CI
  - `tests/` → pruebas unitarias e integración
  - `logs/` y `output/` → salidas de ejecución
- [X] Agregar archivos `README.md` y `.gitignore` general, no se agrego por carpeta por no verlo necesario

  ![1753755107331](image/README/1753755107331.png)

  ![1753795972970](image/README/1753795972970.png)

### 🌿 2. Estrategia de branches

- [X] Definir ramas principales:
  - `main` → rama estable y productiva
  - `dev` → rama de integración y pruebas
  - `feature/<nombre>` → desarrollo de nuevas funciones (ej: `feature/etl-error-logs`)
- [X] Configurar protecciones para `main` y `dev` (opcional en GitHub/GitLab)

* main (producción)
  |
  |----------- dev (integración)
  |
  |------ feature/etl-error-logs
  |------ feature/test-coverage
  |------ feature/update-docs

  ![1753796056460](image/README/1753796056460.png)

  ![1753796213700](image/README/1753796213700.png)

  ![1753796276407](image/README/1753796276407.png)

### 🔄 3. Automatización con CI (GitHub Actions o GitLab CI)

- [X] Crear workflow de CI/CD en `.github/workflows/ci.yml` o `.gitlab-ci.yml`
- [X] Incluir en el pipeline:

  - [X] Linter (`flake8`, `black`, `isort`)
  - [X] Tests (`pytest`)
  - [X] Chequeos estáticos (`mypy`, `bandit`)
  - [X] Validación de DAGs (si se usa Airflow)
  - [X] Reporte de cobertura (opcional con `coverage`)

    ![1753796961587](image/README/1753796961587.png)

    ![1753796985636](image/README/1753796985636.png)

  El proyecto cuenta con pipeline CI/CD en GitHub Actions, que verifica automáticamente:

  - Linter de código (flake8, black, isort)
  - Tests automáticos (pytest)
  - Chequeos estáticos (mypy, bandit)
  - Reporte de cobertura
  - Validación de sintaxis de DAGs Airflow

  Ver el archivo `.github/workflows/ci.yml` para detalles.

  ![1753797208573](image/README/1753797208573.png)

  ```
  # Ordena imports automáticamente y remueve los no usados
  autoflake --in-place --remove-unused-variables --remove-all-unused-imports -r etl/
  autoflake --in-place --remove-unused-variables --remove-all-unused-imports -r etl/utils/

  # Ordena y agrupa imports
  isort etl/
  isort etl/utils/

  # Formatea el código 
  black etl/
  black etl/utils/
  ```

![1753797738825](image/README/1753797738825.png)

![1753797784709](image/README/1753797784709.png)


### 🐳 4. Docker y ejecución reproducible (opcional)

- [ ] Crear `Dockerfile` para ejecutar ETL o DAGs localmente
- [ ] Crear `docker-compose.yml` si hay múltiples servicios (Airflow + DB)
- [ ] Documentar cómo correr el entorno en README
- [ ] Incluir rollback (ej: scripts para revertir carga) y reporting si es posible

---

## 🗂️ Enlaces por hacer / dependencias

- [ ] [ ] Conectar CI al repositorio en GitHub/GitLab
- [ ] [ ] Crear archivos de configuración: `.pre-commit-config.yaml`, `pyproject.toml`
- [ ] [ ] Agregar al README: instrucciones para contribuir, correr tests, y ejecutar CI

---

## 📜 Entregables mínimos

- [X] README claro con estructura del proyecto y pasos para ejecución
- [X] Logs y evidencia de ejecución en `logs/` o adjuntos
- [X] Scripts y notebooks versionados
- [X] Pipeline CI funcionando o documentado

---

## 🧪 Extras (si hay tiempo)

- [ ] Integración con Notebooks o documentación automatizada (ej: MkDocs)
- [ ] Reportes visuales o dashboards con métricas
- [ ] Pipeline para publicar imagen Docker o paquete Python
- [ ]
- [ ]
