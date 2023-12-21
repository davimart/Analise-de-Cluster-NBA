import pandas as pd
import matplotlib.pyplot as plt
import os

def summary(df,nome_coluna):
    # Contagem de cada tipo de variável na coluna 'TP_STATUS_REDACAO'
    contagem = df[nome_coluna].value_counts()

    # Calcular a porcentagem
    porcentagem = (contagem / len(df)) * 100
    print('Contagem: ',contagem)
    print('Porcentagem: ',porcentagem)

    porcentagem_faltando = (df[nome_coluna].isnull().mean()) * 100
    print('Porcentagem nula: ', porcentagem_faltando)

    print(df[nome_coluna].describe())
  

def imprimir_resumo(df, columns, nome_arquivo, dataset_name):
    # Create a directory to store the exported plots (if it doesn't exist)
    output_dir = f'Imagens_{nome_arquivo}'
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Create a text file to save the descriptions
    with open(f'description_{nome_arquivo}.txt', 'w') as description_file:
        for column in columns:
            if column != 'PLAYER_NAME':
                # Verificar o tipo de variável (numérica ou categórica)
                if df[column].dtype == 'int64' or df[column].dtype == 'float64':
                    # Análise para variáveis numéricas
                    description_file.write(f"Análise da variável '{column}':\n")
                    description_file.write(str(df[column].describe()))  # Medidas de tendência central e dispersão
                    description_file.write('\n\n')
                    df[column].plot(kind='hist', bins=10, title=f'Distribuição de Frequências - {column} ({dataset_name})')
                    plt.xlabel(column)
                    plt.savefig(os.path.join(output_dir, f'hist_{column}_{dataset_name}.png'))  # Save the plot
                    plt.close()  # Close the current plot

                    # Create boxplot
                    ax = df.boxplot(column=column, vert=False)
                    plt.title(f'Box Plot - {column} ({dataset_name})')

                    # Calculate IQR
                    Q1 = df[column].quantile(0.25)
                    Q3 = df[column].quantile(0.75)
                    IQR = Q3 - Q1

                    # Identify outliers based on IQR
                    upper_outliers = df[df[column] > Q3 + 1.5 * IQR]  # Outliers above upper whisker
                    lower_outliers = df[df[column] < Q1 - 1.5 * IQR]  # Outliers below lower whisker

                    # Annotate top outlier
                    if not upper_outliers.empty:
                        top_outlier = upper_outliers.nlargest(1, column)
                        row = top_outlier.iloc[0]
                        ax.annotate(row['PLAYER_NAME'], (row[column], 1), textcoords="offset points", xytext=(0, 10), ha='center')

                    # Annotate bottom outlier
                    if not lower_outliers.empty:
                        bottom_outlier = lower_outliers.nsmallest(1, column)
                        row = bottom_outlier.iloc[0]
                        ax.annotate(row['PLAYER_NAME'], (row[column], 1), textcoords="offset points", xytext=(0, 10), ha='center')

                    # Write outlier names to description file
                    description_file.write(f"\nOutliers for '{column}' (in order from top to bottom):\n")
                    if not upper_outliers.empty:
                        upper_outliers_sorted = upper_outliers.sort_values(by=column, ascending=False)
                        description_file.write('\n'.join(upper_outliers_sorted['PLAYER_NAME'].tolist()))
                        description_file.write('\n')
                    if not lower_outliers.empty:
                        lower_outliers_sorted = lower_outliers.sort_values(by=column, ascending=False)
                        description_file.write('\n'.join(lower_outliers_sorted['PLAYER_NAME'].tolist()))
                        description_file.write('\n')

                    plt.savefig(os.path.join(output_dir, f'boxplot_{column}_{dataset_name}.png'))  # Save the plot
                    plt.close()  # Close the current plot


                elif df[column].dtype == 'object' or df[column].dtype == 'int64':
                    try:
                        # Análise para variáveis categóricas
                        description_file.write(f"Análise da variável '{column}':\n")
                        description_file.write(str(df[column].value_counts()))  # Tabela de distribuição de frequências
                        description_file.write('\n\n')
                        
                        # Calcular e imprimir as porcentagens
                        percentages = df[column].value_counts(normalize=True) * 100
                        description_file.write(f"Porcentagens da variável '{column}':\n")
                        description_file.write(str(percentages))
                        description_file.write('\n\n')
                        
                        # Definindo a ordem desejada para as categorias
                        order = sorted(df[column].unique())

                        # Convertendo a coluna para a categoria ordenada
                        df[column] = pd.Categorical(df[column], categories=order, ordered=True)
                        # Plotar o gráfico de barras ordenado com os valores das porcentagens
                        ax = df[column].value_counts().sort_index().plot(kind='bar', title=f'Distribuição de Frequências - {column} ({dataset_name})')
                        plt.xlabel(column)
                        plt.ylabel('Quantidade')
                        plt.savefig(os.path.join(output_dir, f'bar_{column}_{dataset_name}.png'))  # Save the plot
                        plt.close()  # Close the current plot

                        # Plotar o gráfico de barras das porcentagens com os valores
                        ax = percentages.sort_index().plot(kind='bar', title=f'Porcentagens - {column} ({dataset_name})')
                        plt.xlabel(column)
                        plt.ylabel('Porcentagem')
                        for p in ax.patches:
                            ax.annotate(f'{p.get_height():.2f}%', (p.get_x() + p.get_width() / 2., p.get_height()),
                                        ha='center', va='center', xytext=(0, 10), textcoords='offset points')
                        plt.savefig(os.path.join(output_dir, f'percentage_bar_{column}_{dataset_name}.png'))  # Save the plot
                        plt.close()  # Close the current plot
                    except:
                        print('Erro na coluna: ', column)
                else:
                    print(f"A variável '{column}' não é numérica nem categórica e não pode ser analisada automaticamente.")
