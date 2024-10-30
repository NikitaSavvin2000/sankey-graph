import pandas as pd
import svgwrite

import cairosvg


cluster_colors = {
    0: '#FFB3BA',
    1: '#FFDFBA',
    2: '#FFFFBA',
    3: '#BAFFC9',
    4: '#BAE1FF',
    5: '#FFC3A0',
    6: '#FF677D',
    7: '#D4A5A5',
    8: '#392F5A',
    9: '#F6AB6C',
    10: '#F6AB6C',
}


colors_rgb = {
    0: (240, 50, 230),    # #F032E6
    1: (70, 153, 144),    # #469990
    2: (230, 25, 75),     # #E6194B
    3: (245, 130, 49),    # #F58231
    4: (191, 239, 69),    # #BFEF45
    5: (60, 180, 75),     # #3CB44B
    6: (66, 212, 244),    # #42D4F4
    7: (67, 99, 216),     # #4363D8
    8: (154, 99, 36),     # #9A6324
    9: (169, 169, 169),    # #A9A9A9
    10: (145, 30, 180),    # #911EB4
    11: (51, 51, 145),     # #333391
    12: (255, 225, 25),    # #FFE119
    13: (128, 128, 0),     # #808000
    14: (170, 255, 195),   # #AAFFC3
    15: (220, 190, 255),   # #DCBEFF
    16: (250, 190, 212),   # #FABED4
    17: (255, 216, 177),    # #FFD8B1
    18: (255, 250, 200)     # #FFFAC8
}

colors_dict = {
    0: '#F032E6',
    1: '#469990',
    2: '#E6194B',
    3: '#F58231',
    4: '#BFEF45',
    5: '#3CB44B',
    6: '#42D4F4',
    7: '#4363D8',
    8: '#9A6324',
    9: '#A9A9A9',
    10: '#911EB4',
    11: '#333391',
    12: '#FFE119',
    13: '#808000',
    14: '#AAFFC3',
    15: '#DCBEFF',
    16: '#FABED4',
    17: '#FFD8B1',
    18: '#FFFAC8'
}


df = pd.read_csv('/Users/nikitasavvin/Desktop/HSE_work/sankey-graph/df_sankey.csv')
df = df[['year', 'term', 'cluster', "cluster_name"]]



cluster_counts = df.groupby(['year', 'cluster']).size().reset_index(name='term_count')

# Отсортируем кластеры по количеству термов в каждом year
cluster_counts = cluster_counts.sort_values(['year', 'term_count'], ascending=[True, False])

# Создадим новый номер кластера
cluster_counts['new_cluster'] = cluster_counts.groupby('year').cumcount()

# Объединим с оригинальным DataFrame, чтобы получить новый номер кластера
df = df.merge(cluster_counts[['year', 'cluster', 'new_cluster']], on=['year', 'cluster'], how='left')

df = df.drop(columns=['cluster'])
# Переименуем колонку cluster
df.rename(columns={'new_cluster': 'cluster'}, inplace=True)



df['unique_cluster_name'] = df.apply(lambda row: f"{row['year']} {row['cluster']}", axis=1)


min_year = min(df["year"])
max_year = max(df["year"])

min_cluster = min(df["cluster"])
max_cluster = max(df["cluster"])


years = list(range(min_year, max_year+1))
clusters = list(range(min_cluster, max_cluster+1))


# Создание SVG-документа с использованием размера экрана
# width = 1400  # Ширина графика
# height = 800  # Высота графика
# padding_y = 50
# padding_x_right = 120
# padding_x_left = 70

def normalize_dict_values(couples, x, y):
    # Получаем минимальное и максимальное значения
    min_value = min(couples.values())
    max_value = max(couples.values())

    # Нормализуем значения
    normalized_couples = {
        key: x + ((value - min_value) * (y - x)) / (max_value - min_value)
        for key, value in couples.items()
    }

    return normalized_couples


width = 1400  # Ширина графика
height = 800  # Высота графика
padding_y = 50
padding_top = 10
padding_bottom = -110


padding_x_right = 100
padding_x_left = -650


node_width = 20  # Фиксированная ширина узлов
min_node_height = 30  # Минимальная высота узла (для минимального размера)

# Создаем SVG-документ
svg_file = 'sankey_diagram.svg'
dwg = svgwrite.Drawing(svg_file, profile='full', size=(width, height),)

# Добавляем белый фон
dwg.add(dwg.rect(insert=(-820, -220), size=(2000, 1600), fill='white'))

dwg.add(dwg.image('/Users/nikitasavvin/Desktop/HSE_work/sankey-graph/iFORA logo 2.svg', insert=(-680, 745), size=(105, 60)))



text = "Источник: Система интеллектуального анализа больших данных IFORA (правообладатель - ИСИЭЗ НИУ ВШЭ)"


dwg.add(dwg.text(text, insert=(-280, 795),
                 fill='gray',  # Цвет шрифта
                 font_size='18px',
                 font_family='Arial',
                 font_style='italic',  # Наклон
                 text_anchor="start"))



fixed_padding_between_clusters = 5  # Фиксированный отступ между столбиками

term_counts = df.groupby(['year', 'cluster', 'cluster_name']).size().reset_index(name='count')

count_unique_cluster = len(term_counts["cluster"].unique())

term_counts.to_csv('/Users/nikitasavvin/Desktop/HSE_work/sankey-graph/term_counts.csv')

total_term_counts = term_counts.groupby('year')['count'].sum().to_dict()


# Общая высота, доступная для всех столбиков (без верхнего и нижнего отступа)
available_height = height - padding_top+padding_bottom - count_unique_cluster * fixed_padding_between_clusters

# Определение позиций столбиков
node_positions = {}

# Параметры графика
total_height = available_height  # Доступная высота графика



for year in years:

    cluster_count_dict = term_counts.loc[term_counts['year'] == year, ['cluster', 'count']].set_index('cluster')[
        'count'].to_dict()



    total_count = term_counts.loc[term_counts['year'] == year, 'count'].sum()
    cluster_proportion_dict = {}
    if total_count > 0:
        for _, row in term_counts.loc[term_counts['year'] == year].iterrows():
            cluster = row['cluster']
            count = row['count']
            cluster_proportion_dict[cluster] = (count / total_count) * available_height

    total_sum = sum(cluster_proportion_dict.values())

    for cluster, value in cluster_proportion_dict.items():
        if value < min_node_height:
            cluster_proportion_dict[cluster] = min_node_height

    total_sum = sum(cluster_proportion_dict.values())

    extra_height = available_height - total_sum

    if extra_height < 0:
        # Находим сумму значений, превышающих min_node_height
        total_above_min = sum(value for value in cluster_proportion_dict.values())

        for cluster in cluster_proportion_dict:
            value = cluster_proportion_dict[cluster]
            proportion = value / total_above_min
            decrease = proportion * extra_height  # Умножаем на -1, чтобы отнять

            cluster_proportion_dict[cluster] += decrease  # Обновляем значение

    total_terms_in_year = total_term_counts.get(year, 0)

    # y0 = padding_y
    y0 = padding_top

    for cluster in clusters:

        count = term_counts[(term_counts['year'] == year) & (term_counts['cluster'] == cluster)]['count'].values
        cluster_name = term_counts[(term_counts['year'] == year) & (term_counts['cluster'] == cluster)]['cluster_name'].values
        cluster_name = str(cluster_name[0])

        count = count[0] if count.size > 0 else 0
        node_height = cluster_proportion_dict[cluster]

        # Применяем минимальную высоту для столбика
        node_height = max(node_height, min_node_height)
        y1 = y0 + node_height

        # Позиция по X (равномерно распределяем по годам)
        x = padding_x_left + (year - min_year) * (width - 2 * padding_x_right) / (len(years) - 1)

        # Сохраняем позиции y0 и y1 для текущего столбика
        node_positions[f'{year} {cluster}'] = [cluster_name, (x, y0, y1)]

        y0 = y1 + fixed_padding_between_clusters


    dwg.add(dwg.text(year, insert=(x + -25, y1 + 50), fill='black', font_size='34px'))


def add_node(name, x, y0, y1, color):
    height = y1 - y0  # Вычисляем высоту столбика
    dwg.add(dwg.rect(insert=(x, y0), size=(node_width, height), fill=color, opacity=0.5))

    # Проверяем длину имени
    if len(name) > 18:
        # Находим последний пробел в первых 18 символах
        last_space_index = name.rfind(' ', 0, 18)

        if last_space_index == -1:  # Если пробел не найден, берем первые 18 символов
            name1 = name[:18]
            name2 = name[18:]
        else:
            name1 = name[:last_space_index]  # Первая строка (до последнего пробела)
            name2 = name[last_space_index + 1:]  # Вторая строка (после пробела)

        # Позиции для текста
        text_x = x + node_width + 10  # Смещаем текст немного вправо от узла
        text_y1 = y0 + height / 2 - 8  # Центрируем первую строку
        text_y2 = y0 + height / 2 + 8   # Центрируем вторую строку

        # Добавляем обе строки текста
        dwg.add(dwg.text(name1, insert=(text_x, text_y1), fill='black', font_size='12px', font_family='Arial', text_anchor="start"))
        dwg.add(dwg.text(name2, insert=(text_x, text_y2), fill='black', font_size='12px', font_family='Arial', text_anchor="start"))
    else:
        # Позиции для текста, если имя меньше или равно 18 символам
        text_x = x + node_width + 10  # Смещаем текст немного вправо от узла
        text_y = y0 + height / 2 + 5   # Центрируем текст по высоте узла

        # Добавляем текст
        dwg.add(dwg.text(name, insert=(text_x, text_y), fill='black', font_size='12px', font_family='Arial', text_anchor="start"))




for node, values in node_positions.items():

    node = node.split(' ')
    # Извлекаем номер кластера из имени узла (если имя имеет формат 'year CLUSTER cluster_number')
    cluster_number = int(node[1])
    cluster_name = values[0]  # Получаем номер кластера из имени
    cluster_color = colors_rgb.get(cluster_number, (0, 0, 0))  # Используем белый как запасной вариант
    cluster_color = svgwrite.utils.rgb(cluster_color[0], cluster_color[1], cluster_color[2])
    (x, y0, y1) = values[1]
    add_node(cluster_name, x, y0, y1, cluster_color)


# Создание перетоков
flow_data = []

for term in df['term'].unique():
    term_data = df[df['term'] == term].sort_values('year')
    for i in range(len(term_data) - 1):
        current_year = term_data.iloc[i]['year']
        next_year = term_data.iloc[i + 1]['year']

        if next_year - current_year == 1:  # Переход только на следующий год
            source_node = f"{term_data.iloc[i]['cluster_name']}"
            target_node = f"{term_data.iloc[i + 1]['cluster_name']}"
            flow_data.append((source_node, target_node))


couples = []
for year in years[:-1]:
    df_cur_year = df[df["year"] == year]
    df_next_year = df[df["year"] == year+1]
    count_terms = 0
    for term in df_cur_year['term'].unique():
        term_unique_cluster_cur = df_cur_year[df_cur_year["term"] == term]["unique_cluster_name"].values
        term_unique_cluster_next = df_next_year[df_next_year["term"] == term]["unique_cluster_name"].values

        if term_unique_cluster_next:
            couples.append([term_unique_cluster_cur, term_unique_cluster_next])

from collections import defaultdict

count_dict = defaultdict(int)

for sublist in couples:
    tuple_key = tuple(tuple(item) for item in sublist)
    count_dict[tuple_key] += 1

couples = dict(count_dict)

couples = normalize_dict_values(couples, 2, 15)


def add_flow(source, target, value, color_start, color_end):
    x0, y0, node_height0 = node_positions[source][1]
    x1, y1, node_height1 = node_positions[target][1]

    source_center_y = y0 + (node_height0 - y0) / 2
    target_center_y = y1 + (node_height1 - y1) / 2

    # Определяем точки для кривой Безье
    control_x = (x0 + x1) / 2  # Опорная точка по X между двумя узлами
    control_y0 = source_center_y  # Начало кривой в центре исходного узла
    control_y1 = target_center_y  # Конец кривой в центре целевого узла

    source_id = source.replace(' ', '_')
    target_id = target.replace(' ', '_')  # Исправляем target_id на target вместо source

    # Создаем уникальный идентификатор градиента для каждого потока
    id = f'{source_id}_{target_id}_{value}'  # добавляем значение или другой уникальный параметр

    # Создаем линейный градиент
    gradient = dwg.defs.add(dwg.linearGradient(id=id, start=('0%', '0%'), end=('100%', '0%')))

    # Добавляем остановки цвета с прозрачност
    gradient.add_stop_color(0, color_start, opacity=0.4)  # Начальный цвет
    gradient.add_stop_color(1, color_end, opacity=0.4)  # Конечный цвет

    # Добавляем кривую Безье с градиентным цветом
    dwg.add(dwg.path(
        d=f'M {x0 + node_width}, {control_y0} C {control_x}, {control_y0} {control_x}, {control_y1} {x1}, {control_y1}',
        stroke=f'url(#{id})',  # Применяем уникальный градиент
        stroke_width=value, fill='none'
    ))


#
# # # Добавляем потоки в SVG
for key, value in couples.items():

    source = key[0][0]
    target = key[1][0]
    width = value

    cluster_source = df[df["unique_cluster_name"] == source]['cluster'].iloc[0]
    cluster_target = df[df["unique_cluster_name"] == target]['cluster'].iloc[0]
    cluster_source_name = df[df["unique_cluster_name"] == source]['cluster_name'].iloc[0]
    cluster_target_name = df[df["unique_cluster_name"] == target]['cluster_name'].iloc[0]


    color_start = colors_dict[cluster_source]
    color_end = colors_dict[cluster_target]

    add_flow(source, target, value, color_start, color_end)



# Установка атрибутов viewBox для адаптивного отображения
dwg['viewBox'] = f'0 0 {width} {height}'

# Сохраняем SVG файл
dwg.save()

png_file = 'sankey_diagram.png'
# cairosvg.svg2png(url=svg_file, write_to=png_file, background_color='white')


svg_string = dwg.tostring()

# Конвертация SVG в PNG
# cairosvg.svg2png(bytestring=svg_string, write_to='output.png')
cairosvg.svg2png(bytestring=svg_string, write_to='output4.png', dpi=10)  # Замените 300 на нужное значение

print("Sankey диаграмма сохранена в sankey_diagram.svg")
