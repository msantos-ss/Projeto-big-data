import pandas as pd
import numpy as np
from faker import Faker
import random
from datetime import datetime, timedelta

fake = Faker('pt_BR')
random.seed(42)

def gerar_vendas(inicio='2023-06-30', fim='2025-06-30'):
    registros = []

    # Cardápios
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

    sobremesas = [
        ('Pudim de leite', 5.99),
        ('Mousse de maracujá', 5.99),
        ('Mousse de chocolate', 5.99),
        ('Picolé / sorvete simples', 4.49)
    ]

    bebidas_lata = ['Coca-Cola', 'Guaraná Antarctica', 'Fanta Laranja', 'Fanta Uva', 'Pepsi', 'Sprite']
    bebidas_2l = ['Coca-Cola', 'Guaraná', 'Pepsi', 'Fanta']
    sucos = ['Laranja', 'Maracujá', 'Acerola', 'Abacaxi com hortelã']
    formas_pgto = ['Crédito', 'Débito', 'Pix', 'Dinheiro', 'Refeição']

    # Probabilidades de sexo (definidas aleatoriamente a cada execução)
    prob_masculino = random.uniform(0.45, 0.60)
    prob_feminino = 1 - prob_masculino
    print(f"Distribuição de sexo usada → Masculino: {prob_masculino:.1%} | Feminino: {prob_feminino:.1%}")

    for dia in pd.date_range(start=inicio, end=fim):
        mes = dia.month
        dia_semana = dia.weekday()  # 0 = segunda
        multiplicador = 1.3 if mes in [10, 11, 12] else 1.0  # Meses de pico

        # ===== ALMOÇO =====
        n_dia = int(random.randint(80, 120) * multiplicador)
        for _ in range(n_dia):
            hora = random.randint(11, 15)
            minuto = random.randint(0, 59)
            data = datetime(dia.year, dia.month, dia.day, hora, minuto)

            prato_nome, prato_valor = random.choice(pratos_almoco)
            valor = prato_valor

            # Sobremesa (30% das vezes)
            sobremesa_nome, sobremesa_valor = random.choice(sobremesas) if random.random() < 0.3 else ("Nenhuma", 0)
            valor += sobremesa_valor

            # Bebida (90% das vezes)
            bebida = "Nenhuma"
            if random.random() < 0.9:
                tipo = random.choices(["Lata", "2L", "Suco", "Água"], weights=[50, 10, 30, 10])[0]
                if tipo == "Lata":
                    bebida = random.choice(bebidas_lata)
                    valor += 6
                elif tipo == "2L":
                    bebida = random.choice(bebidas_2l)
                    valor += 12
                elif tipo == "Suco":
                    bebida = random.choice(sucos)
                    valor += 8
                else:
                    bebida = "Água"
                    valor += 4

            sexo = np.random.choice(['Masculino', 'Feminino'], p=[prob_masculino, prob_feminino])

            registros.append({
                'data': data,
                'periodo': 'Dia',
                'cliente_id': fake.random_int(1, 6000),
                'sexo': sexo,
                'tipo_cardapio': 'Prato Executivo',
                'prato': prato_nome,
                'sobremesa': sobremesa_nome,
                'bebida': bebida,
                'valor_total': round(valor, 2),
                'forma_pagamento': random.choices(formas_pgto, weights=[35,25,20,10,10])[0],
                'tempo_preparo': random.randint(15,30),
                'tempo_atendimento': random.randint(5,10),
                'avaliacao': random.choices([3,4,5,5,4,5], weights=[5,20,50,15,10,0])[0],
                'cancelado': random.random() < 0.015
            })

        # ===== JANTAR (PIZZAS) =====
        n_noite = int(random.randint(80, 100) * multiplicador)
        for _ in range(n_noite):
            hora = random.randint(18, 23)
            minuto = random.randint(0, 59)
            data = datetime(dia.year, dia.month, dia.day, hora, minuto)

            pizza_nome, pizza_valor = random.choice(pizzas)
            valor = pizza_valor

            # Bebida (85% das vezes)
            bebida = "Nenhuma"
            if random.random() < 0.85:
                tipo = random.choices(["Lata", "2L", "Suco", "Água"], weights=[60, 10, 25, 5])[0]
                if tipo == "Lata":
                    bebida = random.choice(bebidas_lata)
                    valor += 6
                elif tipo == "2L":
                    bebida = random.choice(bebidas_2l)
                    valor += 12
                elif tipo == "Suco":
                    bebida = random.choice(sucos)
                    valor += 8
                else:
                    bebida = "Água"
                    valor += 4

            # Sobremesa (25% das vezes)
            sobremesa_nome, sobremesa_valor = random.choice(sobremesas) if random.random() < 0.25 else ("Nenhuma", 0)
            valor += sobremesa_valor

            sexo = np.random.choice(['Masculino', 'Feminino'], p=[prob_masculino, prob_feminino])

            registros.append({
                'data': data,
                'periodo': 'Noite',
                'cliente_id': fake.random_int(1, 6000),
                'sexo': sexo,
                'tipo_cardapio': 'Pizza à la carte',
                'prato': pizza_nome,
                'sobremesa': sobremesa_nome,
                'bebida': bebida,
                'valor_total': round(valor, 2),
                'forma_pagamento': random.choices(formas_pgto, weights=[35,25,20,10,10])[0],
                'tempo_preparo': random.randint(20,35),
                'tempo_atendimento': random.randint(5,10),
                'avaliacao': random.choices([3,4,5,5,4,5], weights=[5,20,50,15,10,0])[0],
                'cancelado': random.random() < 0.015
            })

    df = pd.DataFrame(registros)
    return df


# === Gerar os dados e salvar ===
df = gerar_vendas()
df.to_csv("vendas_restaurante_2024_2025.csv", index=False, encoding='utf-8-sig')

print(df.shape)
print(df.head(10))
