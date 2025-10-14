import pandas as pd

# Lê o arquivo original
df = pd.read_csv("vendas_restaurante_2024_2025.csv")

# Mostra valores únicos antes da limpeza
print("Valores antes da correção:")
print(df['forma_pagamento'].unique())

# Corrige erros de digitação
df['forma_pagamento'] = df['forma_pagamento'].replace({
    'Dinheir': 'Dinheiro',
    'dinheir': 'Dinheiro',
    'Pixx': 'Pix',
    'pix': 'Pix',
    'Credito': 'Crédito',
    'Debito': 'Débito'
})

# Padroniza capitalização
df['forma_pagamento'] = df['forma_pagamento'].str.capitalize()

# Mostra os valores únicos depois da correção
print("\nValores depois da correção:")
print(df['forma_pagamento'].unique())

# Salva o resultado limpo
df.to_csv("vendas_restaurante_tratado.csv", index=False, encoding='utf-8-sig')


print("\n✅ Arquivo tratado salvo com sucesso: vendas_restaurante_tratado.csv")
