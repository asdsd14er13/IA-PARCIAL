import json, base64, re, tempfile
from pathlib import Path
from docx import Document
from docx.shared import Inches, Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_CELL_VERTICAL_ALIGNMENT
from docx.oxml import OxmlElement
from docx.oxml.ns import qn

ROOT=Path(r'C:\Users\Robert Herrera\escritorio\Desktop\IA PARCIAL')
NB=json.loads((ROOT/'PARCIAL IA SENAHMI.ipynb').read_text(encoding='utf-8'))
ASSET=Path(tempfile.mkdtemp(prefix='senamhi-paper-'))

def extract(cell,n,name):
    images=[]
    for o in NB['cells'][cell].get('outputs',[]):
        d=o.get('data',{}).get('image/png')
        if d: images.append(''.join(d) if isinstance(d,list) else d)
    p=ASSET/name; p.write_bytes(base64.b64decode(images[n])); return p
quality=extract(7,0,'quality.png')
station=extract(13,0,'station.png')
models=extract(19,0,'models.png')
importance=extract(31,0,'importance.png')

doc=Document(); sec=doc.sections[0]
sec.top_margin=sec.bottom_margin=sec.left_margin=sec.right_margin=Inches(1)
sec.header_distance=sec.footer_distance=Inches(.5)
styles=doc.styles
for sn in ['Normal','Title','Heading 1','Heading 2','Heading 3']:
    s=styles[sn]; s.font.name='Times New Roman'; s._element.rPr.rFonts.set(qn('w:ascii'),'Times New Roman'); s._element.rPr.rFonts.set(qn('w:hAnsi'),'Times New Roman')
styles['Normal'].font.size=Pt(12); styles['Normal'].paragraph_format.line_spacing=2; styles['Normal'].paragraph_format.space_after=Pt(0); styles['Normal'].paragraph_format.first_line_indent=Inches(.5)
for sn in ['Title','Heading 1','Heading 2','Heading 3']:
    styles[sn].font.size=Pt(12); styles[sn].font.color.rgb=None; styles[sn].paragraph_format.keep_with_next=True; styles[sn].paragraph_format.space_before=Pt(10); styles[sn].paragraph_format.space_after=Pt(0); styles[sn].paragraph_format.line_spacing=2
styles['Title'].font.bold=True; styles['Title'].paragraph_format.alignment=WD_ALIGN_PARAGRAPH.CENTER
styles['Heading 1'].font.bold=True; styles['Heading 1'].paragraph_format.alignment=WD_ALIGN_PARAGRAPH.CENTER
styles['Heading 2'].font.bold=True; styles['Heading 2'].paragraph_format.alignment=WD_ALIGN_PARAGRAPH.LEFT
h=sec.header.paragraphs[0]; h.alignment=WD_ALIGN_PARAGRAPH.RIGHT
fld=OxmlElement('w:fldSimple'); fld.set(qn('w:instr'),'PAGE'); h._p.append(fld)

def font(run,size=12,bold=None,italic=None):
    run.font.name='Times New Roman'; run.font.size=Pt(size); run._element.get_or_add_rPr().rFonts.set(qn('w:ascii'),'Times New Roman'); run._element.get_or_add_rPr().rFonts.set(qn('w:hAnsi'),'Times New Roman')
    if bold is not None: run.bold=bold
    if italic is not None: run.italic=italic
    return run
def p(text='',indent=True,align=None,size=12,bold=False,italic=False):
    x=doc.add_paragraph(); x.paragraph_format.first_line_indent=Inches(.5) if indent else Inches(0); x.paragraph_format.line_spacing=2; x.paragraph_format.space_after=Pt(0)
    if align is not None: x.alignment=align
    if text: font(x.add_run(text),size,bold,italic)
    return x
def head(text,level=1):
    x=doc.add_paragraph(text,style=f'Heading {level}')
    for r in x.runs: font(r,12,bold=True)
    return x
def bullet(text):
    x=doc.add_paragraph(style='List Bullet'); x.paragraph_format.left_indent=Inches(.5); x.paragraph_format.first_line_indent=Inches(-.25); x.paragraph_format.line_spacing=2; x.paragraph_format.space_after=Pt(0); font(x.add_run(text)); return x
def caption(n,title,kind='Figura'):
    x=doc.add_paragraph(); x.paragraph_format.first_line_indent=Inches(0); x.paragraph_format.line_spacing=1; x.paragraph_format.space_before=Pt(8); x.paragraph_format.space_after=Pt(1); x.paragraph_format.keep_with_next=True; font(x.add_run(f'{kind} {n}'),10,bold=True)
    y=doc.add_paragraph(); y.paragraph_format.first_line_indent=Inches(0); y.paragraph_format.line_spacing=1; y.paragraph_format.space_after=Pt(3); y.paragraph_format.keep_with_next=True; font(y.add_run(title),10,italic=True)
def table(n,title,headers,rows,widths=None,size=8.5):
    caption(n,title,'Tabla'); t=doc.add_table(rows=1,cols=len(headers)); t.style='Table Grid'; t.alignment=WD_TABLE_ALIGNMENT.CENTER; t.autofit=False
    rp=t.rows[0]._tr.get_or_add_trPr(); rh=OxmlElement('w:tblHeader'); rh.set(qn('w:val'),'true'); rp.append(rh)
    for j,v in enumerate(headers):
        c=t.rows[0].cells[j]; c.text=''; c.vertical_alignment=WD_CELL_VERTICAL_ALIGNMENT.CENTER
        sh=OxmlElement('w:shd'); sh.set(qn('w:fill'),'D9E2F3'); c._tc.get_or_add_tcPr().append(sh)
        z=c.paragraphs[0]; z.paragraph_format.first_line_indent=Inches(0); z.paragraph_format.line_spacing=1; z.paragraph_format.space_after=Pt(0); font(z.add_run(str(v)),size,bold=True)
    for row in rows:
        cells=t.add_row().cells; pr=t.rows[-1]._tr.get_or_add_trPr(); pr.append(OxmlElement('w:cantSplit'))
        for j,v in enumerate(row):
            c=cells[j]; c.text=''; c.vertical_alignment=WD_CELL_VERTICAL_ALIGNMENT.CENTER; z=c.paragraphs[0]; z.paragraph_format.first_line_indent=Inches(0); z.paragraph_format.line_spacing=1; z.paragraph_format.space_after=Pt(0); font(z.add_run(str(v)),size)
    if widths:
        for row in t.rows:
            for j,w in enumerate(widths): row.cells[j].width=Inches(w)
    p('',indent=False,size=8)
    return t
def figure(n,title,img,note,width=6.25):
    caption(n,title)
    x=doc.add_paragraph(); x.alignment=WD_ALIGN_PARAGRAPH.CENTER; x.paragraph_format.first_line_indent=Inches(0); x.paragraph_format.line_spacing=1; x.paragraph_format.keep_with_next=True
    pic=x.add_run().add_picture(str(img),width=Inches(width))
    try: pic._inline.docPr.set('descr',title); pic._inline.docPr.set('title',title)
    except Exception: pass
    y=doc.add_paragraph(); y.paragraph_format.first_line_indent=Inches(0); y.paragraph_format.line_spacing=1; y.paragraph_format.space_after=Pt(5); font(y.add_run('Nota. '),9,italic=True); font(y.add_run(note),9)

# APA 7 student title page; missing institution/instructor/date stay as clear fields to complete.
for _ in range(3): p('',indent=False)
p('Comparación de modelos de regresión para estimar PM2.5 con datos horarios abiertos de SENAMHI en Lima Metropolitana (2015–2024)',False,WD_ALIGN_PARAGRAPH.CENTER,12,True)
for _ in range(2): p('',indent=False)
for v in ['Robert Eloy Herrera Ccari','[Institución educativa]','Curso de Inteligencia Artificial','[Nombre del docente]','[Fecha de entrega]']: p(v,False,WD_ALIGN_PARAGRAPH.CENTER)
doc.add_page_break()

head('Resumen',1)
abstract=('Este trabajo compara modelos de aprendizaje automático para estimar la concentración horaria de PM2.5 en siete estaciones de Lima Metropolitana. Se utilizaron datos abiertos del Servicio Nacional de Meteorología e Hidrología del Perú (SENAMHI), con 577 794 registros entre enero de 2015 y mayo de 2024. Luego de convertir fechas, eliminar duplicados exactos y consolidar registros repetidos por estación y hora, quedaron 577 710 filas. Para el experimento principal se seleccionaron 209 102 observaciones con valores disponibles de PM2.5, PM10 y NO2. La tarea se definió como estimación contemporánea: el modelo usa PM10 y NO2 medidos en la misma hora, además de la estación y variables temporales; por ello, no constituye un pronóstico de horas futuras. Se compararon un baseline de la media, regresión lineal, K vecinos más cercanos, árbol de decisión, Random Forest y un Voting que promedia regresión lineal y Random Forest. Los datos se dividieron cronológicamente, con entrenamiento hasta diciembre de 2022 y prueba desde enero de 2023 hasta mayo de 2024. Debido al costo de ejecución se usaron muestras reproducibles de 30 000 registros de entrenamiento y 15 000 de prueba. Random Forest obtuvo el menor error en la comparación principal (MAE = 5.165; RMSE = 8.144; R² = .499), mientras que Voting obtuvo RMSE = 8.300. El Random Forest superó al baseline, pero el valor de R² muestra que aún queda variabilidad sin explicar. Las combinaciones adicionales ensayadas no demostraron una mejora bajo sus protocolos actuales. El modelo guardado puede reutilizarse con registros compatibles, pero no debe interpretarse como una alerta oficial ni como una predicción futura.')
wc=len(re.findall(r'\b[\wÁÉÍÓÚáéíóúñÑ²]+\b',abstract)); assert 200<=wc<=300,wc
p(abstract,False)
x=doc.add_paragraph(); x.paragraph_format.first_line_indent=Inches(0); x.paragraph_format.line_spacing=2; font(x.add_run('Palabras clave: '),12,italic=True); font(x.add_run('calidad del aire, PM2.5, aprendizaje automático, regresión, Random Forest, Lima Metropolitana'))
doc.add_page_break()

head('1. Título',1); p('Comparación de modelos de regresión para estimar PM2.5 con datos horarios abiertos de SENAMHI en Lima Metropolitana (2015–2024). El CSV contiene registros desde el 1 de enero de 2015 hasta el 31 de mayo de 2024; el título no supone que existan datos para todos los meses de 2024.')
head('2. Resumen',1); p('El resumen se presenta al inicio. Incluye el contexto, el objetivo, la fuente, la preparación, los modelos, la validación temporal, las métricas, el hallazgo principal y su límite. Tiene entre 200 y 300 palabras.')
head('3. Palabras clave',1); p('Calidad del aire; PM2.5; aprendizaje automático; regresión; Random Forest; Lima Metropolitana.')

head('4. Introducción',1)
p('La contaminación del aire es un tema relevante para la salud y la gestión ambiental. Entre los contaminantes monitoreados se encuentra el material particulado fino PM2.5, definido por su diámetro aerodinámico de hasta 2.5 micrómetros. La Organización Mundial de la Salud (OMS, 2021) publicó recomendaciones para PM2.5 y otros contaminantes; estas guías sanitarias no deben confundirse con los estándares legales peruanos. En el Perú, el Decreto Supremo N.° 003-2017-MINAM fija los Estándares de Calidad Ambiental (ECA) para aire. Para PM2.5, el ECA diario es de 50 µg/m³ (Ministerio del Ambiente, 2017; SENAMHI, 2024b).')
p('Los boletines oficiales muestran cambios por estación y periodo. En enero de 2024, SENAMHI reportó excedencias del ECA diario en SMP, CRS y CRB, con un máximo de 86.46 µg/m³ en Carabayllo. En agosto de 2026, el boletín mensual reportó un máximo de 63.9 µg/m³ en Pariachi. Son episodios localizados, no valores representativos de toda Lima ni comparables directamente con estimaciones horarias (SENAMHI, 2024, 2026).')
p('En Lima ya se han estudiado diferentes formas de analizar contaminantes. Montalvo et al. (2022) describieron un sistema local con sensores de bajo costo y modelos de IA que genera mapas y pronósticos de seis horas. Rojas et al. (2022) y Sánchez-Ccoyllo y Alonso (2024) estudiaron concentraciones de PM mediante simulación atmosférica y modelos de transporte químico. Solis Teran et al. (2025) compararon modelos estadísticos y redes neuronales para pronosticar PM10, mientras que Gavidia et al. (2026) clasificaron categorías de calidad del aire con registros horarios de SENAMHI.')
p('Este trabajo pregunta qué regresor estima con menor error el PM2.5 de la misma hora si se conocen PM10, NO2, estación y variables temporales. Se comparan varios modelos y un baseline mediante una separación cronológica. El aporte es documentar una comparación reproducible con datos locales abiertos y guardar un pipeline; no se pretende sustituir instrumentos oficiales ni emitir alertas.')

head('5. Situación problemática',1)
p('El recurso de SENAMHI contiene registros horarios validados de PM10, PM2.5 y NO2, pero presenta faltantes: 36.38 % en PM2.5, 34.06 % en PM10 y 48.22 % en NO2. Además, el análisis se limita a las siete estaciones y al periodo del archivo. Los faltantes describen disponibilidad, pero no prueban por sí solos una falla de monitoreo.')
p('En enero de 2024 se registraron concentraciones diarias de PM2.5 superiores al ECA de 50 µg/m³ en SMP, CRS y CRB; Carabayllo alcanzó 86.46 µg/m³. En agosto de 2026, SENAMHI describió una excedencia en Pariachi con 63.9 µg/m³. Son promedios diarios y periodos distintos a la prueba horaria del notebook; se citan como evidencia de episodios localizados, no como resultado del modelo (SENAMHI, 2024b, 2026).')
p('La pregunta práctica es si las otras mediciones horarias permiten estimar PM2.5 para una observación cuando su etiqueta está disponible en el histórico. El experimento no evalúa alertas futuras ni una recuperación operativa de lecturas faltantes en una red en producción.')

head('6. Identificación y formulación del problema',1)
head('Problema general',2); p('No se ha determinado, para este conjunto y bajo una prueba temporal reproducible, qué modelo estima PM2.5 con menor error a partir de estación, tiempo, PM10 y NO2 de la misma hora.')
head('Causas y factores relacionados',2); p('Los registros tienen campos vacíos; la disponibilidad varía por estación y fecha; y las relaciones entre contaminantes pueden no ser lineales. El análisis describe estos factores, pero no prueba que sean causas de la concentración.')
head('Consecuencias y necesidad',2); p('Sin una comparación local resulta difícil seleccionar una alternativa para este ejercicio. Se necesita contrastar varios modelos con un test temporal común y explicar los límites de la tarea.')
head('Evidencias',2); p('La evidencia incluye los conteos de faltantes y duplicados del CSV, las siete estaciones, las 209 102 filas completas de modelado y los boletines oficiales que muestran variabilidad de PM2.5.')

head('7. Pregunta de investigación',1)
p('¿Qué desempeño presentan distintos modelos de regresión para estimar las concentraciones horarias de PM2.5 usando estación, variables temporales y mediciones de PM10 y NO2 de la misma hora en los datos abiertos de monitoreo de Lima Metropolitana?')

head('8. Objetivos',1)
head('Objetivo general',2); p('Comparar modelos de aprendizaje automático para estimar PM2.5 en los registros de monitoreo de Lima Metropolitana, utilizando datos abiertos de SENAMHI y una evaluación temporal, con el fin de identificar el modelo con menor error en el periodo de prueba.')
head('Objetivos específicos',2)
for s in ['OE1. Describir la estructura, cobertura y calidad de los datos de SENAMHI.','OE2. Preparar los registros y documentar el tratamiento de fechas, duplicados, faltantes y variables.','OE3. Entrenar y comparar un baseline, modelos de regresión y combinaciones mediante una partición temporal.','OE4. Evaluar los resultados, identificar el modelo con menor error y guardar su pipeline para datos compatibles.']: bullet(s)
table(1,'Relación entre pregunta, objetivos, experimentos y evidencia',['Problema / pregunta','Objetivo','Método','Evidencia'],[
('Estimar PM2.5 con datos reales.','OE1','Describir la fuente, periodo, estaciones y faltantes.','Ficha y tabla de calidad.'),
('La base tiene vacíos y horas repetidas.','OE2','Convertir fechas y consolidar estación-hora con mediana.','Conteos antes/después.'),
('No se conoce qué modelo minimiza el error.','OE3','Comparar baseline, regresores y Voting.','Métricas del test temporal.'),
('Se necesita reutilizar el modelo elegido.','OE4','Evaluar y guardar el mejor pipeline.','Tabla comparativa y ficha joblib.')], [1.8,.7,2.3,1.65],8.2)

head('9. Justificación',1)
p('La justificación práctica es académica: una comparación local permite observar si los datos abiertos contienen información útil para estimar PM2.5 en la misma hora. La justificación tecnológica es evaluar aprendizaje automático frente a un baseline, sin asumir que el modelo más complejo será superior. Las revisiones de Yin (2025) y Karmoude et al. (2025) muestran que el análisis de PM2.5 incluye estimación, predicción y distintos tipos de modelos; el desempeño depende de la tarea y los datos.')
p('La justificación científica es acotada: se deja evidencia de una comparación reproducible con datos de siete estaciones de Lima y una prueba posterior en el tiempo. La justificación metodológica es organizar el proceso en comprensión, preparación, modelado y evaluación, siguiendo el esquema general CRISP-DM (Wirth & Hipp, 2000). El resultado no es una herramienta oficial de vigilancia.')

head('10. Antecedentes y estado del arte',1)
p('Se seleccionaron estudios que ubican el problema local, comparan tareas y muestran que un ensamble puede o no mejorar según el caso. No se comparan sus métricas numéricamente cuando cambian la variable objetivo, ciudad, entradas o validación.')
table(2,'Estudios relacionados',['Estudio','Método y hallazgo','Relación con este proyecto'],[
('Montalvo et al. (2022), Lima','Sensores de bajo costo, IA y mapas; evalúa predicción espacial/temporal y pronósticos de 6 h.','Antecedente local; tarea diferente a estimación contemporánea.'),
('Rojas et al. (2022), Lima','CCATT-BRAMS y datos SENAMHI para simular PM y analizar meteorología.','Contexto local de PM; método físico, no mismos regresores.'),
('Sánchez-Ccoyllo y Alonso (2024), Lima-Callao','BRAMS 5.2 y emisiones vehiculares para mejorar simulación de PM10/PM2.5.','Antecedente peruano de modelado, distinto a ML supervisado.'),
('Tian et al. (2024), Macao','Stacking LSTM + XGBoost con LightGBM meta; superó métodos comparados en su conjunto.','Ensamble exitoso en otro contexto; no garantiza mejora aquí.'),
('Solis Teran et al. (2025), Lima','Series de tiempo y LSTM para PM10; ARIMA y SSA tuvieron menor error medio que LSTM.','Ejemplo local de modelo tradicional competitivo; objetivo distinto.'),
('Gavidia et al. (2026), Lima','Gaussian Naïve Bayes para categorías con 768 185 registros SENAMHI y división temporal.','Antecedente local de clasificación; no predice valor numérico.'),
('Karmoude et al. (2025); Yin (2025)','Revisiones de ML y análisis de PM2.5.','Ubican métodos, tareas y límites de generalización.')],[1.3,2.75,2.4],8.1)
p('Estos antecedentes muestran trabajos peruanos de simulación, monitoreo y pronóstico. El aporte estudiantil es comparar regresores clásicos con datos abiertos y dejar explícito que las variables de PM10 y NO2 son contemporáneas.')

head('11. Marco conceptual',1)
head('PM2.5, PM10 y NO2',2); p('PM2.5 identifica partículas finas de hasta 2.5 µm; PM10, partículas de hasta 10 µm; NO2 es dióxido de nitrógeno. El CSV registra estas variables por estación y hora. Los boletines de SENAMHI reportan concentraciones en µg/m³, pero el diccionario local no declara explícitamente la unidad en las columnas, por lo que se recomienda confirmarla.')
head('Regresión y modelos',2); p('La regresión estima un número. El baseline predice la media; la regresión lineal representa relaciones lineales; KNN estima a partir de vecinos; un árbol genera reglas; Random Forest promedia árboles para representar patrones no lineales (Breiman, 2001). Voting promedia las predicciones de modelos diferentes. Un ensamble ayuda si reduce errores; añadir modelos no garantiza una mejora.')
head('Métricas e interpretación',2); p('MAE es el error absoluto promedio; RMSE penaliza más los errores grandes; R² compara el error con la variación alrededor de la media y puede ser negativo. La importancia por permutación mide cuánto cambia el score al mezclar una variable, pero no demuestra causalidad.')
head('Estimación contemporánea y pronóstico',2); p('PM10 y NO2 se miden a la misma hora que el PM2.5 objetivo. Por ello, el modelo estima PM2.5 contemporáneo cuando conoce esos valores; no anticipa horas futuras. Un pronóstico requeriría variables disponibles antes del instante objetivo y otra validación.')

head('12. Metodología de investigación',1)
p('El enfoque es cuantitativo y aplicado: se analizan mediciones numéricas reales y se construye un artefacto de aprendizaje automático. El diseño es comparativo y experimental porque se entrenan modelos alternativos y se evalúan en el mismo periodo temporal para el análisis principal. La unidad de análisis es un registro consolidado estación-hora. No se interviene sobre estaciones ni se recolectan datos personales.')
head('13. Metodología de desarrollo de IA',1)
p('El notebook sigue etapas didácticas de CRISP-DM: comprensión del problema, comprensión y preparación de datos, modelado, evaluación y guardado del pipeline. El guardado local no equivale a despliegue productivo. CRISP-DM organiza de manera iterativa proyectos de minería de datos (Wirth & Hipp, 2000).')
head('14. Fase 1: comprensión del problema',1)
p('El prototipo recibe estación, fecha, hora, PM10 y NO2 y devuelve un PM2.5 estimado de la misma observación. El criterio principal es menor RMSE, acompañado de MAE y R². La restricción esencial es que no genera alertas oficiales ni predice horas futuras.')

head('15. Fase 2: comprensión de los datos',1)
p('La fuente es el conjunto “Monitoreo de los contaminantes del aire en Lima Metropolitana”, de SENAMHI, disponible en la Plataforma Nacional de Datos Abiertos. Los metadatos indican mediciones horarias validadas, formato CSV, actualización mensual, licencia Open Data Commons Attribution y cobertura 2015–2024. El archivo estudiado contiene 577 794 filas, 15 columnas y siete estaciones hasta el 31 de mayo de 2024. El boletín de 2026 describe una red actual de diez estaciones, que no debe confundirse con las siete del CSV analizado (SENAMHI, 2024a, 2026).')
table(3,'Ficha resumida del conjunto de datos',['Característica','Descripción'],[
('Entidad/fuente','SENAMHI, Plataforma Nacional de Datos Abiertos.'),('Periodo','2015-01-01 a 2024-05-31.'),('Tamaño','577 794 filas, 15 columnas.'),('Estaciones','Siete estaciones en Lima Metropolitana.'),('Unidad','Medición estación-hora; claves repetidas se consolidan.'),('Objetivo','PM2_5 numérico.'),('Entradas','ESTACION, PM10, NO2, hora, día semana, mes y variables cíclicas.'),('Licencia','Open Data Commons Attribution, según metadatos.'),('Unidad física','El diccionario local no la señala; boletines reportan µg/m³. Confirmar con SENAMHI.')],[1.75,4.7],8.8)

head('16. Ingeniería y preparación de datos',1)
p('Se normalizaron estaciones, se convirtieron campos numéricos y se unieron FECHA y HORA en una marca temporal. No hubo fechas inválidas ni duplicados idénticos. Se encontraron 84 repeticiones en 42 claves estación-hora y se consolidaron con la mediana de PM10, PM2.5 y NO2, quedando 577 710 filas.')
p('Para modelar se seleccionaron filas con PM2.5, PM10 y NO2 presentes: 209 102 observaciones. Se agregaron hora, día de semana, mes y codificaciones seno/coseno para hora y día del año. Los valores extremos se revisaron, pero no se eliminaron automáticamente; no se observaron valores negativos en los tres contaminantes.')
table(4,'Calidad de datos y preparación',['Control','Resultado','Lectura'],[
('Fechas inválidas','0','No hubo descartes por fecha.'),('Duplicados exactos','0','No se encontraron filas idénticas.'),('Claves repetidas','84 filas / 42 claves','Consolidadas con mediana.'),('Filas limpias','577 710','Después de consolidar.'),('PM10 faltante','196 812 (34.06%)','No se imputó para el caso completo principal.'),('PM2.5 faltante','210 203 (36.38%)','No se usa como etiqueta si falta.'),('NO2 faltante','278 602 (48.22%)','Se excluye del caso completo.'),('Filas completas','209 102','166 568 antes de 2023; 42 534 desde 2023.')],[1.45,1.85,3.15],8.3)
figure(1,'Valores faltantes y mediciones disponibles por año',quality,'La disponibilidad cambia por contaminante y periodo; la figura no identifica por sí sola la causa de los faltantes.')
figure(2,'Mediciones válidas por año y distribución de PM2.5 por estación',station,'El boxplot oculta puntos extremos para facilitar lectura; esos valores no fueron eliminados del modelado.')

head('17. Diseño de la solución',1)
p('El flujo lee el CSV, limpia y consolida filas, construye variables de estación/tiempo/contaminantes, aplica preprocesamiento y Random Forest, y produce una estimación. El diagrama representa un artefacto local, no un servicio en tiempo real.')
caption(3,'Flujo del artefacto de estimación')
p('Datos abiertos SENAMHI  →  limpieza y consolidación  →  variables de estación y hora  →  pipeline + Random Forest  →  estimación de PM2.5 para la misma hora',False,WD_ALIGN_PARAGRAPH.CENTER,10)
p('Nota. El modelo utiliza PM10 y NO2 medidos en el mismo instante; elaboración propia a partir del notebook.',False,size=9)
head('Requisitos principales',2)
bullet('Funcional: recibir estación, fecha/hora, PM10 y NO2; preparar variables y devolver PM2.5 estimado.')
bullet('No funcional: conservar preprocesamiento y modelo juntos, registrar versiones y semilla.')
bullet('Restricción: no usar como predicción futura si no se conocen PM10 y NO2 del instante objetivo.')

head('18. Desarrollo e implementación',1)
head('Variables y pipeline',2)
p('El pipeline numérico imputa mediana y estandariza; ESTACION se codifica con One-Hot Encoding. El modelado ya requiere PM10 y NO2 presentes. Se compararon regresión lineal; KNN (7 vecinos, distancia); árbol (profundidad 14, mínimo 5 por hoja); Random Forest (100 árboles, profundidad 18, mínimo 3 por hoja); Voting de lineal + Random Forest; y baseline de media. El pipeline se implementó con herramientas de scikit-learn (Pedregosa et al., 2011).')
head('Modelo guardado',2)
p('`modelo_pm25_senamhi.joblib` guarda el pipeline de Random Forest, clave `mejor_individual`, y una ficha con métricas y combinaciones probadas. No guarda el clasificador ni K-Means. Es un archivo serializado que requiere Python y un esquema de entradas compatible; no es por sí mismo una aplicación.')

head('19. Diseño experimental',1)
p('La partición principal fue cronológica: entrenamiento disponible entre 2015-02-03 y 2022-12-31; prueba entre 2023-01-01 y 2024-05-31. Para reducir tiempo se tomaron 30 000 filas de entrenamiento y 15 000 de prueba con semilla 42. La comparación principal usó el mismo test para los seis modelos. El preprocesamiento se ajustó dentro del pipeline.')
p('Los ensambles adicionales entrenaron modelos base con datos anteriores a 2022 y usaron 2022 para pesos/meta-modelo, dejando 2023–2024 para prueba. Esto evita elegir el ensamble con el test, pero los modelos base recibieron menos periodo/datos que el RF principal. Sus resultados son exploratorios y no aíslan perfectamente el efecto de la combinación.')

head('20. Evaluación',1)
p('RMSE es la métrica principal porque penaliza más los errores grandes; MAE complementa con el error absoluto promedio; R² expresa ajuste respecto a la media y puede ser negativo. Se usaron 15 000 observaciones de prueba. Los errores están en la escala numérica del campo; debe confirmarse la unidad del CSV antes de interpretarlos como µg/m³. La importancia por permutación se calculó con 3 000 filas de prueba, tres repeticiones y score −MAE.')

head('21. Resultados',1)
head('Comparación principal',2)
p('Random Forest obtuvo el menor RMSE en la prueba temporal: MAE = 5.165, RMSE = 8.144 y R² = .499. Voting quedó segundo con RMSE = 8.300. El baseline de la media obtuvo RMSE = 11.885 y R² = −.067.')
table(5,'Métricas de regresión en la prueba temporal',['Modelo','MAE','RMSE','R²'],[
('Baseline de la media','9.325','11.885','−.067'),('Regresión lineal','6.748','9.604','.304'),('KNN regresor','6.823','9.774','.279'),('Árbol regresor','6.047','9.385','.335'),('Random Forest regresor','5.165','8.144','.499'),('Voting: lineal + Random Forest','5.505','8.300','.480')],[3.5,1,1,1],9)
figure(4,'RMSE y valores reales frente a estimados por Random Forest',models,'Métricas calculadas sobre 15 000 filas; dispersión de hasta 3 000 puntos, línea roja = igualdad entre real y estimado.')
head('Combinaciones y análisis complementarios',2)
p('Voting presentó correlación entre errores de .739. Su promedio no mejoró al Random Forest (RMSE 8.300 frente a 8.144). La mezcla ponderada eligió peso cero para lineal y uno para bosque en 2022; su resultado adicional fue MAE 6.486, RMSE 9.430, R² .328. Stacking de cuatro modelos y RidgeCV obtuvo MAE 6.064, RMSE 8.283, R² .482. Ninguna combinación superó al RF principal, pero la diferencia de periodo/volumen de entrenamiento limita una comparación causal definitiva.')
table(6,'Experimentos adicionales de combinación',['Experimento','MAE','RMSE','R²','Nota'],[
('RF principal','5.165','8.144','.499','Entrenamiento hasta 2022.'),('Mezcla ponderada','6.486','9.430','.328','0 % lineal + 100 % RF, base anterior a 2022.'),('Stacking + RidgeCV','6.064','8.283','.482','Bases anteriores a 2022; meta en 2022.')],[1.6,.65,.65,.5,3.1],8.2)
p('Clasificación y K-Means fueron complementarios. El umbral exploratorio de “PM2.5 relativamente alto” fue el percentil 75 del entrenamiento (31.70), no un límite sanitario. La proporción positiva fue .250 en train y .156 en test. Random Forest clasificador obtuvo F1 = .618 y Voting de logística + bosque F1 = .574. En K-Means, k = 2 tuvo el silhouette mayor entre k=2–6 (.425); las medianas de PM10/PM2.5/NO2 fueron 96.70/38.70/31.40 para el grupo 0 y 40.91/17.18/17.00 para el grupo 1. Los grupos no son categorías oficiales.')
p('La importancia por permutación fue mayor para PM10 (4.2881) y estación (1.4517). Esto expresa dependencia predictiva del modelo en esta muestra, no causalidad.')
figure(5,'Importancia por permutación del Random Forest',importance,'Cambio del score −MAE al permutar cada variable; valores mayores indican mayor dependencia predictiva en esa evaluación, no efecto causal.')

head('22. Discusión',1)
p('Random Forest superó al baseline y a los otros regresores en esta prueba. El promedio de árboles representó patrones de los datos con menor error que una regresión lineal. Aun así, R² = .499 indica ajuste parcial; no todos los cambios de PM2.5 se explican con las variables usadas. Revisiones de la literatura describen buenos resultados de Random Forest y XGBoost en datos estructurados, pero subrayan que la elección depende de la tarea y del comportamiento temporal (Karmoude et al., 2025; Yin, 2025).')
p('Voting no mejoró al mejor componente. La correlación de errores .739 indica errores parcialmente parecidos, aunque no explica por sí sola la causa. Tian et al. (2024) sí reportaron un stacking exitoso para Macao con LSTM, XGBoost y LightGBM. La diferencia no contradice este resultado porque cambian ciudad, variables, modelos, arquitectura y protocolo. Aquí el stacking quedó cercano, pero por debajo del RF principal, y tuvo menos años de entrenamiento.')
p('Los trabajos de Montalvo et al. (2022), Rojas et al. (2022) y Sánchez-Ccoyllo y Alonso (2024) muestran otros enfoques locales de medición, simulación y pronóstico. El presente proyecto no los reemplaza; ofrece una comparación sencilla con un dataset abierto. Como PM10 y NO2 son contemporáneos, sus resultados no deben presentarse como alerta anticipada.')

head('23. Amenazas a la validez y limitaciones',1)
for s in [
'Validez interna: la comparación principal usó muestras de 30 000 filas de entrenamiento y 15 000 de prueba, no todas las filas completas; otra muestra podría cambiar métricas.',
'Ensambles: sus experimentos usaron un periodo y tamaño de entrenamiento distinto al RF principal; se reportan como exploratorios.',
'Validez temporal: solo se evaluó un corte (2023–mayo de 2024); cambios futuros pueden alterar resultados.',
'Validez externa: siete estaciones del archivo no representan automáticamente toda Lima, Perú ni la red actual.',
'Validez de constructo: se estima PM2.5 contemporáneo con PM10 y NO2 de esa misma hora; no es pronóstico futuro ni alerta oficial.',
'Calidad: hay altos porcentajes de valores faltantes, especialmente NO2 (48.22 %); los casos completos podrían no representar toda la red.',
'Unidad: el diccionario descargado no especifica explícitamente unidades; confirmar con SENAMHI antes de atribuir unidad física a las métricas.',
'Validez de conclusión: no se calcularon intervalos de confianza ni se repitieron varios cortes temporales.'
]: bullet(s)

head('24. Consideraciones éticas',1)
p('Se usaron registros públicos ambientales y no datos personales. Corresponde atribuir a SENAMHI y respetar la licencia indicada. La responsabilidad está en mantener la integridad de los datos, documentar faltantes y evitar comunicar una estimación como medición oficial (Alemohammad, 2026). El umbral P75 = 31.70 se eligió para practicar clasificación y no es ECA ni guía de la OMS.')

head('25. Reproducibilidad',1)
p('El notebook registra Python 3.13.1, pandas 3.0.5, scikit-learn 1.9.1 y semilla 42. Para repetirlo, se descarga el CSV, se cambia la ruta en la configuración y se ejecutan las celdas en orden. Se guardan `resultados_senamhi/models/modelo_pm25_senamhi.joblib` y `resultados_senamhi/ficha_modelo.json`. El modelo requiere columnas compatibles; otra computadora debe ajustar la ruta y conservar el esquema del CSV.')

head('26. Conclusiones',1)
for s in [
'OE1: el CSV original contiene 577 794 filas, 15 columnas y siete estaciones entre enero de 2015 y mayo de 2024; PM2.5, PM10 y NO2 presentan valores faltantes.',
'OE2: se consolidaron 42 claves repetidas estación-hora (84 filas extra) y quedaron 577 710 registros. Para regresión se usaron 209 102 casos completos.',
'OE3/OE4: Random Forest tuvo el menor RMSE (8.144) y R² .499 en la muestra de prueba; superó al baseline, aunque deja variabilidad sin explicar.',
'Voting y las combinaciones adicionales no superaron al RF principal en los resultados reportados. El joblib guarda el pipeline RF individual; esto no demuestra que los ensambles sean siempre inferiores.',
'El modelo estima PM2.5 para la misma hora con PM10 y NO2 contemporáneos; no predice horas futuras ni sustituye una comunicación oficial.'
]: bullet(s)

head('27. Recomendaciones y trabajo futuro',1)
for s in [
'Confirmar con SENAMHI la unidad exacta de los campos del CSV.',
'Probar varios cortes temporales o validación de origen móvil.',
'Repetir Voting, mezcla y stacking con igual periodo y volumen de entrenamiento, reservando validación y test por separado.',
'Analizar errores por estación y por rango de PM2.5; añadir intervalos de incertidumbre.',
'Para pronosticar el futuro, usar variables disponibles antes del momento objetivo, como retardos horarios, y diseñar un nuevo test cronológico.',
'Si se hace una interfaz, presentarla como prototipo académico y aclarar que no sustituye mediciones ni alertas de SENAMHI.'
]: bullet(s)

doc.add_page_break(); head('28. Referencias',1)
refs=[
'Alemohammad, H. (2026). Data considerations for AI applications in environmental context. Field Actions Science Reports, Special Report, 34–39. https://journals.openedition.org/factsreports/8096',
'Breiman, L. (2001). Random forests. Machine Learning, 45, 5–32. https://doi.org/10.1023/A:1010933404324',
'Gavidia, A., Dominguez, A., & Flores-Chacón, E. (2026). Predicting air pollution in Metropolitan Lima using Gaussian Naïve Bayes (2025): An efficient model for urban environmental management. Sustainability, 18(11), Article 5748. https://doi.org/10.3390/su18115748',
'Karmoude, M., Munhungewarwa, B., Chiraira, I., Mckenzie, R., Kong, J., Smith, B., Ayana, G., Njara, N., Mathaha, T., Kumar, M., & Mellado, B. (2025). Machine learning for air quality prediction and data analysis: Review on recent advancements, challenges, and outlooks. Science of the Total Environment, 1002, Article 180593. https://doi.org/10.1016/j.scitotenv.2025.180593',
'Ministerio del Ambiente. (2017). Decreto Supremo N.° 003-2017-MINAM: Aprueban los estándares de calidad ambiental (ECA) para aire y establecen disposiciones complementarias. https://www.gob.pe/institucion/minam/normas-legales/3670-003-2017-minam',
'Montalvo, L., Fosca, D., Paredes, D., Abarca, M., Saito, C., & Villanueva, E. (2022). An air quality monitoring and forecasting system for Lima City with low-cost sensors and artificial intelligence models. Frontiers in Sustainable Cities, 4, Article 849762. https://doi.org/10.3389/frsc.2022.849762',
'Pedregosa, F., Varoquaux, G., Gramfort, A., Michel, V., Thirion, B., Grisel, O., Blondel, M., Prettenhofer, P., Weiss, R., Dubourg, V., Vanderplas, J., Passos, A., Cournapeau, D., Brucher, M., Perrot, M., & Duchesnay, É. (2011). Scikit-learn: Machine learning in Python. Journal of Machine Learning Research, 12, 2825–2830. https://jmlr.org/papers/v12/pedregosa11a.html',
'Rojas, F. J., Pacsi-Valdivia, S., & Sánchez-Ccoyllo, O. (2022). Simulación computacional e influencia de las variables meteorológicas en las concentraciones de PM10 y PM2.5 en Lima Metropolitana. Información Tecnológica, 33(3), 223–238. https://doi.org/10.4067/S0718-07642022000300223',
'Sánchez-Ccoyllo, O. R., & Alonso, M. (2024). Improving PM10 and PM2.5 concentration prediction using the Brazilian Regional Atmospheric Modeling 5.2 System in Lima, Peru. Urban Climate, 55, Article 101985. https://doi.org/10.1016/j.uclim.2024.101985',
'SENAMHI. (2024a). Monitoreo de los contaminantes del aire en Lima Metropolitana [Conjunto de datos]. Plataforma Nacional de Datos Abiertos. https://www.datosabiertos.gob.pe/dataset/monitoreo-de-los-contaminantes-del-aire-en-lima-metropolitana-servicio-nacional-de',
'SENAMHI. (2024b). Vigilancia de la calidad del aire en el Área Metropolitana de Lima y Callao (AMLC): Enero 2024 [Boletín]. https://www.senamhi.gob.pe/load/file/03201SENA-130.pdf',
'SENAMHI. (2026). Vigilancia de la calidad del aire en el Área Metropolitana de Lima y Callao (AMLC): Agosto 2026 [Boletín]. https://www.senamhi.gob.pe/load/file/03201SENA-163.pdf',
'Solis Teran, M. A., Leite Coelho da Silva, F., Torres Armas, E. A., Carbo-Bustinza, N., & López-Gonzales, J. L. (2025). Modeling air pollution in Metropolitan Lima: A statistical and artificial neural network approach. Environments, 12(6), Article 196. https://doi.org/10.3390/environments12060196',
'Tian, H., Kong, H., & Wong, C. (2024). A novel stacking ensemble learning approach for predicting PM2.5 levels in dense urban environments using meteorological variables: A case study in Macau. Applied Sciences, 14(12), Article 5062. https://doi.org/10.3390/app14125062',
'World Health Organization. (2021). WHO global air quality guidelines: Particulate matter (PM2.5 and PM10), ozone, nitrogen dioxide, sulfur dioxide and carbon monoxide. https://www.who.int/publications/i/item/9789240034228',
'Wirth, R., & Hipp, J. (2000). CRISP-DM: Towards a standard process model for data mining. In Proceedings of the 4th International Conference on the Practical Applications of Knowledge Discovery and Data Mining (pp. 29–39).',
'Yin, P.-Y. (2025). A review on PM2.5 sources, mass prediction, and association analysis: Research opportunities and challenges. Sustainability, 17(3), Article 1101. https://doi.org/10.3390/su17031101'
]
for ref in refs:
    x=doc.add_paragraph(); x.paragraph_format.left_indent=Inches(.5); x.paragraph_format.first_line_indent=Inches(-.5); x.paragraph_format.line_spacing=2; x.paragraph_format.space_after=Pt(0); x.paragraph_format.keep_together=True; font(x.add_run(ref),11)

head('29. Anexos',1)
head('Anexo A. Resultados auxiliares',2)
p('La clasificación y K-Means son complementarios y no cambian la pregunta principal de regresión.',False)
table(7,'Clasificación exploratoria de PM2.5 relativamente alto',['Modelo','Acc.','Prec.','Rec.','F1','ROC-AUC','PR-AUC'],[
('Baseline mayoritaria','.844','.000','.000','.000','—','—'),('Regresión logística','.839','.483','.465','.474','.839','.514'),('KNN clasificador','.843','.494','.317','.386','.765','.404'),('Árbol clasificador','.857','.542','.532','.537','.843','.522'),('Random Forest clasificador','.894','.710','.548','.618','.933','.678'),('Voting logística + RF','.888','.708','.483','.574','.920','.677')],[2.0,.65,.65,.65,.55,.85,.85],7.6)
p('El umbral fue el percentil 75 del entrenamiento (31.70); el porcentaje positivo cambió de 25.0 % en train a 15.6 % en test. No es un umbral sanitario.',False,size=9)
table(8,'Perfiles de K-Means con k = 2',['Grupo','Mediana PM10','Mediana PM2.5','Mediana NO2'],[('0','96.70','38.70','31.40'),('1','40.91','17.18','17.00')],[1.3,1.7,1.8,1.6],9)
p('Silhouette = .425, mayor entre k=2–6 probados. Las etiquetas de grupo son arbitrarias.',False,size=9)
head('Anexo B. Archivos del proyecto',2)
for s in ['Notebook: PARCIAL IA SENAHMI.ipynb.','Modelo: resultados_senamhi/models/modelo_pm25_senamhi.joblib.','Ficha: resultados_senamhi/ficha_modelo.json.','Dataset, metadatos y diccionario: Plataforma Nacional de Datos Abiertos / SENAMHI.']: bullet(s)

for t in doc.tables:
    t.alignment=WD_TABLE_ALIGNMENT.CENTER
    for row in t.rows:
        for c in row.cells:
            for par in c.paragraphs: par.paragraph_format.widow_control=True
doc.core_properties.title='Comparación de modelos de regresión para estimar PM2.5 en Lima Metropolitana'
doc.core_properties.subject='Paper académico con datos abiertos de SENAMHI'
doc.core_properties.author='Robert Eloy Herrera Ccari'
doc.core_properties.keywords='SENAMHI, PM2.5, Lima, aprendizaje automático, APA 7'
out=ROOT/'Paper_IA_Calidad_del_Aire_Lima_SENAMHI.docx'; doc.save(out)
print('CREATED',out,'ABSTRACT_WORDS',wc,'REFERENCES',len(refs),'TABLES',len(doc.tables),'PARAGRAPHS',len(doc.paragraphs))
