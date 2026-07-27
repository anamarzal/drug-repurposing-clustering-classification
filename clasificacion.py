#CLASIFICACION DE GMM, KMEAN Y MEANSHIFT (3 BLOQUES SEPARADOS) + MODELOS DE CLASIFICACION GUARDADOS. 

'''
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
from sklearn.metrics import classification_report, confusion_matrix, roc_curve, auc
import matplotlib.pyplot as plt
import joblib

import sklearn
print(sklearn.__version__)


# Cargar los datos
print("Cargando los datos...")
df = pd.read_excel('farmacos_clusterizados_gmm_SIN_F.xlsx')
print(f"Datos cargados. Total de filas: {df.shape[0]} y columnas: {df.shape[1]}.")

# Filtrar solo el Cluster 0
print("Filtrando los fármacos del Cluster...")
df_cluster0 = df[df['GMM_Cluster'] == 1].copy()
print(f"Total de fármacos en el Cluster: {df_cluster0.shape[0]}.")

# Definir la indicación a predecir
indicacion = "Antibacterial"
print(f"Indicador a predecir: {indicacion}")

# Crear la variable objetivo (1 si tiene la indicación especificada, 0 si no)
print(f"Creando la variable objetivo para la indicación {indicacion}...")
df_cluster0[indicacion] = df_cluster0[[f'Indicacion{i}' for i in range(1, 8)]].apply(
    lambda x: 1 if indicacion in x.values else 0, axis=1
)
print(f"Se ha creado la variable objetivo. Ejemplo de los primeros valores: {df_cluster0[indicacion].head()}.")

# Seleccionar características físico-químicas
print(f"Seleccionando características físico-químicas...")
features = ['Molecular Weight', 'Targets', 'AlogP', 'Polar Surface Area', 'HBA', 'HBD',
            '#RO5 Violations', '#Rotatable Bonds', 'QED Weighted', 'Aromatic Rings']
X = df_cluster0[features]
y = df_cluster0[indicacion]
print(f"Características seleccionadas: {features}. Ejemplo de los primeros valores de las características: {X.head()}.")

# Dividir en conjunto de entrenamiento y prueba (80% entrenamiento, 20% prueba)
print("Dividiendo los datos en conjunto de entrenamiento y prueba...")
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
print(f"Conjunto de entrenamiento: {X_train.shape[0]} muestras, Conjunto de prueba: {X_test.shape[0]} muestras.")

# Entrenar un modelo de Random Forest
print("Entrenando el modelo de Random Forest...")
clf = RandomForestClassifier(n_estimators=100, random_state=42)
clf.fit(X_train, y_train)
print("Modelo entrenado.")

#GUARDAMOS MODELOS PARA INTERFAZ
joblib.dump(clf, 'modelo_rf_gmm_cluster1_antibacteriano.pkl')

# Evaluar el modelo
print("Evaluando el modelo...")
y_pred = clf.predict(X_test)
print(classification_report(y_test, y_pred))

# Matriz de confusión
print("Matriz de Confusión:")
cm = confusion_matrix(y_test, y_pred)
print(cm)

# Graficar la matriz de confusión
plt.figure(figsize=(6, 6))
plt.imshow(cm, interpolation='nearest', cmap=plt.cm.Blues)
plt.title('Matriz de Confusión GMM.')
plt.colorbar()
tick_marks = np.arange(2)
plt.xticks(tick_marks, ['No ' + indicacion, indicacion], rotation=45)
plt.yticks(tick_marks, ['No ' + indicacion, indicacion])
plt.xlabel('Predicción')
plt.ylabel('Real')
plt.tight_layout()
plt.show()

# Aplicar el modelo a fármacos del Cluster 0 que NO tienen la indicación especificada
print(f"Filtrando fármacos en el Cluster que NO tienen la indicación {indicacion}...")
df_no_indicacion = df_cluster0[df_cluster0[indicacion] == 0].copy()
print(f"Total de fármacos sin la indicación {indicacion}: {df_no_indicacion.shape[0]}.")

X_no_indicacion = df_no_indicacion[features]

# Predecir si alguno podría tener la indicación especificada
print("Realizando predicciones sobre los fármacos sin la indicación...")
predictions = clf.predict(X_no_indicacion)
df_no_indicacion[f'Predicted {indicacion}'] = predictions

# Guardar los fármacos reposicionados en un archivo
df_repositioned = df_no_indicacion[df_no_indicacion[f'Predicted {indicacion}'] == 1]
df_repositioned.to_excel(f'farmacos_reposicionados_{indicacion}_GMM_0.xlsx', index=False)

print(f"Se han identificado {df_repositioned.shape[0]} fármacos potencialmente reposicionados como {indicacion}.")
'''

#---------------------------------------------------------------------------------------------------------------------

'''
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
import joblib


# Cargar los datos
print("Cargando los datos...")
df = pd.read_excel('farmacos_clusterizados_kmeans_SIN_F.xlsx')
print(f"Datos cargados. Total de filas: {df.shape[0]} y columnas: {df.shape[1]}.")

# Filtrar solo el Cluster 3
print("Filtrando los fármacos del Cluster 3...")
df_cluster3 = df[df['Cluster_K3'] == 1].copy()
print(f"Total de fármacos en el Cluster 3: {df_cluster3.shape[0]}.")

# Definir la indicación a predecir
indicacion = "Antibacterial"
print(f"Indicador a predecir: {indicacion}")

# Crear la variable objetivo (1 si tiene la indicación especificada, 0 si no)
print(f"Creando la variable objetivo para la indicación {indicacion}...")
df_cluster3[indicacion] = df_cluster3[[f'Indicacion{i}' for i in range(1, 8)]].apply(
    lambda x: 1 if indicacion in x.values else 0, axis=1
)
print(f"Se ha creado la variable objetivo. Ejemplo de los primeros valores: {df_cluster3[indicacion].head()}.")

# Seleccionar características físico-químicas
print(f"Seleccionando características físico-químicas...")
features = ['Molecular Weight', 'Targets', 'AlogP', 'Polar Surface Area', 'HBA', 'HBD',
            '#RO5 Violations', '#Rotatable Bonds', 'QED Weighted', 'Aromatic Rings']
X = df_cluster3[features]
y = df_cluster3[indicacion]
print(f"Características seleccionadas: {features}. Ejemplo de los primeros valores de las características: {X.head()}.")

# Dividir en conjunto de entrenamiento y prueba (80% entrenamiento, 20% prueba)
print("Dividiendo los datos en conjunto de entrenamiento y prueba...")
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
print(f"Conjunto de entrenamiento: {X_train.shape[0]} muestras, Conjunto de prueba: {X_test.shape[0]} muestras.")

# Entrenar un modelo de Random Forest
print("Entrenando el modelo de Random Forest...")
clf = RandomForestClassifier(n_estimators=100, random_state=42)
clf.fit(X_train, y_train)
print("Modelo entrenado.")

#GUARDAMOS MODELOS PARA INTERFAZ
joblib.dump(clf, 'modelo_rf_kmeans_cluster0_antibacteriano.pkl')

# Evaluar el modelo
print("Evaluando el modelo...")
y_pred = clf.predict(X_test)
print(classification_report(y_test, y_pred))

# Aplicar el modelo a fármacos del Cluster 3 que NO tienen la indicación especificada
print(f"Filtrando fármacos en el Cluster 3 que NO tienen la indicación {indicacion}...")
df_no_indicacion = df_cluster3[df_cluster3[indicacion] == 0].copy()
print(f"Total de fármacos sin la indicación {indicacion}: {df_no_indicacion.shape[0]}.")

X_no_indicacion = df_no_indicacion[features]

# Predecir si alguno podría tener la indicación especificada
print("Realizando predicciones sobre los fármacos sin la indicación...")
predictions = clf.predict(X_no_indicacion)
df_no_indicacion[f'Predicted {indicacion}'] = predictions

# Guardar los fármacos reposicionados en un archivo
df_repositioned = df_no_indicacion[df_no_indicacion[f'Predicted {indicacion}'] == 1]
df_repositioned.to_excel(f'farmacos_reposicionados_{indicacion}_kmeans_Cluster3_1.xlsx', index=False)

print(f"Se han identificado {df_repositioned.shape[0]} fármacos potencialmente reposicionados como {indicacion}.")
'''

#------------------------------------------------------------------------------------------------------------------------------

'''
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
from sklearn.metrics import classification_report, confusion_matrix, roc_curve, auc
import matplotlib.pyplot as plt
import joblib

import sklearn
print(sklearn.__version__)

# Cargar los datos
print("Cargando los datos...")
df = pd.read_excel('farmacos_clusterizados_meanshift_SIN_F.xlsx')
print(f"Datos cargados. Total de filas: {df.shape[0]} y columnas: {df.shape[1]}.")

# Filtrar solo el Cluster 0
print("Filtrando los fármacos del Cluster...")
df_cluster0 = df[df['MeanShift_Cluster'] == 0].copy()
print(f"Total de fármacos en el Cluster: {df_cluster0.shape[0]}.")

# Definir la indicación a predecir
indicacion = "Antineoplastic"
print(f"Indicador a predecir: {indicacion}")

# Crear la variable objetivo (1 si tiene la indicación especificada, 0 si no)
print(f"Creando la variable objetivo para la indicación {indicacion}...")
df_cluster0[indicacion] = df_cluster0[[f'Indicacion{i}' for i in range(1, 8)]].apply(
    lambda x: 1 if indicacion in x.values else 0, axis=1
)
print(f"Se ha creado la variable objetivo. Ejemplo de los primeros valores: {df_cluster0[indicacion].head()}.")

# Seleccionar características físico-químicas
print(f"Seleccionando características físico-químicas...")
features = ['Molecular Weight', 'Targets', 'AlogP', 'Polar Surface Area', 'HBA', 'HBD',
            '#RO5 Violations', '#Rotatable Bonds', 'QED Weighted', 'Aromatic Rings']
X = df_cluster0[features]
y = df_cluster0[indicacion]
print(f"Características seleccionadas: {features}. Ejemplo de los primeros valores de las características: {X.head()}.")

# Dividir en conjunto de entrenamiento y prueba (80% entrenamiento, 20% prueba)
print("Dividiendo los datos en conjunto de entrenamiento y prueba...")
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
print(f"Conjunto de entrenamiento: {X_train.shape[0]} muestras, Conjunto de prueba: {X_test.shape[0]} muestras.")

# Entrenar un modelo de Random Forest
print("Entrenando el modelo de Random Forest...")
clf = RandomForestClassifier(n_estimators=100, random_state=42)
clf.fit(X_train, y_train)
print("Modelo entrenado.")

#GUARDAMOS MODELOS PARA INTERFAZ
joblib.dump(clf, 'modelo_rf_meanshift_cluster0_antiinflamatorio.pkl')

# Evaluar el modelo
print("Evaluando el modelo...")
y_pred = clf.predict(X_test)
print(classification_report(y_test, y_pred))

# Matriz de confusión
print("Confusion Matrix Mean-Shift Antineoplastic:")
cm = confusion_matrix(y_test, y_pred)
print(cm)

# Graficar la matriz de confusión
plt.figure(figsize=(6, 6))
plt.imshow(cm, interpolation='nearest', cmap=plt.cm.Blues)
plt.title('Confusion Matrix Mean-Shift')
plt.colorbar()
tick_marks = np.arange(2)
plt.xticks(tick_marks, ['No ' + indicacion, indicacion], rotation=45)
plt.yticks(tick_marks, ['No ' + indicacion, indicacion])
plt.xlabel('Prediction')
plt.ylabel('Real')
plt.tight_layout()
plt.show()

# Aplicar el modelo a fármacos del Cluster 0 que NO tienen la indicación especificada
print(f"Filtrando fármacos en el Cluster que NO tienen la indicación {indicacion}...")
df_no_indicacion = df_cluster0[df_cluster0[indicacion] == 0].copy()
print(f"Total de fármacos sin la indicación {indicacion}: {df_no_indicacion.shape[0]}.")

X_no_indicacion = df_no_indicacion[features]

# Predecir si alguno podría tener la indicación especificada
print("Realizando predicciones sobre los fármacos sin la indicación...")
predictions = clf.predict(X_no_indicacion)
df_no_indicacion[f'Predicted {indicacion}'] = predictions

# Guardar los fármacos reposicionados en un archivo
df_repositioned = df_no_indicacion[df_no_indicacion[f'Predicted {indicacion}'] == 1]
df_repositioned.to_excel(f'farmacos_reposicionados_{indicacion}_MeanShift_0.xlsx', index=False)

print(f"Se han identificado {df_repositioned.shape[0]} fármacos potencialmente reposicionados como {indicacion}.")
'''




