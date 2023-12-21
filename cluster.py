import os
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import AgglomerativeClustering, KMeans
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.cluster.hierarchy import linkage, dendrogram

# Carregando o dataset
colunas = ['PLAYER_NAME', 'W', 'USG_PCT', 'SALARY_MILLIONS', 'TWITTER_FOLLOWER_COUNT_MILLIONS']
dataset_path = 'C:\\Users\\Davi Araujo\\Documents\\GitHub\\Analise-de-Cluster-NBA\\archive\\nba_2016_2017_100.csv'
df = pd.read_csv(dataset_path, usecols=colunas)

# Remover 'PLAYER_NAME' antes da padronização
df_selected = df.drop('PLAYER_NAME', axis=1)

# Identificar e remover outliers usando IQR
Q1 = df_selected.quantile(0.25)
Q3 = df_selected.quantile(0.75)
IQR = Q3 - Q1

outlier_mask = ~((df_selected < (Q1 - 1.5 * IQR)) | (df_selected > (Q3 + 1.5 * IQR))).any(axis=1)

# Filtrar o DataFrame para manter apenas as linhas sem outliers
df_filtered = df[outlier_mask]

# Padronização das variáveis
scaler = StandardScaler()
df_scaled = scaler.fit_transform(df_filtered.drop('PLAYER_NAME', axis=1))

# Agrupamento Hierárquico Aglomerativo
def hierarchical_clustering(n_clusters):
    model = AgglomerativeClustering(n_clusters=n_clusters, affinity='euclidean', linkage='ward')
    clusters = model.fit_predict(df_scaled)
    return clusters

# Agrupamento K-Means
def k_means_clustering(n_clusters):
    model = KMeans(n_clusters=n_clusters, random_state=42)
    clusters = model.fit_predict(df_scaled)
    return clusters

# Formação de 3, 4 e 5 grupos
num_clusters_list = [3]

# Criar as pastas se não existirem
output_folder_hierarchical = 'Imagens_Cluster_Hierarchical'
output_folder_kmeans = 'Imagens_Cluster_KMeans'
os.makedirs(output_folder_hierarchical, exist_ok=True)
os.makedirs(output_folder_kmeans, exist_ok=True)

# Caminhos dos arquivos de texto para salvar os resultados
output_txt_path_hierarchical = os.path.join(output_folder_hierarchical, 'validation_results.txt')
output_txt_path_kmeans = os.path.join(output_folder_kmeans, 'validation_results.txt')

# Lista de pares de variáveis para criar os gráficos de dispersão
variable_pairs = [('W', 'USG_PCT'),
                  ('W', 'SALARY_MILLIONS'),
                  ('USG_PCT', 'TWITTER_FOLLOWER_COUNT_MILLIONS'),
                  ('SALARY_MILLIONS', 'TWITTER_FOLLOWER_COUNT_MILLIONS')]

# Loop para criar e salvar os gráficos de dispersão e validar os agrupamentos
for num_clusters in num_clusters_list:
    # Hierarchical Clustering
    clusters_hierarchical = hierarchical_clustering(num_clusters)
    df_filtered['Cluster'] = clusters_hierarchical
    cluster_summary_hierarchical = df_filtered.drop('PLAYER_NAME', axis=1).groupby('Cluster').mean()

    # Calcular a matriz de ligação para o dendrograma
    linkage_matrix = linkage(df_scaled, method='ward')

    # Salvar dendrograma
    plt.figure(figsize=(12, 6))
    dendrogram(linkage_matrix, labels=df_filtered['PLAYER_NAME'].tolist(), orientation='top', distance_sort='descending')
    plt.title(f'Hierarchical Clustering Dendrogram - {num_clusters} Clusters')
    plt.savefig(os.path.join(output_folder_hierarchical, f'dendrogram_clusters_{num_clusters}.png'))
    plt.close()

    # Salvar resultados e gráficos para Hierarchical Clustering
    with open(output_txt_path_hierarchical, 'a') as output_file:
        output_file.write(f'\nNúmero de Clusters (Hierarchical): {num_clusters}\n')
        output_file.write(f'{cluster_summary_hierarchical}\n')

        for pair in variable_pairs:
            x_variable, y_variable = pair
            plt.figure(figsize=(10, 8))
            sns.scatterplot(data=df_filtered, x=x_variable, y=y_variable, hue='Cluster', palette='viridis')
            plt.title(f'Hierarchical Clustering - {num_clusters} Clusters\n{y_variable} vs {x_variable}')
            output_path = os.path.join(output_folder_hierarchical, f'scatter_{y_variable}_vs_{x_variable}_clusters_{num_clusters}_filtered.png')
            
            #Adicionar até 3 PLAYER_NAME em cada grupo
            for cluster_id in range(num_clusters):
                players_in_cluster = df_filtered[df_filtered['Cluster'] == cluster_id]['PLAYER_NAME'].head(3).tolist()
                for player_name in players_in_cluster:
                    player_row = df_filtered[df_filtered['PLAYER_NAME'] == player_name]
                    plt.annotate(player_name, 
                                 (player_row[x_variable].values[0], player_row[y_variable].values[0]), 
                                 textcoords="offset points",
                                 xytext=(5,5),
                                 ha='left', va='top', fontsize=8)

            plt.savefig(output_path)
            plt.close()
            output_file.write(f'Gráfico: {y_variable} vs {x_variable}\nArquivo: {output_path}\n\n')
         

    # K-Means Clustering
    clusters_kmeans = k_means_clustering(num_clusters)
    df_filtered['Cluster'] = clusters_kmeans
    cluster_summary_kmeans = df_filtered.drop('PLAYER_NAME', axis=1).groupby('Cluster').mean()

    # Salvar resultados e gráficos para K-Means Clustering
    with open(output_txt_path_kmeans, 'a') as output_file:
        output_file.write(f'\nNúmero de Clusters (K-Means): {num_clusters}\n')
        output_file.write(f'{cluster_summary_kmeans}\n')

        for pair in variable_pairs:
            x_variable, y_variable = pair
            plt.figure(figsize=(10, 8))
            sns.scatterplot(data=df_filtered, x=x_variable, y=y_variable, hue='Cluster', palette='viridis')
            plt.title(f'K-Means Clustering - {num_clusters} Clusters\n{y_variable} vs {x_variable}')
            output_path = os.path.join(output_folder_kmeans, f'scatter_{y_variable}_vs_{x_variable}_clusters_{num_clusters}_filtered.png')
            

            # Adicionar até 3 PLAYER_NAME em cada grupo
            for cluster_id in range(num_clusters):
                players_in_cluster = df_filtered[df_filtered['Cluster'] == cluster_id]['PLAYER_NAME'].head(3).tolist()
                for player_name in players_in_cluster:
                    player_row = df_filtered[df_filtered['PLAYER_NAME'] == player_name]
                    plt.annotate(player_name, 
                                 (player_row[x_variable].values[0], player_row[y_variable].values[0]), 
                                 textcoords="offset points",
                                 xytext=(5,5),
                                 ha='left', va='top', fontsize=8)

            plt.savefig(output_path)
            plt.close()
            output_file.write(f'Gráfico: {y_variable} vs {x_variable}\nArquivo: {output_path}\n\n')
            
