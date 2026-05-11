import pandas
import logging

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    datefmt='%d-%m-%Y %H-%M-%S',
    handlers=[
        logging.FileHandler('info.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)

data = pandas.read_csv('data.csv')

# Удаление столбцов
delete_column = ['RID', 'yq', 'Series', 'Unit', 'Source']
# print(data['Unit'].nunique()) # Количестов уникальных значений в столбце
data = data.drop(columns=delete_column)
logging.info(f'Удалены столбцы: {delete_column}')
# print(data.dtypes) # Типы данных в столбцах

# Исключение регионов
exclude_region = ['NEW_ZEALAND', 'NORTH_ISLAND', 'SOUTH_ISLAND']
# country_data = data[data['region'].isin(exclude_region)] # Нужны ли эти данные?
data = data[~data['region'].isin(exclude_region)]
logging.info(f'Исключены регионы: {exclude_region}')
# print(data['region'].unique()) # Уникальные значения в столбце

# Расчёт характеристик
stats = data.groupby('region')['value'].agg(['std', 'mean', 'max', 'min', lambda x: x.quantile(0.75)])
stats['range'] = stats['max'] - stats['min'] # Размах
stats['cv'] = (stats['std'] / stats['mean']) * 100 # Коэффициент вариации
stats = stats.rename(columns={'<lambda_0>': 'q3'})
# print('Третий квартиль для всех регионов: ', data['value'].quantile(0.75)) # Расчёт квартиля в общем
print(stats[['std', 'range', 'cv', 'q3', 'min']])

# print(data.head()) # Первые несколько строк