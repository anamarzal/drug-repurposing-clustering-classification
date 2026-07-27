'''
import pandas as pd
import numpy as np
from sklearn.cluster import DBSCAN
from sklearn.metrics import silhouette_score, davies_bouldin_score

#Cargar los datos preparados
df = pd.read_excel("farmacos_preparadosCOMPROBACION.xlsx")

#Eliminar las columnas 'ChEMBL ID' y las columnas de indicaciones
columns_to_drop = ['ChEMBL ID', 'Indicacion1', 'Indicacion2', 'Indicacion3', 'Indicacion4', 'Indicacion5', 'Indicacion6', 'Indicacion7']
df_clustering = df.drop(columns=columns_to_drop)

#Convertir la columna 'Fingerprint Vector' (cadena) en una lista de números binarios
fingerprint_list = df_clustering['Fingerprint Vector'].apply(lambda x: np.array(list(map(int, x.split(','))))).apply(np.array)

# Verificar la longitud de los fingerprints
fingerprint_lengths = fingerprint_list.apply(len)
print("Longitudes de los fingerprints:", fingerprint_lengths.unique())

#Agregar la columna de fingerprints al DataFrame
fingerprint_matrix = np.vstack(fingerprint_list)
df_clustering = df_clustering.drop(columns=['Fingerprint Vector'])
df_clustering = pd.concat([df_clustering, pd.DataFrame(fingerprint_matrix)], axis=1)

#Usar los datos ya normalizados (no aplicar normalización adicional)
final_data = df_clustering.values

# Probar diferentes combinaciones de parámetros de DBSCAN
eps_values = [0.1, 0.2, 0.25, 0.3, 0.40, 0.5]  # Distancia máxima entre dos puntos
min_samples_values = [3, 5, 10]  # Número mínimo de puntos para formar un cluster

best_score = -1
best_db_score = float('inf')  # Davies-Bouldin es un score donde menor es mejor
best_params = None
best_model = None

for eps in eps_values:
    for min_samples in min_samples_values:
        # Crear el modelo DBSCAN con los parámetros
        clusterer = DBSCAN(eps=eps, min_samples=min_samples)
        
        # Ajustar el modelo
        clusters = clusterer.fit_predict(final_data)
        
        # Calcular los scores de las métricas de calidad (solo si hay más de 1 cluster)
        if len(np.unique(clusters)) > 1:
            silhouette = silhouette_score(final_data, clusters)
            davis_bouldin = davies_bouldin_score(final_data, clusters)
            print(f"EPS: {eps}, Min_samples: {min_samples}, Silhouette Score: {silhouette}, Davies-Bouldin Score: {davis_bouldin}")
            
            # Guardar los mejores parámetros según el Silhouette Score
            if silhouette > best_score:
                best_score = silhouette
                best_db_score = davis_bouldin
                best_params = (eps, min_samples)
                best_model = clusterer

#Imprimir los mejores parámetros y el modelo
print(f"\nMejores parámetros encontrados: EPS={best_params[0]}, Min_samples={best_params[1]}")
print(f"Silhouette Score: {best_score}")
print(f"Davies-Bouldin Score: {best_db_score}")

#Ajustar el modelo final con los mejores parámetros
best_model.fit(final_data)

#Obtener los clusters finales
df['DBSCAN_Cluster'] = best_model.labels_

#Guardar los resultados en un archivo Excel
df.to_excel("farmacos_clusterizados_dbscan_CON_F.xlsx", index=False)

#Visualizar la cantidad de elementos por cluster
print("\nDistribución de los clusters DBSCAN:")
print(df['DBSCAN_Cluster'].value_counts())

# Mostrar las primeras filas para verificar
print("\nPrimeras filas del DataFrame con resultados DBSCAN:")
print(df.head())
'''


import pandas as pd
import numpy as np
from sklearn.cluster import DBSCAN
from sklearn.metrics import silhouette_score, davies_bouldin_score

#Cargar los datos preparados
df = pd.read_excel("farmacos_preparadosCOMPROBACION.xlsx")

#Eliminar las columnas 'ChEMBL ID', las columnas de indicaciones y la columna 'Fingerprint Vector'
columns_to_drop = ['ChEMBL ID', 'Indicacion1', 'Indicacion2', 'Indicacion3', 'Indicacion4', 'Indicacion5', 'Indicacion6', 'Indicacion7', 'Fingerprint Vector']
df_clustering = df.drop(columns=columns_to_drop)

# Usar los datos ya normalizados (no aplicar normalización adicional)
final_data = df_clustering.values

#Probar diferentes combinaciones de parámetros de DBSCAN
eps_values = [0.1, 0.2, 0.25, 0.3, 0.40, 0.5]  # Distancia máxima entre dos puntos
min_samples_values = [3, 5, 10]  # Número mínimo de puntos para formar un cluster

best_score = -1
best_db_score = float('inf')  # Davies-Bouldin es un score donde menor es mejor
best_params = None
best_model = None

for eps in eps_values:
    for min_samples in min_samples_values:
        # Crear el modelo DBSCAN con los parámetros
        clusterer = DBSCAN(eps=eps, min_samples=min_samples)
        
        # Ajustar el modelo
        clusters = clusterer.fit_predict(final_data)
        
        # Calcular los scores de las métricas de calidad (solo si hay más de 1 cluster)
        if len(np.unique(clusters)) > 1:
            silhouette = silhouette_score(final_data, clusters)
            davis_bouldin = davies_bouldin_score(final_data, clusters)
            print(f"EPS: {eps}, Min_samples: {min_samples}, Silhouette Score: {silhouette}, Davies-Bouldin Score: {davis_bouldin}")
            
            # Guardar los mejores parámetros según el Silhouette Score
            if silhouette > best_score:
                best_score = silhouette
                best_db_score = davis_bouldin
                best_params = (eps, min_samples)
                best_model = clusterer

#Imprimir los mejores parámetros y el modelo
print(f"\nMejores parámetros encontrados: EPS={best_params[0]}, Min_samples={best_params[1]}")
print(f"Silhouette Score: {best_score}")
print(f"Davies-Bouldin Score: {best_db_score}")

#Ajustar el modelo final con los mejores parámetros
best_model.fit(final_data)

#  Obtener los clusters finales
df['DBSCAN_Cluster'] = best_model.labels_

#Guardar los resultados en un archivo Excel
df.to_excel("farmacos_clusterizados_dbscan_SIN_F.xlsx", index=False)

#  Visualizar la cantidad de elementos por cluster
print("\nDistribución de los clusters DBSCAN:")
print(df['DBSCAN_Cluster'].value_counts())

#  Mostrar las primeras filas para verificar
print("\nPrimeras filas del DataFrame con resultados DBSCAN:")
print(df.head())



