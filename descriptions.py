import pandas as pd
from functions import *


dataset = 'C:\\Users\\Davi Araujo\\Documents\\GitHub\\Analise-de-Cluster-NBA\\archive\\nba_2016_2017_100.csv'

df = pd.read_csv(dataset, sep=',')

colunas =["PLAYER_NAME", "W", "OFF_RATING", "DEF_RATING", "USG_PCT", "SALARY_MILLIONS", "TWITTER_FOLLOWER_COUNT_MILLIONS"]


imprimir_resumo(df, colunas, 'NBA Social Power','2016-17')

