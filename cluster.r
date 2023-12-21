pacotes <- c("cluster", "factoextra", "dendextend")

# Instalação de pacotes ausentes
pacotes_instalar <- pacotes[!(pacotes %in% installed.packages()[,"Package"])]
if(length(pacotes_instalar) > 0) install.packages(pacotes_instalar)

# Carregamento de pacotes
pacotes_carregar <- pacotes[pacotes %in% installed.packages()[,"Package"]]
sapply(pacotes_carregar, require, character.only = TRUE)

# Carregar os pacotes necessários
library(cluster)    # Para análise de clusters e métricas
library(factoextra) # Para visualizações adicionais como gráficos de silhueta e fviz_cluster
library(dendextend) # Para manipulação e visualização de dendrogramas


dataset <- 'cluster.csv'
# Selecionando as variáveis para análise de cluster
cluster_data <- dataset[, c('PLAYER_NAME','W', 'OFF_RATING', 'DEF_RATING', 'USG_PCT', 'SALARY_MILLIONS', 'TWITTER_FOLLOWER_COUNT_MILLIONS')]

# Normalizando os dados
cluster_data_norm <- scale(cluster_data)

# Calculando a distância euclidiana
dist_matrix <- dist(cluster_data_norm, method = "euclidean")

# Realizando a análise de cluster hierárquico com o método Ward
hc <- hclust(dist_matrix, method = "ward.D2")

na_labels <- rep(NA, length = length(labels(dend)))

# Defina as etiquetas para NA
dend <- set(dend, "labels", na_labels)

# Simplificar o dendrograma para evitar poluição visual
# Removendo as etiquetas para limpar a visualização
dend <- set(dend, "labels_cex", 0)  # Define o tamanho das etiquetas para 0 para ocultá-las
dend <- set(dend, "labels", NA)     # Remove as etiquetas

# Gráfico 1: Dendrograma Simplificado
##############################################
# Criar o dendrograma a partir do objeto hclust
dend <- as.dendrogram(hc)

# Configurar para não mostrar as etiquetas
dend <- set(dend, "labels", NA)

# Configurar a altura em que as folhas são penduradas para reduzir a densidade de linhas na parte inferior
# Altere o valor de hang para -1 para alinhar todas as folhas na mesma altura
dend <- hang.dendrogram(dend, hang = -1)

# Colorir os ramos do dendrograma de acordo com os clusters
# Aqui, k é o número de clusters que você escolheu
k <- 4 
dend <- color_branches(dend, k)

# Ajustar as propriedades visuais do dendrograma
dend <- set(dend, "branches_lwd", 2) # Ajustar a espessura das linhas

# Ajustar as margens para evitar cortar o dendrograma
par(mar=c(5,4,4,2) + 0.1)

# Plotar o dendrograma melhorado
plot(dend, main="Dendrograma do Método Hierárquico Simplificado", xlab="", sub="")

#################################################
# Gráfico 2: Método do Cotovelo
# Determinando o número óptimo de clusters
fviz_nbclust(cluster_data_norm, kmeans, method = "wss") + 
  geom_vline(xintercept = 4, linetype = 2)  # O valor de xintercept deve ser ajustado com base no método do cotovelo

# Gráfico 3: Análise de Silhueta para avaliar a qualidade do agrupamento
# Escolher o número de clusters baseado no método do cotovelo
k <- 4 # Este valor deve ser ajustado conforme necessário
silhouette <- silhouette(cutree(hc, k), dist_matrix)
plot(silhouette, col = 1:k, border = NA)

# Gráfico 4: Gráfico de dispersão dos clusters
# Este passo requer uma redução de dimensionalidade, como PCA, se você tiver mais de duas variáveis
# Aplicando PCA para redução de dimensionalidade
pca <- prcomp(cluster_data_norm)

# Ajustando os clusters com base no PCA
clusters_pca <- cutree(hc, k)

# Visualização dos clusters baseados na PCA
fviz_cluster(list(data = pca$x, cluster = clusters_pca), geom = "point", 
             stand = FALSE, ellipse.type = "norm", 
             main = "Clusters baseados na PCA")

# Para uma visualização ainda mais clara, você pode querer visualizar apenas os dois primeiros componentes principais
fviz_cluster(list(data = pca$x[,1:2], cluster = clusters_pca), geom = "point",
             stand = FALSE, ellipse.type = "norm", 
             main = "Clusters baseados nos dois primeiros componentes da PCA")

#####################################################



# Determinar o número óptimo de clusters usando o método do cotovelo
set.seed(123) # Configurar uma semente para reprodutibilidade
fviz_nbclust(cluster_data_norm, kmeans, method = "wss") +
  geom_vline(xintercept = 4, linetype = 2)  # Este valor pode precisar ser ajustado

# Realizar a análise de clusters K-means com o número óptimo de clusters
# Substitua 4 pelo número apropriado de clusters conforme determinado acima
k <- 4
kmeans_result <- kmeans(cluster_data_norm, centers = k, nstart = 25)

# Visualizar os clusters
fviz_cluster(kmeans_result, data = cluster_data_norm, ellipse.type = "convex") +
  labs(title = "Análise de Cluster K-means")