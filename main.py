import pandas
import logging

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
data = data.drop(columns=delete_column)
logging.info(f'Удалены столбцы: {delete_column}')

# print(data.dtypes) # Типы данных в столбцах
# print(data['value'].nunique()) # Количестов уникальных значений в столбце

print(data.head()) # Первые несколько строк