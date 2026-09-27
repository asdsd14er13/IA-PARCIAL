# Guía para redactar el paper del proyecto de calidad del aire

Esta guía sigue la estructura del formato del profesor y aterriza cada sección al notebook `PARCIAL IA SENAHMI.ipynb`. Está escrita como apoyo para un trabajo académico de estudiante. **No reemplaza los resultados reales ni las citas:** completa los campos entre corchetes después de revisar las salidas finales del cuaderno y de leer las fuentes que encuentres.

## Enfoque recomendado para que el trabajo sea coherente

El notebook tiene varios análisis, pero la investigación principal conviene que sea **regresión para estimar PM2.5 en una estación y hora determinadas**. Los clasificadores y K-Means son ejercicios complementarios, no el objetivo principal del paper.

La estimación usa estación, fecha/hora y mediciones de PM10 y NO₂ de esa misma hora. Por eso se debe describir como **estimación con variables de la misma hora**, no como pronóstico de contaminación futura ni como alerta sanitaria.

El archivo de modelo guarda el mejor modelo individual, Random Forest regresor. También se probaron combinaciones: si no superan al modelo individual, se debe informar ese resultado honestamente. Probar dos modelos que trabajan juntos no obliga a afirmar que la combinación mejoró.

Datos ya revisados en el proceso: fuente abierta de SENAMHI; CSV de aproximadamente 577,794 filas originales, siete estaciones y periodo hasta mayo de 2024; el conjunto utilizable para el objetivo PM2.5 con PM10 y NO₂ tuvo aproximadamente 209,102 filas antes de los muestreos del experimento. Se consolidaron 84 registros repetidos en 42 claves estación-hora. El experimento principal separó temporalmente datos anteriores a 2023 para entrenamiento y 2023 en adelante para prueba; utilizó muestras para reducir el tiempo de cálculo. Verifica estas cifras en las salidas finales del notebook antes de publicarlas, en especial si volviste a ejecutar o modificaste celdas.

En la evaluación guardada que se revisó, Random Forest obtuvo aproximadamente MAE=5.165, RMSE=8.144 y R²=0.499; el Voting de regresión lineal y Random Forest obtuvo MAE=5.505, RMSE=8.300 y R²=0.480. Estos números son resultados del experimento actual, no una garantía para otros periodos o datos. Comprueba que coincidan con la ejecución final que usarás en el informe.

## En qué secciones sí buscar y citar fuentes

No necesitas buscar artículos para las 29 secciones. Cita fuentes cuando expliques hechos externos, conceptos, métodos o compares tus resultados con estudios previos. En cambio, tus propios resultados se citan con tablas/figuras del notebook, no con artículos. **“Obligatoria”** aquí significa que debe haber respaldo para las afirmaciones externas; puede ser artículo científico, documento oficial o documentación técnica, según el caso.

| Sección del formato | ¿Buscar/citar? | Qué respaldar | Palabras de búsqueda recomendadas |
|---|---|---|---|
| **4. Introducción** | Sí, artículos y fuentes oficiales | Importancia de PM2.5, contexto de contaminación/monitoreo en Lima o Perú, trabajos de estimación con IA y el vacío que aborda tu comparación. | `PM2.5 Lima Metropolitana estudio calidad del aire`; `air quality Lima Peru particulate matter study`; `PM2.5 estimation machine learning review`; `machine learning air pollution Peru`; `WHO particulate matter PM2.5 health air quality guidelines`. |
| **5. Situación problemática** | Sí, principalmente fuentes oficiales y estudios locales | Que la situación existe: reportes/mediciones de SENAMHI, cobertura de estaciones, concentraciones o episodios documentados. Los conteos de tu CSV se respaldan con tus propias tablas y figuras. | `SENAMHI calidad del aire Lima informe PM2.5`; `site:datosabiertos.gob.pe monitoreo contaminantes aire Lima SENAMHI`; `Lima Metropolitana PM2.5 monitoring stations study`; `Peru air quality report particulate matter`. |
| **6. Identificación y formulación del problema** | Opcional, si presentas un árbol o método formal | La técnica que realmente uses (árbol de problemas, Ishikawa o 5 porqués) y afirmaciones sobre datos faltantes/medición ambiental. No hace falta citar tus propios conteos. | `problem tree analysis research methodology`; `Ishikawa fishbone problem analysis research`; `air quality monitoring missing data sensor stations`; `PM2.5 estimation missing measurements machine learning`. |
| **9. Justificación** | Sí, pocas fuentes | Por qué importa estudiar PM2.5, por qué es razonable comparar modelos y qué aporta el uso de datos abiertos. La justificación debe conectarse con la evidencia y literatura, no ser solo opinión. | `PM2.5 health effects scientific review`; `machine learning air quality estimation benefits limitations`; `open government data environmental research Peru`. |
| **10. Antecedentes y estado del arte** | Sí, es la sección que más artículos necesita | Usa principalmente estudios científicos sobre estimación/predicción de PM2.5. Para cada estudio registra datos, variables, validación, modelos, métricas, resultados y limitaciones. | `PM2.5 concentration estimation machine learning systematic review`; `hourly PM2.5 regression Random Forest air quality`; `PM2.5 prediction model comparison linear regression KNN decision tree random forest`; `air pollution ensemble learning PM2.5`; `temporal validation air quality machine learning`; `Lima Peru PM2.5 machine learning`. |
| **11. Marco conceptual** | Sí, fuentes científicas/fundacionales y documentación técnica | Definiciones de PM2.5/PM10/NO₂, regresión, baseline, Random Forest, Voting/stacking, MAE/RMSE/R², data leakage y generalización. Usa una fuente confiable por concepto o grupo relacionado; no hace falta citar cada oración repetidamente. | `WHO PM2.5 definition particulate matter`; `Random Forest regression Breiman 2001`; `VotingRegressor scikit-learn documentation`; `MAE RMSE R2 regression metrics reference`; `data leakage machine learning temporal data`; `regression model generalization air quality`. |
| **12. Metodología de investigación** | Sí, para justificar el enfoque/diseño | Referencia metodológica para investigación aplicada/cuanti­tativa y, solo si lo declaras, Design Science Research. | `applied quantitative research experimental design machine learning`; `Design Science Research Hevner 2004 artifact evaluation`; `research methodology comparative machine learning study`. |
| **13. Metodología de desarrollo de IA** | Sí | La fuente original o académica de CRISP-DM y, si se usa, Design Science. Describe lo que hiciste en el notebook y cita la metodología cuando la presentes. | `CRISP-DM methodology original paper Chapman 2000`; `CRISP-DM data mining process phases`; `Design Science Research information systems artifact evaluation`. |
| **14. Fase 1: comprensión del problema** | Opcional, si afirmas que aplicaste una técnica reconocida | Cita 5 Whys, SIPOC, BPMN, Ishikawa u otra técnica únicamente si de verdad la utilizaste. Si solo resumes el alcance del proyecto, no necesitas artículo. | `5 Whys root cause analysis methodology`; `SIPOC process mapping methodology`; `problem framing data science project`. |
| **15. Fase 2: comprensión de los datos** | Sí, fuente oficial obligatoria para describir el dataset | Página del conjunto de datos, metadatos y diccionario de SENAMHI: procedencia, periodo, variables, unidades, licencia/condiciones. Esas fuentes pueden ser documentación oficial, no necesariamente artículos científicos. | `site:datosabiertos.gob.pe "Monitoreo de los contaminantes del aire" Lima`; `SENAMHI diccionario de datos monitoreo contaminantes aire Lima`; `SENAMHI metadatos estaciones calidad del aire Lima`. |
| **16. Ingeniería y preparación de datos** | Sí para justificar conceptos/decisiones generales; no para tus conteos | Referencias sobre calidad de datos, datos faltantes, mediciones de sensores y características temporales/cíclicas. Los pasos exactos y cantidades se documentan con el notebook. | `environmental sensor data quality missing values air monitoring`; `air quality monitoring data preprocessing missing observations`; `cyclical encoding hour day machine learning`; `median aggregation repeated sensor measurements`; `scikit-learn preprocessing Pipeline data leakage`. |
| **17. Diseño de la solución** | Opcional, fuentes técnicas | Cita documentación técnica si describes Pipeline, codificación, persistencia con joblib o arquitectura de ML como conceptos. El diagrama que diseñes es elaboración propia. | `scikit-learn Pipeline preprocessing estimator documentation`; `joblib model persistence scikit-learn documentation`; `machine learning system architecture data pipeline`. |
| **18. Desarrollo e implementación** | Sí para los algoritmos y herramientas, de forma breve | Cita documentación original/oficial al describir modelos y librerías. No hace falta una referencia por cada línea de código. | `scikit-learn DummyRegressor documentation`; `LinearRegression KNeighborsRegressor DecisionTreeRegressor RandomForestRegressor documentation`; `VotingRegressor documentation scikit-learn`; `Jupyter notebook reproducible workflow`. |
| **19. Diseño experimental** | Sí para el diseño de validación cuando expliques por qué | Fuentes sobre división temporal, evaluación de modelos y prevención de fuga. Los parámetros concretos de tu ejecución son información propia que reportas en una tabla. | `time based train test split machine learning temporal validation`; `time series cross validation scikit-learn documentation`; `data leakage temporal train test split`; `ensemble model validation held out test set`. |
| **20. Evaluación** | Sí para definir/justificar métricas y explicabilidad | Fuente técnica o científica de MAE, RMSE, R² y, si reportas importancia por permutación, de esa técnica. Los valores medidos no requieren citas externas. | `MAE RMSE coefficient of determination regression metrics scikit-learn`; `permutation feature importance scikit-learn user guide`; `regression evaluation metrics air quality PM2.5`. |
| **21. Resultados** | Normalmente no para presentar tus métricas; sí si comparas con otros papers | La tabla y gráficos son evidencia propia. Si comparas directamente tus números con resultados publicados en esta sección, cita esos artículos; también puedes dejar esa comparación para Discusión. | Para comparación únicamente: `PM2.5 Random Forest regression MAE RMSE study`; `air quality model comparison PM2.5 temporal test`. |
| **22. Discusión** | Sí | Compara tus hallazgos con antecedentes; explica coincidencias/diferencias y limita las interpretaciones. Cita los estudios que uses para contrastar, no solo una búsqueda general. | `PM2.5 Random Forest regression feature importance study`; `air quality ensemble model error correlation PM2.5`; `machine learning PM2.5 model comparison temporal generalization`; `Lima Peru air pollution machine learning results`. |
| **23. Amenazas a la validez y limitaciones** | Opcional/recomendable | Cita marcos de validez de estudios empíricos si utilizas sus categorías; cita drift/generalización si haces afirmaciones metodológicas. Las limitaciones específicas (7 estaciones, periodo, muestreo) se derivan de tu propio dataset/experimento. | `validity threats empirical machine learning study internal external construct conclusion`; `temporal distribution shift machine learning environmental data`; `generalization limits air quality monitoring stations`. |
| **24. Consideraciones éticas** | Sí, fuentes oficiales para licencia y recomendaciones éticas si haces afirmaciones generales | Licencia/condiciones de datos abiertos del portal; atribución a SENAMHI. Como no son datos de personas, explica eso sin inventar un problema de privacidad. Cita guías éticas solo si discutes uso responsable de IA. | `datos abiertos Perú licencia atribución portal oficial`; `SENAMHI datos abiertos términos de uso`; `responsible AI environmental monitoring guidelines`. |
| **25. Reproducibilidad** | Opcional, principalmente documentación técnica | Para versiones, Pipeline y guardado/carga del joblib, usa documentación oficial de Python/scikit-learn/joblib. La semilla, rutas y pasos de ejecución son datos de tu propio proyecto. | `scikit-learn model persistence joblib official documentation`; `scikit-learn version reproducibility random_state`; `Jupyter reproducible research environment requirements`. |
| **27. Recomendaciones y trabajo futuro** | Opcional | Cita solo si propones una línea basada en literatura (por ejemplo, pronóstico con variables rezagadas, validación temporal repetida o nuevas estaciones). Las recomendaciones derivadas directamente de tus limitaciones pueden ser propias. | `PM2.5 forecasting lagged features machine learning`; `air quality temporal cross validation multiple years`; `transferability air pollution models monitoring stations`. |
| **28. Referencias** | Sí, reúne todo lo efectivamente citado | No es una fuente que debas citar a sí misma: aquí se listan con el estilo indicado todas las fuentes citadas en las secciones anteriores. Prioriza artículos revisados por pares, además de SENAMHI y documentación técnica pertinente. | Usa las búsquedas de las filas anteriores; en Google Scholar/Scopus agrega `review`, `systematic review`, `Lima`, `Peru` o el nombre del algoritmo para afinar. |

**Secciones que normalmente no necesitan artículos propios:** 1. Título; 2. Resumen (normalmente no lleva citas); 3. Palabras clave; 7. Pregunta; 8. Objetivos; matriz de trazabilidad; 26. Conclusiones; 29. Anexos. En 21. Resultados tampoco, salvo que compares explícitamente con otros estudios. En estas secciones usa la información y evidencia de tu proyecto, sin añadir afirmaciones externas sin cita.

**Cómo usar las búsquedas:** prueba primero las frases en Google Scholar; para contexto de Perú, busca además en SENAMHI y Datos Abiertos Perú. Abre y lee cada fuente antes de citarla. Registra autores, año, título, revista/congreso, DOI o URL y qué dato concreto usarás. No cites los resultados que solo aparecen en el resumen de búsqueda ni copies métricas de otro estudio como si fueran tuyas.

## 1. Título

**Qué escribir:** un título que nombre el problema, el método y el lugar/datos.

**Propuesta:** *Estimación de PM2.5 mediante modelos de aprendizaje automático con datos de monitoreo de calidad del aire de Lima Metropolitana, 2020–2024*.

Confirma el año inicial exacto en el CSV. No lo llames pronóstico futuro, porque las entradas incluyen PM10 y NO₂ de la misma hora.

## 2. Resumen / Abstract

**Qué escribir:** un único párrafo de 200–300 palabras que incluya contexto, problema, objetivo, origen y periodo de los datos, preparación, modelos comparados, separación temporal, métricas, resultado principal y conclusión. Escríbelo al final, cuando ya estén cerradas las cifras.

**Usa del proyecto:** datos abiertos de SENAMHI, PM2.5 como variable objetivo, siete estaciones (confirma), modelos de regresión, prueba temporal y MAE/RMSE/R². No pongas métricas provisionales ni digas que el modelo predice el futuro.

## 3. Palabras clave

**Qué escribir:** entre cuatro y ocho términos que también aparezcan en el resumen. Una propuesta: **calidad del aire; PM2.5; aprendizaje automático; regresión; Random Forest; Lima Metropolitana**.

## 4. Introducción

**Qué escribir:** presenta el monitoreo de calidad del aire; explica por qué interesa estimar PM2.5; cita evidencia oficial o científica; resume estudios anteriores; señala qué aspecto concreto no cubre tu trabajo; presenta la comparación de modelos y tu aporte estudiantil. Organízalo de lo general a lo específico y cita las afirmaciones sobre efectos en salud.

**Aporte posible, sin exagerar:** documentar y comparar modelos de regresión con datos abiertos de estaciones de Lima usando una evaluación temporal y dejar un pipeline reutilizable para nuevos registros con las mismas columnas.

**Palabras para buscar:** `PM2.5 salud OMS material particulado`, `calidad del aire Lima estaciones monitoreo estudio`, `machine learning PM2.5 estimation review`, `air pollution prediction random forest Peru`.

## 5. Situación problemática

**Qué escribir:** demuestra que la calidad del aire y el monitoreo de PM2.5 son un problema real con datos de SENAMHI, reportes oficiales y literatura. Describe qué cubre el archivo: fechas, estaciones, frecuencia y mediciones. Presenta un gráfico o tabla del notebook y di qué evidencia muestra. Evita asegurar que hay contaminación “alta” o daños locales si no tienes una fuente que lo demuestre.

**Evidencia que puedes usar:** cantidad de observaciones por estación/año, distribución de PM2.5 y registros faltantes. Aclara que la base describe lo medido por las estaciones incluidas, no necesariamente todos los distritos o toda la población de Lima.

**Palabras para buscar:** `SENAMHI calidad del aire Lima informe`, `datos abiertos monitoreo contaminantes aire Lima`, `PM2.5 Lima Metropolitana concentración estudio`.

## 6. Identificación y formulación del problema

**Qué escribir:** presenta un árbol de problemas sencillo. Problema central sugerido: *necesidad de estimar PM2.5 a partir de las variables disponibles en los registros horarios de las estaciones analizadas*. Causas a verificar con los datos: mediciones incompletas, cobertura limitada a estaciones/periodos, variabilidad temporal. Consecuencias posibles: dificultad para completar o analizar registros; no afirmes consecuencias operativas sin evidencia. Evidencia: conteo de faltantes, estaciones y distribución temporal. Necesidad: comparar modelos para saber si alguno ofrece estimaciones razonables.

## 7. Pregunta de investigación

**Propuesta:** *¿Qué desempeño presentan distintos modelos de regresión para estimar las concentraciones horarias de PM2.5 usando estación, variables temporales y mediciones de PM10 y NO₂ de la misma hora en los datos abiertos de monitoreo de Lima Metropolitana?*

Esta pregunta se responde comparando modelos con el mismo conjunto de prueba temporal y las mismas métricas.

## 8. Objetivo general

**Propuesta:** *Comparar modelos de aprendizaje automático para estimar PM2.5 en los registros de monitoreo de calidad del aire de Lima Metropolitana, utilizando datos abiertos de SENAMHI y una evaluación temporal, con el fin de identificar el modelo con menor error en el periodo de prueba.*

### Objetivos específicos

Puedes usar estos cuatro, ajustándolos a lo que realmente ejecutaste:

1. Describir la estructura, cobertura y calidad del conjunto de datos de SENAMHI.
2. Limpiar y preparar los registros para estimar PM2.5, documentando faltantes, duplicados y variables empleadas.
3. Entrenar y comparar los modelos de regresión incluidos en el notebook, junto con un baseline y las combinaciones probadas.
4. Evaluar los modelos en un periodo posterior al entrenamiento mediante MAE, RMSE y R², y guardar el pipeline seleccionado para reutilizarlo con datos compatibles.

Cada objetivo debe tener su propia evidencia en metodología/resultados y una conclusión relacionada.

### Matriz de trazabilidad (inclúyela dentro de objetivos o metodología)

Incluye una tabla que conecte problema, pregunta, objetivos, método, resultado y evidencia. Ejemplo de filas: descripción del dataset → OE1 → análisis descriptivo → perfil de datos → tabla de estaciones y faltantes; preparación → OE2 → limpieza → datos listos → conteos antes/después; comparación → OE3/OE4 → modelos y métricas → modelo con menor error → tabla y gráfico.

## 9. Justificación

Escribe cuatro párrafos cortos:

- **Práctica:** estudiar si los datos disponibles permiten estimar PM2.5 en los registros analizados.
- **Tecnológica:** la regresión permite modelar relaciones que pueden no ser lineales; se comprueba mediante comparación, no se presupone que IA sea mejor.
- **Científica/académica:** aporta una comparación reproducible sobre un dataset abierto local y sus limitaciones.
- **Metodológica:** documenta limpieza, separación temporal, baseline, métricas y guardado del pipeline.

No presentes el cuaderno como sistema oficial de vigilancia ni como herramienta clínica o de salud pública.

**Palabras para buscar:** `justificación investigación aplicada aprendizaje automático calidad del aire`, `open government data air quality machine learning`.

## 10. Antecedentes y estado del arte

Busca aproximadamente 5–8 trabajos científicos cercanos. Para cada uno resume: problema, ciudad/datos, periodo, variables, modelos, validación, métricas, resultado, limitación y relación con tu proyecto. Agrúpalos por temas (estimación de PM2.5, modelos de árboles/ensambles y evaluación temporal), no hagas una lista sin comparación. Prioriza artículos revisados por pares recientes y conserva también una fuente oficial de datos.

**Palabras para buscar en Google Scholar, Scopus o IEEE Xplore:** `PM2.5 concentration estimation machine learning review`; `air quality PM2.5 Random Forest regression hourly data`; `PM2.5 temporal validation machine learning`; `air pollution prediction ensemble learning`; `Lima air pollution PM2.5 study`; `Peru air quality monitoring machine learning`.

## 11. Marco conceptual

Define en lenguaje propio y cita fuentes: calidad del aire, PM2.5, PM10, NO₂, estación de monitoreo, aprendizaje supervisado, regresión, características y variable objetivo, entrenamiento/prueba, baseline, Random Forest regresor, Voting/ensamble, MAE, RMSE, R², sobreajuste, generalización, fuga de datos y joblib/pipeline. Explica que regresor predice un número; clasificador asigna una categoría; K-Means agrupa observaciones.

**Palabras para buscar:** `PM2.5 PM10 NO2 definición`, `Random Forest regression original paper`, `MAE RMSE coefficient of determination regression`, `data leakage time series machine learning`, `scikit-learn Pipeline model persistence joblib`.

## 12. Metodología de investigación

Describe el enfoque como **cuantitativo**, de tipo **aplicado**, con evaluación **experimental/comparativa** de modelos sobre datos históricos. Aclara la unidad de análisis (registro estación-hora después de consolidación) y que no hubo intervención sobre las estaciones ni recolección de personas. Si el curso requiere Design Science Research, justifica brevemente que se construyó y evaluó un artefacto de software: el pipeline de estimación.

**Palabras para buscar:** `investigación aplicada cuantitativa experimental modelos predictivos`, `Design Science Research Hevner AI artifact evaluation`.

## 13. Metodología de desarrollo de IA

Explica cómo el notebook sigue fases parecidas a CRISP-DM: comprender problema, entender datos, prepararlos, modelar, evaluar y guardar el pipeline. Relaciona cada fase con celdas/artefactos concretos. No digas que hubo despliegue en producción si solo guardaste un joblib y una función de ejemplo.

**Palabras para buscar:** `CRISP-DM phases data mining methodology`, `CRISP-DM machine learning project reproducibility`, `AI software engineering lifecycle`.

## 14. Fase 1: comprensión del problema

Documenta contexto, usuarios potenciales (estudiante/investigador que analiza los registros), necesidad, alcance, restricciones, requisitos y criterio de éxito. Requisito funcional: recibir estación, fecha/hora, PM10 y NO₂ y estimar PM2.5. Restricción: requiere columnas compatibles y no genera un pronóstico futuro. Criterio principal: menor RMSE en el test temporal, revisando también MAE y R² frente al baseline.

**Palabras para buscar:** `requirements machine learning system data science`, `problem framing air quality monitoring`.

## 15. Fase 2: comprensión de los datos

Presenta una ficha: fuente SENAMHI/datosabiertos.gob.pe; título oficial del recurso; formato CSV; periodo exacto que muestre el archivo; fecha de descarga (complétala si la tienes); filas originales; estaciones; columnas; unidad de análisis; variable objetivo PM2.5; variables predictoras; licencia/condiciones tal como figuran en el portal. Anexa el diccionario de datos y los metadatos del recurso. No infieras unidades si el diccionario no las confirma.

**Palabras para buscar:** `SENAMHI monitoreo contaminantes aire Lima metropolitana dataset`, `data card dataset documentation`, `open data government metadata Peru`.

## 16. Ingeniería y preparación de datos

Cuenta el orden real de las operaciones: lectura del CSV; normalización/conversión de fechas; conversión de contaminantes a números; retiro de fechas inválidas; duplicados idénticos; consolidación por estación-hora con mediana; selección de filas con PM2.5/PM10/NO₂ disponibles; creación de variables temporales/cíclicas; codificación/estandarización dentro del pipeline cuando corresponda. Incluye conteos antes y después y justifica cada decisión. Describe outliers con cautela; no digas que eliminaste valores extremos si el notebook no lo hizo.

**Palabras para buscar:** `data cleaning environmental monitoring data missing values`, `feature engineering cyclic hour day machine learning`, `median aggregation duplicate sensor readings`.

### 17.1 Calidad y análisis exploratorio

Incluye conteo de nulos por columna, duplicados, filas por estación/año, histogramas/boxplots de contaminantes, relaciones/correlaciones y comportamiento mensual de PM2.5. Debajo de cada figura escribe qué se observa y una interpretación prudente. Para valores faltantes, distingue entre falta de dato y valor cero.

**Palabras para buscar:** `exploratory data analysis air quality`, `air pollution monitoring data quality completeness validity`, `sensor data missingness environmental monitoring`.

### 17.2 Prevención de fuga de información

Explica que se utilizó una separación cronológica: entrenamiento con fechas previas a 2023 y prueba con 2023 en adelante, en lugar de mezclar aleatoriamente pasado y futuro. Indica cualquier muestra aleatoria tomada después de definir cada periodo y su semilla. Expón la limitación: como PM10 y NO₂ son mediciones de la misma hora que PM2.5, el modelo estima/construye una estimación para esa hora cuando esas mediciones están disponibles; no puede usarse como pronóstico previo de esa hora. Revisa que los transformadores se ajusten con entrenamiento mediante `Pipeline`.

**Palabras para buscar:** `temporal train test split time series leakage`, `data leakage machine learning preprocessing pipeline`, `time-aware validation environmental data`.

## 17. Diseño de la solución

Añade un diagrama simple: CSV SENAMHI → limpieza/consolidación → variables de estación/tiempo/contaminantes → pipeline de preprocesamiento + regresor → estimación de PM2.5 → métricas/guardado del modelo. Indica entradas, salida, librerías y dónde se guarda el artefacto. El joblib es un archivo serializado para cargar de nuevo el pipeline; no es una aplicación independiente.

**Palabras para buscar:** `machine learning pipeline architecture diagram`, `scikit-learn pipeline preprocessing estimator`, `joblib persistence sklearn model`.

### 18.1 Requisitos y software

Incluye pocos requisitos concretos: leer CSV, limpiar datos, entrenar modelos, comparar errores, guardar/cargar pipeline y predecir en filas con las columnas requeridas. Requisitos no funcionales: reproducible con versiones/semilla y ejecución local. Menciona Python, pandas, scikit-learn, matplotlib/seaborn y joblib solo si aparecen en el notebook.

**Palabras para buscar:** `software requirements data science notebook`, `reproducible machine learning environment requirements`.

## 18. Desarrollo e implementación

Describe brevemente el notebook y sus bloques: importaciones, configuración de rutas, lectura/diagnóstico, limpieza, visualizaciones, selección de variables, entrenamiento, comparación, análisis complementarios y guardado/carga del pipeline. Usa capturas solo si ayudan; el código completo puede ir en anexos o repositorio. Aclara que K-Means y clasificación son análisis complementarios y que la tarea principal es regresión.

**Palabras para buscar:** `Jupyter notebook reproducible data science workflow`, `scikit-learn regression pipeline`.

### 19.1 Modelos y baseline

Lista exactamente los comparados en la ejecución final: baseline de media, regresión lineal, KNN regresor, árbol de decisión, Random Forest y Voting de regresión lineal + Random Forest. Define en una frase cada uno. Si en la versión actual se añadieron blending/stacking, repórtalos como experimentos adicionales con sus resultados reales. Random Forest combina muchos árboles; Voting promedia predicciones de modelos distintos; el ensamble solo conviene si su error baja frente a sus componentes.

**Palabras para buscar:** `DummyRegressor mean baseline`, `linear regression`, `KNeighborsRegressor`, `DecisionTreeRegressor`, `RandomForestRegressor`, `VotingRegressor ensemble`, `stacking regressor`.

## 19. Diseño experimental

Presenta una tabla con experimento/modelo, variables, periodo de entrenamiento, periodo de prueba, tamaño de muestra, semilla, parámetros y métricas. Explica qué se mantuvo igual y qué cambió. Las comparaciones deben usar las mismas observaciones de prueba. Si se probó un peso del Voting o un stacking, explica que se seleccionó usando validación separada y reporta esa regla; no ajustes con el test final.

**Palabras para buscar:** `experimental design machine learning model comparison`, `time series holdout evaluation regression`, `ensemble validation leakage`.

## 20. Evaluación

Explica las métricas sin complicarlo: MAE es el error absoluto promedio (en unidades de PM2.5); RMSE penaliza más los errores grandes; R² compara con una referencia de variación y puede ser negativo. Justifica RMSE/MAE como métricas principales porque PM2.5 es numérico. Describe la prueba temporal y el baseline. La clasificación exploratoria usa precision/recall/F1/matriz de confusión si vas a mencionarla, pero no la mezcles con las métricas de regresión.

**Palabras para buscar:** `MAE RMSE R squared interpretation regression`, `temporal holdout model evaluation`, `permutation feature importance interpretation`.

## 21. Resultados

Reporta primero los números observados, sin explicar todavía causas: tabla completa de modelos con MAE/RMSE/R²; modelo con menor RMSE; gráfico de comparación; gráfico observado vs. estimado; tamaño real del train/test; y resultado del Voting/otras combinaciones. En el experimento previamente revisado, RF ≈ MAE 5.165, RMSE 8.144, R² 0.499; Voting LR+RF ≈ MAE 5.505, RMSE 8.300, R² 0.480. **Confirma/actualiza esas cifras después de la última ejecución.** Si una combinación empeoró, dilo: se probó la cooperación y no ganó. Reporta clustering/clasificación aparte como complementarios.

No necesitas citar artículos para presentar tus propias tablas y gráficos. Si comparas aquí tus métricas con las de publicaciones, cita esos estudios; las búsquedas para esa comparación están en la tabla de secciones que requieren referencias.

## 22. Discusión

Interpreta por qué el modelo ganador pudo representar mejor relaciones no lineales; compara con los artículos revisados usando condiciones comparables; explica que R²≈0.50 deja variación sin explicar; comenta variables importantes por permutación con cautela; analiza por qué Voting no mejoró (por ejemplo, errores parecidos o componente lineal menos preciso, solo si tus resultados lo respaldan). No interpretes importancia como causalidad ni generalices a todas las zonas del Perú.

**Palabras para buscar:** `PM2.5 machine learning model comparison discussion`, `random forest air pollution regression feature importance`, `ensemble error correlation regression`.

## 23. Amenazas a la validez y limitaciones

Menciona: solo siete estaciones del recurso (confirmar); periodo termina en mayo de 2024; faltantes y consolidación; muestreo computacional; una única división temporal; datos de entrada de la misma hora; posible cambio de estaciones/condiciones; métricas sensibles a distribución de prueba; resultado no generalizable automáticamente a otras ciudades o años. Separa validez interna (diseño/sampling), externa (otras estaciones/periodos), constructo (PM2.5 observado representa la variable que se desea estudiar) y conclusión (incertidumbre por una prueba limitada).

**Palabras para buscar:** `validity threats machine learning empirical study`, `generalization temporal drift air quality model`, `sensor coverage bias air quality`.

## 24. Consideraciones éticas

Indica que se trabajó con mediciones ambientales abiertas y no con datos personales, después de verificar los metadatos/licencia del portal. Reconoce autoría de SENAMHI y cita la fuente. Usa el modelo como ejercicio académico: no sustituye monitoreo oficial, recomendaciones médicas ni alertas ambientales. Explica que se debe evitar presentar una estimación como medición real.

**Palabras para buscar:** `responsible use open environmental data`, `Peru datos abiertos licencia atribución`, `responsible AI environmental monitoring`.

## 25. Reproducibilidad

Indica ruta/fuente de descarga y nombre del CSV, fecha de descarga si consta, versión del notebook, Python y versiones relevantes de librerías, semilla, columnas requeridas, regla temporal, pasos para ejecutar desde arriba y ruta del joblib. Para volver a usarlo se requiere el mismo esquema de entradas; datos futuros deben prepararse con las mismas reglas. No incluyas rutas locales de Windows como única forma de reproducir: da también instrucciones para cambiar la ruta a otra computadora.

**Palabras para buscar:** `machine learning reproducibility random seed software versions`, `Jupyter reproducible research data availability`, `model serialization pipeline joblib`.

## 26. Conclusiones

Escribe una conclusión por objetivo específico y usa únicamente resultados ya reportados. Resume qué se conoció del dataset, qué preparación se aplicó, qué modelo tuvo menor error y si las combinaciones ayudaron. Una conclusión posible, condicionada a confirmar métricas: *en la división temporal evaluada, Random Forest obtuvo menor RMSE que el Voting de regresión lineal y Random Forest; por tanto, no se justifica afirmar que esa combinación mejoró la estimación*. No introduzcas cifras o afirmaciones nuevas.

## 27. Recomendaciones y trabajo futuro

Propón acciones realizables: incorporar nuevos años/estaciones; repetir con validación temporal de varios cortes; probar otras variables disponibles; analizar por estación; comparar ensambles con validación sin tocar el test; revisar calidad/unidades con metadatos; desarrollar una interfaz educativa y evaluar su uso. Señala que cualquier predicción anticipada necesitaría variables disponibles antes de la hora objetivo, por ejemplo históricos rezagados y un diseño de pronóstico distinto.

**Palabras para buscar:** `future work PM2.5 prediction temporal validation`, `air quality forecasting lag features`, `transferability air pollution machine learning models`.

## 28. Referencias

Incluye citas dentro del texto y la lista final con el estilo solicitado por el profesor (si no indicó uno, pregunta o usa APA 7 de forma consistente). Necesitas al menos: (1) ficha/recurso oficial de SENAMHI/datos abiertos; (2) fuente oficial sobre PM2.5/salud, si haces afirmaciones sanitarias; (3) artículo de revisión de ML en calidad del aire; (4) estudios empíricos comparables de PM2.5; (5) fuentes metodológicas de CRISP-DM/Design Science si las invocas; (6) documentación oficial de scikit-learn para métricas/modelos, como referencia técnica secundaria. Comprueba título, autores, año, DOI/URL y que de verdad leíste la fuente. No cites un artículo solo porque aparece en una búsqueda.

**Búsquedas sugeridas:** `PM2.5 machine learning systematic review air quality`; `Random Forest PM2.5 regression monitoring stations`; `air pollution machine learning temporal validation`; `Lima air quality PM2.5 research`; `CRISP-DM original paper`; `Design Science Research Hevner 2004`; `site:datosabiertos.gob.pe monitoreo contaminantes aire Lima SENAMHI`.

## 29. Anexos

Incluye: ficha/diccionario del dataset; enlace o copia del notebook; tabla completa de métricas; parámetros y semillas; ficha del modelo/joblib; gráficos adicionales; árbol del problema/matriz de trazabilidad; instrucciones breves de ejecución. No pegues cientos de líneas de código en el cuerpo principal.

## Referencias y recursos que conviene localizar

- Portal oficial del recurso: [Monitoreo de los contaminantes del aire en Lima Metropolitana — SENAMHI, Datos Abiertos Perú](https://www.datosabiertos.gob.pe/dataset/monitoreo-de-los-contaminantes-del-aire-en-lima-metropolitana-servicio-nacional-de).
- Busca artículos científicos con las palabras clave indicadas en Google Scholar, Scopus, IEEE Xplore o ScienceDirect; filtra por artículos revisados por pares y años recientes, sin excluir trabajos fundacionales del método.
- Para metodología y conceptos técnicos, usa documentos originales o documentación oficial (por ejemplo, CRISP-DM, Design Science Research y scikit-learn); para contexto local, prioriza SENAMHI y fuentes oficiales peruanas.

## Lista de verificación antes de entregar

- [ ] El periodo exacto, unidades, nombres de columnas, cantidad final de filas y fecha de descarga se verificaron contra CSV/metadatos.
- [ ] Las métricas coinciden con la ejecución final del notebook y se informa el tamaño de las muestras evaluadas.
- [ ] Queda claro que la variable objetivo es PM2.5 y que la tarea principal es regresión.
- [ ] Se compara contra baseline y se explican los resultados de las combinaciones, incluso si no mejoraron.
- [ ] No se llama pronóstico futuro a una estimación que usa PM10/NO₂ de la misma hora.
- [ ] Cada figura tiene número, título, fuente y una interpretación breve.
- [ ] Todas las afirmaciones científicas tienen citas; cada referencia de la lista aparece citada en el texto.
- [ ] Las conclusiones responden a objetivos y no exageran lo que permite concluir un solo periodo de prueba.
