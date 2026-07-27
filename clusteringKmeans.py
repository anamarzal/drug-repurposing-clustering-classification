
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score, davies_bouldin_score
from sklearn.decomposition import PCA

# Cargar los datos preparados
df = pd.read_excel("farmacos_preparadosCOMPROBACION.xlsx")

#Eliminar las columnas 'ChEMBL ID' y las columnas de indicaciones
columns_to_drop = ['ChEMBL ID', 'Indicacion1', 'Indicacion2', 'Indicacion3', 'Indicacion4', 'Indicacion5', 'Indicacion6', 'Indicacion7']
df_clustering = df.drop(columns=columns_to_drop)

#Convertir la columna 'Fingerprint Vector' (cadena) en una lista de números binarios
fingerprint_list = df_clustering['Fingerprint Vector'].apply(lambda x: np.array(list(map(int, x.split(',')))))


#Agregar la columna de fingerprints al DataFrame
fingerprint_matrix = np.vstack(fingerprint_list)
df_clustering = df_clustering.drop(columns=['Fingerprint Vector'])
df_clustering = pd.concat([df_clustering, pd.DataFrame(fingerprint_matrix)], axis=1)

#Convertir el DataFrame a una matriz NumPy
final_data = df_clustering.values

#Aplicar K-Means y calcular métricas
k_values = [3, 4, 5, 6]
cluster_results = {}
metrics = {}

for k in k_values:
    kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
    df[f'Cluster_K{k}'] = kmeans.fit_predict(final_data)
    
    # Calcular métricas
    silhouette = silhouette_score(final_data, df[f'Cluster_K{k}'])
    davies_bouldin = davies_bouldin_score(final_data, df[f'Cluster_K{k}'])
    
    # Guardar resultados
    cluster_results[k] = kmeans
    metrics[k] = {"Silhouette Score": silhouette, "Davies-Bouldin Score": davies_bouldin}

#Guardar los resultados en un archivo Excel
df.to_excel("farmacos_clusterizados_kmeans_con_F.xlsx", index=False)

#Visualizar distribución de los clusters
fig, axes = plt.subplots(1, 4, figsize=(18, 5))

for i, k in enumerate(k_values):
    axes[i].hist(df[f'Cluster_K{k}'], bins=k, color="b", alpha=0.7, rwidth=0.8)
    axes[i].set_title(f"Distribución de Clusters para K={k}")
    axes[i].set_xlabel("Cluster")
    axes[i].set_ylabel("Número de Fármacos")

plt.tight_layout()
plt.show()

#Mostrar las métricas en una tabla
metrics_df = pd.DataFrame(metrics).T
print(metrics_df)

#Graficar métricas para comparación
fig, ax = plt.subplots(1, 2, figsize=(12, 5))

ax[0].plot(metrics_df.index, metrics_df["Silhouette Score"], marker='o', linestyle='--', color='g')
ax[0].set_title('Índice de Silueta')
ax[0].set_xlabel('Número de Clusters (k)')
ax[0].set_ylabel('Silhouette Score')

ax[1].plot(metrics_df.index, metrics_df["Davies-Bouldin Score"], marker='o', linestyle='--', color='r')
ax[1].set_title('Coeficiente de Davies-Bouldin')
ax[1].set_xlabel('Número de Clusters (k)')
ax[1].set_ylabel('Davies-Bouldin Score')

plt.show()

#Visualizar los clusters en 2D con PCA
pca = PCA(n_components=2)
principal_components = pca.fit_transform(final_data)

# Graficar los puntos de los clusters
fig, axes = plt.subplots(1, 4, figsize=(18, 5))

for i, k in enumerate(k_values):
    axes[i].scatter(principal_components[:, 0], principal_components[:, 1], c=df[f'Cluster_K{k}'], cmap='viridis', alpha=0.7)
    axes[i].set_title(f"Clusters in 2D for K={k}")
    axes[i].set_xlabel("Principal Component 1")
    axes[i].set_ylabel("Principal Component 2")

plt.tight_layout()
plt.show()



'''
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score, davies_bouldin_score
from sklearn.decomposition import PCA

#Cargar los datos preparados
df = pd.read_excel("farmacos_preparadosCOMPROBACION.xlsx")

#Eliminar las columnas 'ChEMBL ID' y las columnas de indicaciones
columns_to_drop = ['ChEMBL ID', 'Indicacion1', 'Indicacion2', 'Indicacion3', 'Indicacion4', 'Indicacion5', 'Indicacion6', 'Indicacion7', 'Fingerprint Vector']
df_clustering = df.drop(columns=columns_to_drop)

#Aquí no es necesario convertir la columna de fingerprints
# Solo utilizamos las características numéricas restantes. Asegúrate de que las columnas que queden sean adecuadas para clustering.

#Convertir el DataFrame a una matriz NumPy (usando las características numéricas)
final_data = df_clustering.values

#Aplicar K-Means y calcular métricas
k_values = [3, 4, 5, 6]
cluster_results = {}
metrics = {}

for k in k_values:
    kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
    df[f'Cluster_K{k}'] = kmeans.fit_predict(final_data)
    
    # Calcular métricas
    silhouette = silhouette_score(final_data, df[f'Cluster_K{k}'])
    davies_bouldin = davies_bouldin_score(final_data, df[f'Cluster_K{k}'])
    
    # Guardar resultados
    cluster_results[k] = kmeans
    metrics[k] = {"Silhouette Score": silhouette, "Davies-Bouldin Score": davies_bouldin}

#Guardar los resultados en un archivo Excel
df.to_excel("farmacos_clusterizados_kmeans_sin_F.xlsx", index=False)

#Visualizar distribución de los clusters
fig, axes = plt.subplots(1, 4, figsize=(18, 5))

for i, k in enumerate(k_values):
    axes[i].hist(df[f'Cluster_K{k}'], bins=k, color="b", alpha=0.7, rwidth=0.8)
    axes[i].set_title(f"Distribución de Clusters para K={k}")
    axes[i].set_xlabel("Cluster")
    axes[i].set_ylabel("Número de Fármacos")

plt.tight_layout()
plt.show()

# Mostrar las métricas en una tabla
metrics_df = pd.DataFrame(metrics).T
print(metrics_df)

#Graficar métricas para comparación
fig, ax = plt.subplots(1, 2, figsize=(12, 5))

ax[0].plot(metrics_df.index, metrics_df["Silhouette Score"], marker='o', linestyle='--', color='g')
ax[0].set_title('Índice de Silueta')
ax[0].set_xlabel('Número de Clusters (k)')
ax[0].set_ylabel('Silhouette Score')

ax[1].plot(metrics_df.index, metrics_df["Davies-Bouldin Score"], marker='o', linestyle='--', color='r')
ax[1].set_title('Coeficiente de Davies-Bouldin')
ax[1].set_xlabel('Número de Clusters (k)')
ax[1].set_ylabel('Davies-Bouldin Score')

plt.show()

#Visualizar los clusters en 2D con PCA
pca = PCA(n_components=2)
principal_components = pca.fit_transform(final_data)

# Graficar los puntos de los clusters
fig, axes = plt.subplots(1, 4, figsize=(18, 5))

for i, k in enumerate(k_values):
    axes[i].scatter(principal_components[:, 0], principal_components[:, 1], c=df[f'Cluster_K{k}'], cmap='viridis', alpha=0.7)
    axes[i].set_title(f"Clusters in 2D for K={k}")
    axes[i].set_xlabel("Principal Component 1")
    axes[i].set_ylabel("Principal Component 2")

plt.tight_layout()
plt.show()
'''


