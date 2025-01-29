import matplotlib.pyplot as plt
import pandas as pd
import openpyxl

# Шаг 1: Считываем данные из Excel
file_path = 'Characters.xlsx'  # Путь к файлу Excel
df = pd.read_excel(file_path)

# Шаг 2: Построение графика
# Используем данные из DataFrame
x = df['Вещество']
print('Выберите характеристику, которую вы хотите отобразить на графике:')
print('1 - T плавления, 2 - T кипения, 3 - уд. теплоёмкость в т.с., 4 - уд. теплоемкость в ж.с.')
num = int(input())
if num == 1:
    y = df['T плавления']
if num == 2:
    y = df['T кипения']
if num == 3:
    y = df['Уд. теплоёмкость в т.с.']
if num == 4:
    y = df['Уд. теплоёмкость в ж.с.']
plt.grid(True)
plt.bar(x, y)
plt.show()
