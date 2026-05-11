import pandas
import logging
import matplotlib.pyplot as plt

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
country_data = data[data['region'].isin(exclude_region)]
data = data[~data['region'].isin(exclude_region)]
logging.info(f'Исключены регионы: {exclude_region}')
# print(data['region'].unique()) # Уникальные значения в столбце

# Проверка на наличие пропусков
missing_count = data['value'].isnull().sum()
if missing_count == 0:
    logging.info('Пропусков не найдено')
else:
    logging.warning(f'Обнаружено пропусков {missing_count}')
    data['value'] = data['value'].fillna(data['value'].median())
    logging.info('Пропуски заменены медианой')

# Расчёт характеристик / группировка
stats = data.groupby('region')['value'].agg(['std', 'mean', 'max', 'min', lambda x: x.quantile(0.75)])
stats['range'] = stats['max'] - stats['min'] # Размах
stats['cv'] = (stats['std'] / stats['mean']) * 100 # Коэффициент вариации
stats = stats.rename(columns={'<lambda_0>': 'q3'})
# print('Третий квартиль для всех регионов: ', data['value'].quantile(0.75)) # Расчёт квартиля в общем
print(stats[['std', 'range', 'cv', 'q3', 'min']])

# Три наибольших и наименьших значения
top_3_max = data.nlargest(3, 'value')
top_3_min = data.nsmallest(3, 'value')
print("Тройка наибольших:\n", top_3_max[['region', 'year', 'value']])
print("\nТройка наименьших:\n", top_3_min[['region', 'year', 'value']])

# Проверка гипотезы сезонности
season = data.groupby('Quarter')['value'].mean()
print("Средние значения по кварталам:")
print(season)
max_q = season.idxmax()
min_q = season.idxmin()
if season.max() / season.min() > 1.2:
    print(f"Наблюдается сезонность. Пик выработки приходится на {max_q} квартал.")
else:
    print("Значимой сезонности не обнаружено.")

# Построение графиков
indicator = 'Discharge by Hydrogeneration'
region = 'NEW_ZEALAND'
data_use = country_data

schedule_data = data_use[(data_use['variable'] == indicator) & (data_use['region'] == region)].copy()

window = plt.figure(figsize=(18, 6))
window.canvas.manager.set_window_title(region)

# Линейный
plt.subplot(1, 3, 1)
plt.plot(range(len(schedule_data)), schedule_data['value'], color='blue', marker='o', markersize=2)
plt.title('Линейный график')
plt.grid(True, alpha=0.3)

# Плотность
plt.subplot(1, 3, 2)
schedule_data['value'].plot(kind='kde', color='green') 
plt.title('Плотность распределения')
plt.grid(True, alpha=0.3)

# Кумулятивная сумма
plt.subplot(1, 3, 3)
plt.plot(range(len(schedule_data)), schedule_data['value'].cumsum(), color='orange', linewidth=2)
plt.title('Кумулятивная сумма')
plt.grid(True, alpha=0.3)

plt.tight_layout()
plt.show()

# print(data.head()) # Первые несколько строк