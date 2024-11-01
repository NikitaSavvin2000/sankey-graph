import pandas as pd
import svgwrite

import cairosvg
import svgwrite
import base64
from collections import defaultdict

colors_dict = {
    0: '#800000',
    1: '#F032E6',
    2: '#469990',
    3: '#E6194B',
    4: '#F58231',
    5: '#BFEF45',
    6: '#3CB44B',
    7: '#42D4F4',
    8: '#4363D8',
    9: '#9A6324',
    10: '#A9A9A9',
    11: '#911EB4',
    12: '#333391',
    13: '#FFE119',
    14: '#808000',
    15: '#AAFFC3',
    16: '#DCBEFF',
    17: '#FABED4',
    18: '#FFD8B1',
    19: '#FFFAC8'
}


def prepare_visualization_params(df):
    df = df[['year', 'term', 'cluster', "cluster_name"]]

    cluster_counts = df.groupby(['year', 'cluster']).size().reset_index(name='term_count')

    cluster_counts = cluster_counts.sort_values(['year', 'term_count'], ascending=[True, False])

    cluster_counts['new_cluster'] = cluster_counts.groupby('year').cumcount()

    df = df.merge(cluster_counts[['year', 'cluster', 'new_cluster']], on=['year', 'cluster'], how='left')

    df = df.drop(columns=['cluster'])

    df.rename(columns={'new_cluster': 'cluster'}, inplace=True)

    df['unique_cluster_name'] = df.apply(lambda row: f"{row['year']} {row['cluster']}", axis=1)

    min_year = min(df["year"])
    max_year = max(df["year"])

    min_cluster = min(df["cluster"])
    max_cluster = max(df["cluster"])

    years = list(range(min_year, max_year + 1))
    clusters = list(range(min_cluster, max_cluster + 1))

    term_counts = df.groupby(['year', 'cluster', 'cluster_name']).size().reset_index(name='count')

    count_unique_cluster = len(term_counts["cluster"].unique())

    total_term_counts = term_counts.groupby('year')['count'].sum().to_dict()


    horizontal_distance_between_nodes = ((width + padding_x_right) - node_width * (len(years))) / (len(years))

    available_height = height - padding_top + padding_bottom - count_unique_cluster * fixed_padding_between_clusters

    horizontal_distance_between_columns = horizontal_distance_between_nodes - 2 * node_width

    return df, cluster_counts, min_year, max_year, min_cluster, max_cluster, years, clusters, count_unique_cluster, total_term_counts, term_counts, horizontal_distance_between_nodes, available_height, horizontal_distance_between_columns


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
    gradient.add_stop_color(0, color_start, opacity=0.3)  # Начальный цвет
    gradient.add_stop_color(1, color_end, opacity=0.3)  # Конечный цвет

    # Добавляем кривую Безье с градиентным цветом
    dwg.add(dwg.path(
        d=f'M {x0 + node_width}, {control_y0} C {control_x}, {control_y0} {control_x}, {control_y1} {x1}, {control_y1}',
        stroke=f'url(#{id})',  # Применяем уникальный градиент
        stroke_width=value, fill='none'
    ))

#
# # # Добавляем потоки в SVG
def draw_flows():
    for key, value in couples.items():
        source = key[0][0]
        target = key[1][0]

        cluster_source = df[df["unique_cluster_name"] == source]['cluster'].iloc[0]
        cluster_target = df[df["unique_cluster_name"] == target]['cluster'].iloc[0]

        color_start = colors_dict[cluster_source]
        color_end = colors_dict[cluster_target]

        add_flow(source, target, value, color_start, color_end)


def draw_nodes():
    for node, values in node_positions.items():
        node = node.split(' ')
        cluster_number = int(node[1])
        cluster_name = values[0]
        cluster_color = colors_dict.get(cluster_number)
        (x, y0, y1) = values[1]
        add_node(cluster_name, x, y0, y1, cluster_color, dwg, horizontal_distance_between_columns)


def normalize_width_flow(couples, x, y):
    # Получаем минимальное и максимальное значения
    min_value = min(couples.values())
    max_value = max(couples.values())

    # Нормализуем значения
    normalized_couples = {
        key: x + ((value - min_value) * (y - x)) / (max_value - min_value)
        for key, value in couples.items()
    }

    return normalized_couples


def create_couples(df, years):
    couples = []

    for year in years[:-1]:
        df_cur_year = df[df["year"] == year]
        df_next_year = df[df["year"] == year + 1]

        for term in df_cur_year['term'].unique():
            term_unique_cluster_cur = df_cur_year[df_cur_year["term"] == term]["unique_cluster_name"].values
            term_unique_cluster_next = df_next_year[df_next_year["term"] == term]["unique_cluster_name"].values

            if term_unique_cluster_next.size > 0:
                couples.append([term_unique_cluster_cur, term_unique_cluster_next])

    count_dict = defaultdict(int)

    for sublist in couples:
        tuple_key = tuple(tuple(item) for item in sublist)
        count_dict[tuple_key] += 1

    couples = dict(count_dict)

    couples = normalize_width_flow(couples, 2, 15)

    return couples


def create_flows():
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
    return flow_data


def add_node(name, x, y0, y1, color, dwg, horizontal_distance_between_columns):
    height = y1 - y0  # Вычисляем высоту столбика
    dwg.add(dwg.rect(insert=(x, y0), size=(node_width, height), fill=color, opacity=0.9))

    # Определяем допустимую ширину текста для узлов справа
    max_text_width = horizontal_distance_between_columns - (node_width)

    # Изначальный размер шрифта
    font_size = 14
    max_lines = 2  # Максимальное количество строк

    # Функция для измерения ширины текста (упрощенная, требует библиотеку для точных измерений)
    def text_width(text, font_size):
        return font_size * 0.6 * len(text)  # Примерная ширина символов

    # Разбиваем текст по словам
    words = name.split()
    lines = []
    current_line = ""

    # Формируем строки текста
    for word in words:
        # Проверяем, уместится ли текущее слово в строке
        if text_width(current_line + " " + word, font_size) <= max_text_width:
            current_line += (word if not current_line else " " + word)
        else:
            if current_line:
                lines.append(current_line)
            current_line = word
            if len(lines) >= max_lines:
                break

    # Добавляем последнюю строку
    if current_line:
        lines.append(current_line)

    # Проверяем, помещается ли текст в две строки
    while len(lines) > max_lines or any(text_width(line, font_size) > max_text_width for line in lines):
        font_size -= 1  # Уменьшаем шрифт
        lines = []
        current_line = ""

        # Формируем строки текста заново с новым размером шрифта
        for word in words:
            if text_width(current_line + " " + word, font_size) <= max_text_width:
                current_line += (word if not current_line else " " + word)
            else:
                if current_line:
                    lines.append(current_line)
                current_line = word
                if len(lines) >= max_lines:
                    break

        if current_line:
            lines.append(current_line)

    # Позиции для текста
    text_x = x + node_width + 10
    text_y_start = y0 + height / 2 - (font_size + 2) * (len(lines) - 1) / 2  # Центрируем по вертикали

    # Добавляем строки текста
    for i, line in enumerate(lines[:max_lines]):
        text_y = text_y_start + i * (font_size + 2)  # Смещение каждой строки
        dwg.add(dwg.text(line, insert=(text_x, text_y), fill='black', font_size=f'{font_size}px', font_family='Arial',
                         text_anchor="start"))


def create_nodes_positions():
    node_positions = {}
    years_text = {}
    for year in years:
        # Определяем начальную позицию по X для каждого года
        x_year_start = padding_x_left + (year - min_year) * horizontal_distance_between_nodes
        x = x_year_start  # Начальная позиция X для текущего года

        # Вычисление пропорций и высот
        cluster_count_dict = term_counts.loc[term_counts['year'] == year, ['cluster', 'count']].set_index('cluster')[
            'count'].to_dict()
        total_count = term_counts.loc[term_counts['year'] == year, 'count'].sum()

        cluster_proportion_dict = {}
        if total_count > 0:
            for _, row in term_counts.loc[term_counts['year'] == year].iterrows():
                cluster = row['cluster']
                count = row['count']
                cluster_proportion_dict[cluster] = (count / total_count) * available_height

        # Применение минимальной высоты к кластерам
        for cluster, value in cluster_proportion_dict.items():
            if value < min_node_height:
                cluster_proportion_dict[cluster] = min_node_height

        # Высчитываем разницу, чтобы распределить оставшуюся высоту
        total_sum = sum(cluster_proportion_dict.values())
        extra_height = available_height - total_sum

        if extra_height < 0:
            total_above_min = sum(value for value in cluster_proportion_dict.values())
            for cluster in cluster_proportion_dict:
                value = cluster_proportion_dict[cluster]
                proportion = value / total_above_min
                decrease = proportion * extra_height
                cluster_proportion_dict[cluster] += decrease

        # Рисуем кластеры
        y0 = padding_top
        for cluster in clusters:
            count = term_counts[(term_counts['year'] == year) & (term_counts['cluster'] == cluster)]['count'].values
            cluster_name = term_counts[(term_counts['year'] == year) & (term_counts['cluster'] == cluster)][
                'cluster_name'].values
            cluster_name = str(cluster_name[0]) if cluster_name.size > 0 else f"Cluster {cluster}"

            count = count[0] if count.size > 0 else 0
            node_height = cluster_proportion_dict.get(cluster, min_node_height)
            y1 = y0 + node_height

            # Сохраняем позиции для текущего столбика
            node_positions[f'{year} {cluster}'] = [cluster_name, (x, y0, y1)]

            # Смещаем y0 для следующего кластера
            y0 = y1 + fixed_padding_between_clusters

        # Отображаем год под колонками
        # dwg.add(dwg.text(year, insert=(x_year_start - 15, y1 + 35), fill='black', font_size='24px', font_family='Arial'))
        years_text[year] = [x_year_start, y1]

    return node_positions, years_text


def draw_years(years_text):
    for key, values in years_text.items():
        dwg.add(
            dwg.text(key, insert=(values[0] - 15, values[1] + 35), fill='black', font_size='24px', font_family='Arial'))


def draw_logos():
    # Читаем изображение и кодируем его в Base64
    with open('/Users/nikitasavvin/Desktop/HSE_work/sankey-graph/iFORA logo 2.svg', 'rb') as image_file:
        encoded_image = base64.b64encode(image_file.read()).decode('utf-8')

    data_uri = f"data:image/svg+xml;base64,{encoded_image}"
    dwg.add(dwg.image(href=data_uri, insert=(10, 790), size=(105, 60)))

    text = "Источник: Система интеллектуального анализа больших данных iFORA (правообладатель — ИСИЭЗ НИУ ВШЭ)"

    dwg.add(dwg.text(text, insert=(423, 845),
                     fill='gray',  # Цвет шрифта
                     font_size='18px',
                     font_family='Arial',
                     font_style='italic',  # Наклон
                     text_anchor="start"))

def draw_sankey_map(df):
    svg_file = 'sankey_diagram.svg'
    dwg = svgwrite.Drawing(svg_file, profile='full', size=(width, height), )

    # Добавляем белый фон
    dwg.add(dwg.rect(insert=(-820, -220), size=(2000, 1600), fill='white'))



    (df, cluster_counts, min_year, max_year, min_cluster, max_cluster, years, clusters, count_unique_cluster,
     total_term_counts, term_counts, horizontal_distance_between_nodes, available_height,
     horizontal_distance_between_columns) = prepare_visualization_params(df)

    node_positions, years_text = create_nodes_positions(years)

    draw_years(years_text)

    flow_data = create_flows()

    couples = create_couples(df, years)

    draw_flows()

    draw_nodes()

    draw_logos()

    dwg['viewBox'] = f'0 0 {width} {height}'

    # Сохраняем SVG файл
    dwg.save()

    png_file = 'sankey_diagram.png'

    svg_string = dwg.tostring()

    # Конвертация SVG в PNG
    cairosvg.svg2png(bytestring=svg_string, write_to='output4.png', dpi=10)  # Замените 300 на нужное значение

    print("Sankey диаграмма сохранена в sankey_diagram.svg")



df = pd.read_csv('/Users/nikitasavvin/Desktop/HSE_work/ifora_core/experiments/df_sankey_дорожные карты.csv')

width = 1400  # Ширина графика
height = 850  # Высота графика
padding_y = 50
padding_top = 10
padding_bottom = -120

padding_x_right = 50
padding_x_left = 50

node_width = 20  # Фиксированная ширина узлов
min_node_height = 30  # Минимальная высота узла (для минимального размера)
fixed_padding_between_clusters = 5



svg_file = 'sankey_diagram.svg'
dwg = svgwrite.Drawing(svg_file, profile='full', size=(width, height), )

# Добавляем белый фон
dwg.add(dwg.rect(insert=(-820, -220), size=(2000, 1600), fill='white'))



(df, cluster_counts, min_year, max_year, min_cluster, max_cluster, years, clusters, count_unique_cluster,
 total_term_counts, term_counts, horizontal_distance_between_nodes, available_height,
 horizontal_distance_between_columns) = prepare_visualization_params(df)

node_positions, years_text = create_nodes_positions()

draw_years(years_text)

flow_data = create_flows()

couples = create_couples(df, years)

draw_flows()

draw_nodes()

draw_logos()

dwg['viewBox'] = f'0 0 {width} {height}'

# Сохраняем SVG файл
dwg.save()

png_file = 'sankey_diagram.png'

svg_string = dwg.tostring()

# Конвертация SVG в PNG
cairosvg.svg2png(bytestring=svg_string, write_to='output4.png', dpi=10)  # Замените 300 на нужное значение

print("Sankey диаграмма сохранена в sankey_diagram.svg")

