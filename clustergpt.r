# Instale as bibliotecas necessárias se ainda não estiverem instaladas
install.packages(c("dplyr", "ggplot2", "factoextra"))

# Carregue as bibliotecas
library(dplyr)
library(factoextra)

# Carregue os dados
nba_data <- read.csv("cluster.csv")

# Etapa 1: Análise das variáveis e objetos
# Vamos excluir a coluna PLAYER_NAME temporariamente para a análise
nba_data_analytical <- nba_data %>%
  select(-PLAYER_NAME)

# Identificação de outliers (pode personalizar esse passo)
outliers <- boxplot.stats(nba_data_analytical)$out
nba_data_analytical_no_outliers <- nba_data_analytical %>%
  filter_all(all_vars(!. %in% outliers))

# Padronização (normalização z)
nba_data_scaled <- scale(nba_data_analytical_no_outliers)

# Etapa 2: Seleção da medida de distância
dist_matrix <- dist(nba_data_scaled, method = "euclidean")

# Etapa 3: Seleção do algoritmo de agrupamento hierárquico
hclust_model <- hclust(dist_matrix, method = "ward.D2")

# Etapa 4: Escolha da quantidade de agrupamentos
num_clusters <- c(3, 4, 5)
cluster_assignments <- lapply(num_clusters, function(k) cutree(hclust_model, k))

# Etapa 5: Interpretação e validação dos agrupamentos
for (i in seq_along(num_clusters)) {
  cat("Número de clusters:", num_clusters[i], "\n")
  cat("Grupos formados:", cluster_assignments[[i]], "\n\n")
}

# Visualização dendrograma
plot(hclust_model, cex = 0.6, hang = -1, main = "Dendrograma Hierárquico")

# Visualização gráfica dos clusters
fviz_cluster(list(data = nba_data_scaled, cluster = cluster_assignments[[1]]))
