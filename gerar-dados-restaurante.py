import pandas as pd
import numpy as np
from faker import Faker
import random
from datetime import datetime, timedelta

fake = Faker('pt_BR')
random.seed(42)

def gerar_vendas(inicio='2023-06-30', fim='2025-06-30'):
    registros = []

    # ===== CARDÁPIOS =====
    pratos_almoco = [
        ('PF Frango Grelhado com Arroz, Feijão e Salada', 24.90),
        ('PF Bife Acebolado com Arroz, Feijão e Fritas', 27.90),
        ('PF File de Peixe com Purê e Salada', 29.90),
        ('PF Carne de Panela com Arroz e Feijão', 26.90),
        ('PF Strogonoff de Frango com Batata Palha', 28.90),
        ('PF Strogonoff de Carne com Batata Palha', 30.90),
        ('PF Lasanha Bolonhesa', 31.90),
        ('PF Parmegiana de Frango', 32.90),
        ('PF Parmegiana de Carne', 34.90),
        ('PF Omelete com Salada e Arroz', 22.90)
    ]

    pizzas = [
        ('Margherita', 38.90),
        ('Calabresa', 42.90),
        ('Frango com Catupiry', 44.90),
        ('Portuguesa', 45.90),
        ('Napolitana', 39.90),
        ('Pepperoni', 46.90),
        ('4 Queijos', 47.90),
        ('Bacon', 43.90),
        ('Vegetariana', 41.90),
        ('Chocolate', 36.90)
    ]
    pesos_pizzas = [14, 18, 15, 12, 8, 14, 9, 6, 3, 7]  

    sobremesas = ['Pudim de leite', 'Mousse de maracujá', 'Mousse de chocolate', 'Picolé / sorvete simples']
    pesos_sobremesa = [45, 30, 15, 10]

    bebidas_lata = ['Coca-Cola', 'Guaraná Antarctica', 'Fanta Laranja', 'Fanta Uva', 'Pepsi', 'Sprite']
    pesos_lata = [40, 25, 10, 8, 12, 5]

    bebidas_2l = ['Coca-Cola', 'Guaraná', 'Pepsi', 'Fanta']
    pesos_2l = [45, 25, 20, 10]

    sucos = ['Laranja', 'Maracujá', 'Acerola', 'Abacaxi com hortelã']
    pesos_suco = [40, 30, 15, 15]

    formas_pgto_lista = ['Crédito', 'Débito', 'Pix', 'Dinheiro', 'Refeição']

    multiplicadores_mes = {1:0.9, 2:0.9, 3:1.0, 4:1.0, 5:1.1, 6:1.2, 7:1.3, 8:1.1, 9:1.0, 10:1.1, 11:1.2, 12:1.4}
    multiplicadores_semana = [0.8, 0.9, 1.0, 1.0, 1.2, 1.5, 1.3]

    prob_masculino = random.uniform(0.45, 0.60)
    prob_feminino = 1 - prob_masculino
    print(f"Distribuição de sexo usada → Masculino: {prob_masculino:.1%} | Feminino: {prob_feminino:.1%}")

    for dia in pd.date_range(start=inicio, end=fim):
        mes = dia.month
        dia_semana = dia.weekday()
        mult_mes = multiplicadores_mes.get(mes, 1.0)
        mult_semana = multiplicadores_semana[dia_semana]
        multiplicador_final = mult_mes * mult_semana * random.uniform(0.9, 1.1)

        # === ALMOÇO ===
        n_dia = int(random.randint(60, 120) * multiplicador_final)
        for _ in range(n_dia):
            hora = random.randint(11, 15)
            minuto = random.randint(0, 59)
            data = datetime(dia.year, dia.month, dia.day, hora, minuto)

            prato_nome, prato_valor = random.choice(pratos_almoco)
            valor = prato_valor

            # 🍮 Sobremesa (25%)
            if random.random() < 0.25:
                sobremesa_nome = random.choices(sobremesas, weights=pesos_sobremesa)[0]
                sobremesa_valor = 5.99 if "Picolé" not in sobremesa_nome else 4.49
            else:
                sobremesa_nome, sobremesa_valor = "Nenhuma", 0
            valor += sobremesa_valor

            # 🥤 Bebida (90%)
            bebida = "Nenhuma"
            tipo_bebida = "Nenhuma"
            if random.random() < 0.9:
                tipo = random.choices(["Lata", "2L", "Suco", "Água", "Refil"], weights=[45, 8, 25, 10, 12])[0]
                tipo_bebida = tipo
                if tipo == "Lata":
                    bebida = random.choices(bebidas_lata, weights=pesos_lata)[0]
                    valor += 6
                elif tipo == "2L":
                    bebida = random.choices(bebidas_2l, weights=pesos_2l)[0]
                    valor += 12
                elif tipo == "Suco":
                    bebida = random.choices(sucos, weights=pesos_suco)[0]
                    valor += 8
                elif tipo == "Refil":
                    bebida = "Refil de Refrigerante"
                    valor += 12.90
                else:
                    bebida = "Água"
                    valor += 4

            pesos_pgto = [
                random.randint(25, 40),
                random.randint(15, 30),
                random.randint(20, 35),
                random.randint(5, 15),
                random.randint(10, 20)
            ]
            forma_pgto = random.choices(formas_pgto_lista, weights=pesos_pgto)[0]

            avaliacao = random.choices([1, 2, 3, 4, 5], weights=[1, 4, 15, 40, 40])[0]
            cancelado = random.random() < (0.01 + random.uniform(-0.005, 0.01))
            sexo = np.random.choice(['Masculino', 'Feminino'], p=[prob_masculino, prob_feminino])

            registros.append({
                'data': data,
                'periodo': 'Dia',
                'cliente_id': fake.random_int(1, 6000),
                'sexo': sexo,
                'tipo_cardapio': 'Prato Executivo',
                'prato': prato_nome,
                'sobremesa': sobremesa_nome,
                'tipo_bebida': tipo_bebida,
                'bebida': bebida,
                'valor_total': round(valor, 2),
                'forma_pagamento': forma_pgto,
                'tempo_preparo': random.randint(15,30),
                'tempo_atendimento': random.randint(5,10),
                'avaliacao': avaliacao,
                'cancelado': cancelado
            })

        # === JANTAR ===
        n_noite = int(random.randint(70, 110) * multiplicador_final)
        for _ in range(n_noite):
            hora = random.randint(18, 23)
            minuto = random.randint(0, 59)
            data = datetime(dia.year, dia.month, dia.day, hora, minuto)

            pizza_nomes = [p[0] for p in pizzas]
            pizza_nome = random.choices(pizza_nomes, weights=pesos_pizzas)[0]
            pizza_valor = next(p[1] for p in pizzas if p[0] == pizza_nome)
            valor = pizza_valor

            # 🥤 Bebida (85%)
            bebida = "Nenhuma"
            tipo_bebida = "Nenhuma"
            if random.random() < 0.85:
                tipo = random.choices(["Lata", "2L", "Suco", "Água", "Refil"], weights=[50, 15, 20, 5, 10])[0]
                tipo_bebida = tipo
                if tipo == "Lata":
                    bebida = random.choices(bebidas_lata, weights=pesos_lata)[0]
                    valor += 6
                elif tipo == "2L":
                    bebida = random.choices(bebidas_2l, weights=pesos_2l)[0]
                    valor += 12
                elif tipo == "Suco":
                    bebida = random.choices(sucos, weights=pesos_suco)[0]
                    valor += 8
                elif tipo == "Refil":
                    bebida = "Refil de Refrigerante"
                    valor += 12.90
                else:
                    bebida = "Água"
                    valor += 4

            # 🍮 Sobremesa (20%)
            if random.random() < 0.2:
                sobremesa_nome = random.choices(sobremesas, weights=pesos_sobremesa)[0]
                sobremesa_valor = 5.99 if "Picolé" not in sobremesa_nome else 4.49
            else:
                sobremesa_nome, sobremesa_valor = "Nenhuma", 0
            valor += sobremesa_valor

            pesos_pgto_noite = [
                random.randint(35, 50),
                random.randint(20, 30),
                random.randint(10, 25),
                random.randint(5, 15),
                random.randint(0, 5)
            ]
            forma_pgto = random.choices(formas_pgto_lista, weights=pesos_pgto_noite)[0]

            avaliacao = random.choices([1, 2, 3, 4, 5], weights=[2, 6, 20, 35, 37])[0]
            cancelado = random.random() < (0.012 + random.uniform(-0.005, 0.008))
            sexo = np.random.choice(['Masculino', 'Feminino'], p=[prob_masculino, prob_feminino])

            registros.append({
                'data': data,
                'periodo': 'Noite',
                'cliente_id': fake.random_int(1, 6000),
                'sexo': sexo,
                'tipo_cardapio': 'Pizza à la carte',
                'prato': pizza_nome,
                'sobremesa': sobremesa_nome,
                'tipo_bebida': tipo_bebida,
                'bebida': bebida,
                'valor_total': round(valor, 2),
                'forma_pagamento': forma_pgto,
                'tempo_preparo': random.randint(20,35),
                'tempo_atendimento': random.randint(5,10),
                'avaliacao': avaliacao,
                'cancelado': cancelado
            })

    df = pd.DataFrame(registros)

    # === Estatística de bebidas ===
    total_refil = (df['tipo_bebida'] == 'Refil').sum()
    total_refrigerante = df['tipo_bebida'].isin(['Lata', '2L']).sum()

    print(f"\nTotal que escolheram REFRIL: {total_refil}")
    print(f"Total que escolheram REFRIGERANTE (Lata/2L): {total_refrigerante}")
    print(f"Total geral de vendas: {len(df)}")

    return df


# === GERAR DADOS E SALVAR ===
df = gerar_vendas()
df.to_csv("vendas_restaurante_realista.csv", index=False, encoding='utf-8-sig')

print(df.shape)
print(df.head(10))
print("\nArquivo 'vendas_restaurante_realista.csv' gerado com sucesso!")
