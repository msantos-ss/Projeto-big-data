import pandas as pd
import os

# Lê o arquivo tratado (com codificação UTF-8)
df = pd.read_csv("vendas_restaurante_tratado.csv", encoding='utf-8')

# Converte a coluna de data para datetime
df['data'] = pd.to_datetime(df['data'], errors='coerce')

# Cria colunas de ano e mês
df['ano'] = df['data'].dt.year
df['mes'] = df['data'].dt.month

# Loop para salvar por ano e mês
for (ano, mes), grupo in df.groupby(['ano', 'mes']):
    pasta = f"dados/vendas/{ano}/{mes:02d}"
    os.makedirs(pasta, exist_ok=True)
    arquivo = f"{pasta}/vendas_{ano}_{mes:02d}.csv"
    
    # Salva com codificação compatível com Excel
    grupo.to_csv(arquivo, index=False, encoding='utf-8-sig')
    
    print(f"✅ Arquivo salvo em: {arquivo}")
