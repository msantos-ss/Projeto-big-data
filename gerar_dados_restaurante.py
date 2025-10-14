import pandas as pd
import numpy as np
from faker import Faker
import random
from datetime import datetime, timedelta

fake = Faker('pt_BR')
random.seed(42)

def gerar_vendas(inicio='2024-01-01', fim='2025-06-30'):
    datas = pd.date_range(start=inicio, end=fim, freq='H')
    registros = []

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

    for dia in pd.date_range(start=inicio, end=fim):
        mes = dia.month
        dia_semana = dia.weekday()  # 0 = segunda
        # Meses de pico: mais movimento
        multiplicador = 1.3 if mes in [10, 11, 12] else 1.0

        # Almoço
        n_dia = int(random.randint(80, 120) * multiplicador)
        for _ in range(n_dia):
            hora = random.randint(11, 15)
            minuto = random.randint(0, 59)
            data = datetime(dia.year, dia.month, dia.day, hora, minuto)

            valor = 26.0
            sobremesa_nome, sobremesa_valor = random.choice(sobremesas) if random.random() < 0.3 else ("Nenhuma", 0)
            bebida = None
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
            valor += sobremesa_valor

            registros.append({
                'data': data,
                'periodo': 'Dia',
                'cliente_id': fake.random_int(1, 6000),
                'tipo_cardapio': 'Self-service',
                'prato': 'Self-service',
                'sobremesa': sobremesa_nome,
                'bebida': bebida or "Nenhuma",
                'valor_total': round(valor, 2),
                'forma_pagamento': random.choices(formas_pgto, weights=[35,25,20,10,10])[0],
                'tempo_preparo': random.randint(30,40),
                'tempo_atendimento': random.randint(5,10),
                'avaliacao': random.choices([3,4,5,5,4,5], weights=[5,20,50,15,10,0])[0],
                'cancelado': random.random() < 0.015
            })

        # Jantar (rodízio)
        n_noite = int(random.randint(80, 100) * multiplicador)
        for _ in range(n_noite):
            hora = random.randint(18, 23)
            minuto = random.randint(0, 59)
            data = datetime(dia.year, dia.month, dia.day, hora, minuto)

            base = 49.90 if dia_semana < 5 else 59.90
            valor = base
            if random.random() < 0.4:
                valor += 12.90  # refil

            # Combo promocional (ex: dia comemorativo)
            if mes in [5, 10, 12] and random.random() < 0.05:
                valor = 69.90

            registros.append({
                'data': data,
                'periodo': 'Noite',
                'cliente_id': fake.random_int(1, 6000),
                'tipo_cardapio': 'Rodízio',
                'prato': 'Rodízio de pizzas',
                'sobremesa': 'Nenhuma',
                'bebida': random.choice(bebidas_lata + sucos),
                'valor_total': round(valor, 2),
                'forma_pagamento': random.choices(formas_pgto, weights=[35,25,20,10,10])[0],
                'tempo_preparo': random.randint(30,40),
                'tempo_atendimento': random.randint(5,10),
                'avaliacao': random.choices([3,4,5,5,4,5], weights=[5,20,50,15,10,0])[0],
                'cancelado': random.random() < 0.015
            })

    df = pd.DataFrame(registros)
    return df

df = gerar_vendas()
df.to_csv("vendas_restaurante_2024_2025.csv", index=False)
print(df.shape)
print(df.head())
