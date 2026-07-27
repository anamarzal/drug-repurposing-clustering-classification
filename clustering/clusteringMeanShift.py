
import pandas as pd
import numpy as np
from sklearn.cluster import MeanShift
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


#Usar los datos ya normalizados (sin fingerprints)
final_data = df_clustering.values

#Probar diferentes combinaciones de parámetros de MeanShift
bandwidth_values = [0.5, 1, 2, 4, 6, 8, 10, 12, 15]  # Ajusta estos valores según tus datos

best_score_silhouette = -1
best_score_davies = np.inf  # El mejor Davies-Bouldin es el más bajo
best_bandwidth = None
best_model = None

for bandwidth in bandwidth_values:
    # Crear el modelo MeanShift con el parámetro 'bandwidth'
    clusterer = MeanShift(bandwidth=bandwidth)
    
    # Ajustar el modelo
    clusters = clusterer.fit_predict(final_data)
    
    # Imprimir el número de clusters generados
    num_clusters = len(np.unique(clusters))
    print(f"Bandwidth: {bandwidth}, Número de Clusters: {num_clusters}")
    
    # Calcular las métricas solo si hay más de un cluster
    if num_clusters > 1:
        silhouette = silhouette_score(final_data, clusters)
        davies_bouldin = davies_bouldin_score(final_data, clusters)
        
        # Imprimir los resultados para cada valor de bandwidth
        print(f"Silhouette Score: {silhouette}, Davies-Bouldin Score: {davies_bouldin}")
        
        # Guardar los mejores parámetros
        if silhouette > best_score_silhouette:
            best_score_silhouette = silhouette
            best_score_davies = davies_bouldin
            best_bandwidth = bandwidth
            best_model = clusterer

#Imprimir los mejores parámetros y el modelo
print(f"\nMejores parámetros encontrados: Bandwidth={best_bandwidth}")
print(f"Silhouette Score: {best_score_silhouette}, Davies-Bouldin Score: {best_score_davies}")

#Ajustar el modelo final con el mejor parámetro
best_model.fit(final_data)

#Obtener los clusters finales
df['MeanShift_Cluster'] = best_model.labels_

#Visualizar la cantidad de elementos por cluster
print("\nDistribución de los clusters MeanShift:")
print(df['MeanShift_Cluster'].value_counts())

#Visualizar los clusters con PCA para ver la separación
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt

pca = PCA(n_components=2)
features_2d = pca.fit_transform(final_data)

plt.figure(figsize=(8, 6))
plt.scatter(features_2d[:, 0], features_2d[:, 1], c=df['MeanShift_Cluster'], cmap='viridis', s=50, alpha=0.7)
plt.title('Visualización de los clusters MeanShift con PCA con Huellas Moleculares')
plt.xlabel('Componente Principal 1')
plt.ylabel('Componente Principal 2')
plt.colorbar(label='Cluster')
plt.grid(True)
plt.tight_layout()
plt.show()

#Mostrar las primeras filas para verificar
print("\nPrimeras filas del DataFrame con resultados MeanShift:")
print(df.head())

#Guardar los resultados en un archivo Excel
df.to_excel("farmacos_clusterizados_meanshift_CON_F.xlsx", index=False)



'''
import pandas as pd
import numpy as np
from sklearn.cluster import MeanShift
from sklearn.metrics import silhouette_score, davies_bouldin_score

#Cargar los datos preparados
df = pd.read_excel("farmacos_preparadosCOMPROBACION.xlsx")

#Eliminar las columnas 'ChEMBL ID' y las columnas de indicaciones
columns_to_drop = ['ChEMBL ID', 'Indicacion1', 'Indicacion2', 'Indicacion3', 'Indicacion4', 'Indicacion5', 'Indicacion6', 'Indicacion7', 'Fingerprint Vector']
df_clustering = df.drop(columns=columns_to_drop)

#Usar los datos ya normalizados (sin fingerprints)
final_data = df_clustering.values

# Probar diferentes combinaciones de parámetros de MeanShift
bandwidth_values = [0.5, 1, 2, 4, 6, 8, 10, 12, 15]  # Ajusta estos valores según tus datos

best_score_silhouette = -1
best_score_davies = np.inf  # El mejor Davies-Bouldin es el más bajo
best_bandwidth = None
best_model = None

for bandwidth in bandwidth_values:
    # Crear el modelo MeanShift con el parámetro 'bandwidth'
    clusterer = MeanShift(bandwidth=bandwidth)
    
    # Ajustar el modelo
    clusters = clusterer.fit_predict(final_data)
    
    # Imprimir el número de clusters generados
    num_clusters = len(np.unique(clusters))
    print(f"Bandwidth: {bandwidth}, Número de Clusters: {num_clusters}")
    
    # Calcular las métricas solo si hay más de un cluster
    if num_clusters > 1:
        silhouette = silhouette_score(final_data, clusters)
        davies_bouldin = davies_bouldin_score(final_data, clusters)
        
        # Imprimir los resultados para cada valor de bandwidth
        print(f"Silhouette Score: {silhouette}, Davies-Bouldin Score: {davies_bouldin}")
        
        # Guardar los mejores parámetros
        if silhouette > best_score_silhouette:
            best_score_silhouette = silhouette
            best_score_davies = davies_bouldin
            best_bandwidth = bandwidth
            best_model = clusterer

#Imprimir los mejores parámetros y el modelo
print(f"\nMejores parámetros encontrados: Bandwidth={best_bandwidth}")
print(f"Silhouette Score: {best_score_silhouette}, Davies-Bouldin Score: {best_score_davies}")

#Ajustar el modelo final con el mejor parámetro
best_model.fit(final_data)

#Obtener los clusters finales
df['MeanShift_Cluster'] = best_model.labels_

#Visualizar la cantidad de elementos por cluster
print("\nDistribución de los clusters MeanShift:")
print(df['MeanShift_Cluster'].value_counts())

# Visualizar los clusters con PCA para ver la separación
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt

pca = PCA(n_components=2)
features_2d = pca.fit_transform(final_data)

plt.figure(figsize=(8, 6))
plt.scatter(features_2d[:, 0], features_2d[:, 1], c=df['MeanShift_Cluster'], cmap='viridis', s=50, alpha=0.7)
plt.title('Visualización de los clusters MeanShift con PCA sin Huellas Moleculares')
plt.xlabel('Componente Principal 1')
plt.ylabel('Componente Principal 2')
plt.colorbar(label='Cluster')
plt.grid(True)
plt.tight_layout()
plt.show()

#Mostrar las primeras filas para verificar
print("\nPrimeras filas del DataFrame con resultados MeanShift:")
print(df.head())

#Guardar los resultados en un archivo Excel
df.to_excel("farmacos_clusterizados_meanshift_SIN_F.xlsx", index=False)
'''

