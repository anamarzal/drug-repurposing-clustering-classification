
import pandas as pd
import numpy as np
from sklearn.mixture import GaussianMixture
from sklearn.metrics import silhouette_score, davies_bouldin_score
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA

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

#Usar los datos ya normalizados (sin normalización adicional)
final_data = df_clustering.values

#Búsqueda de n_components usando AIC, BIC, Silhouette y Davies-Bouldin
best_aic = np.inf
best_bic = np.inf
best_silhouette = -1
best_davies_bouldin = np.inf

best_n_components_aic = None
best_n_components_bic = None
best_n_components_silhouette = None
best_n_components_davies_bouldin = None

# Realizar el ajuste para diferentes valores de n_components
for n_components in range(1, 11):  # Probamos entre 1 y 10 componentes
    gmm = GaussianMixture(n_components=n_components, random_state=42)
    gmm.fit(final_data)
    
    # Calcular AIC y BIC
    aic = gmm.aic(final_data)
    bic = gmm.bic(final_data)
    
    # Predecir las etiquetas para calcular las métricas de calidad
    clusters = gmm.predict(final_data)
    
    # Inicializar las métricas con valores predeterminados
    silhouette = -1
    davis_bouldin = np.inf
    
    # Solo calcular Silhouette y Davies-Bouldin si hay más de 1 cluster
    if n_components > 1 and len(np.unique(clusters)) > 1:
        silhouette = silhouette_score(final_data, clusters)
        davis_bouldin = davies_bouldin_score(final_data, clusters)
    
    print(f"n_components = {n_components}, AIC = {aic}, BIC = {bic}, Silhouette Score = {silhouette}, Davies-Bouldin Score = {davis_bouldin}")
    
    # Guardar los mejores parámetros según AIC, BIC, Silhouette y Davies-Bouldin
    if aic < best_aic:
        best_aic = aic
        best_n_components_aic = n_components
    
    if bic < best_bic:
        best_bic = bic
        best_n_components_bic = n_components
    
    if silhouette > best_silhouette:
        best_silhouette = silhouette
        best_n_components_silhouette = n_components
    
    if davis_bouldin < best_davies_bouldin:
        best_davies_bouldin = davis_bouldin
        best_n_components_davies_bouldin = n_components

print("\nMejor número de componentes según AIC:", best_n_components_aic)
print("Mejor número de componentes según BIC:", best_n_components_bic)
print("Mejor número de componentes según Silhouette Score:", best_n_components_silhouette)
print("Mejor número de componentes según Davies-Bouldin Score:", best_n_components_davies_bouldin)

#Usar el número óptimo de componentes (según las métricas AIC, BIC, Silhouette o Davies-Bouldin)
# Aquí se puede elegir el mejor según cualquiera de las métricas. Ejemplo usando AIC:
optimal_n_components = best_n_components_silhouette  # O puedes elegir cualquier otro basado en tu preferencia de métrica.

final_gmm = GaussianMixture(n_components=optimal_n_components, random_state=42)
df['GMM_Cluster'] = final_gmm.fit_predict(final_data)

#Guardar los resultados en un archivo Excel
df.to_excel("farmacos_clusterizados_gmm_CON_F.xlsx", index=False)

#Visualizar la cantidad de elementos por cluster
print("\nDistribución de los clusters GMM:")
print(df['GMM_Cluster'].value_counts())

#Visualizar los clusters con PCA para ver la separación
pca = PCA(n_components=2)
features_2d = pca.fit_transform(final_data)

# Graficar los clusters
plt.figure(figsize=(8, 6))
plt.scatter(features_2d[:, 0], features_2d[:, 1], c=df['GMM_Cluster'], cmap='viridis', s=50)
plt.title('Visualización de los clusters GMM con PCA')
plt.xlabel('Componente Principal 1')
plt.ylabel('Componente Principal 2')
plt.colorbar(label='Cluster')
plt.show()

#Mostrar las primeras filas para verificar
print("\nPrimeras filas del DataFrame con resultados GMM:")
print(df.head())





'''
import pandas as pd
import numpy as np
from sklearn.mixture import GaussianMixture
from sklearn.metrics import silhouette_score, davies_bouldin_score
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA

#Cargar los datos preparados
df = pd.read_excel("farmacos_preparadosCOMPROBACION.xlsx")

#Eliminar las columnas 'ChEMBL ID' y las columnas de indicaciones
columns_to_drop = ['ChEMBL ID', 'Indicacion1', 'Indicacion2', 'Indicacion3', 'Indicacion4', 'Indicacion5', 'Indicacion6', 'Indicacion7', 'Fingerprint Vector']
df_clustering = df.drop(columns=columns_to_drop)

# Usar los datos ya normalizados (sin la columna de fingerprints)
final_data = df_clustering.values

#Búsqueda de n_components usando AIC, BIC, Silhouette y Davies-Bouldin
best_aic = np.inf
best_bic = np.inf
best_silhouette = -1
best_davies_bouldin = np.inf

best_n_components_aic = None
best_n_components_bic = None
best_n_components_silhouette = None
best_n_components_davies_bouldin = None

# Realizar el ajuste para diferentes valores de n_components
for n_components in range(1, 11):  # Probamos entre 1 y 10 componentes
    gmm = GaussianMixture(n_components=n_components, random_state=42)
    gmm.fit(final_data)
    
    # Calcular AIC y BIC
    aic = gmm.aic(final_data)
    bic = gmm.bic(final_data)
    
    # Predecir las etiquetas para calcular las métricas de calidad
    clusters = gmm.predict(final_data)
    
    # Inicializar las métricas con valores predeterminados
    silhouette = -1
    davis_bouldin = np.inf
    
    # Solo calcular Silhouette y Davies-Bouldin si hay más de 1 cluster
    if n_components > 1:
        silhouette = silhouette_score(final_data, clusters)
        davis_bouldin = davies_bouldin_score(final_data, clusters)
    
    print(f"n_components = {n_components}, AIC = {aic}, BIC = {bic}, Silhouette Score = {silhouette}, Davies-Bouldin Score = {davis_bouldin}")
    
    # Guardar los mejores parámetros según AIC, BIC, Silhouette y Davies-Bouldin
    if aic < best_aic:
        best_aic = aic
        best_n_components_aic = n_components
    
    if bic < best_bic:
        best_bic = bic
        best_n_components_bic = n_components
    
    if silhouette > best_silhouette:
        best_silhouette = silhouette
        best_n_components_silhouette = n_components
    
    if davis_bouldin < best_davies_bouldin:
        best_davies_bouldin = davis_bouldin
        best_n_components_davies_bouldin = n_components

print("\nMejor número de componentes según AIC:", best_n_components_aic)
print("Mejor número de componentes según BIC:", best_n_components_bic)
print("Mejor número de componentes según Silhouette Score:", best_n_components_silhouette)
print("Mejor número de componentes según Davies-Bouldin Score:", best_n_components_davies_bouldin)

#Usar el número óptimo de componentes (según las métricas AIC, BIC, Silhouette o Davies-Bouldin)
# Aquí se puede elegir el mejor según cualquiera de las métricas. Ejemplo usando AIC:
#optimal_n_components = best_n_components_silhouette # O puedes elegir cualquier otro basado en tu preferencia de métrica.
optimal_n_components = best_n_components_davies_bouldin

final_gmm = GaussianMixture(n_components=optimal_n_components, random_state=42)
df['GMM_Cluster'] = final_gmm.fit_predict(final_data)

#Guardar los resultados en un archivo Excel
df.to_excel("farmacos_clusterizados_gmm_SIN_F_d.xlsx", index=False)

#Visualizar la cantidad de elementos por cluster
print("\nDistribución de los clusters GMM:")
print(df['GMM_Cluster'].value_counts())

 Visualizar los clusters con PCA para ver la separación
pca = PCA(n_components=2)
features_2d = pca.fit_transform(final_data)

# Graficar los clusters
plt.figure(figsize=(8, 6))
plt.scatter(features_2d[:, 0], features_2d[:, 1], c=df['GMM_Cluster'], cmap='viridis', s=50)
plt.title('Visualización de los clusters GMM con PCA / Silhouette Score  ')
plt.xlabel('Componente Principal 1')
plt.ylabel('Componente Principal 2')
plt.colorbar(label='Cluster')
plt.show()

#Mostrar las primeras filas para verificar
print("\nPrimeras filas del DataFrame con resultados GMM:")
print(df.head())
'''

