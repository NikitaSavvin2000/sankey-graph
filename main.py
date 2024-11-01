import base64
import svgwrite
import cairosvg
import pandas as pd

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


class SankeyMap:
    """
    Класс для создания Санки-диаграмм.

    Атрибуты:
    ----------
    area : str
        Название области, где будет отображаться диаграмма.
    df : pandas.DataFrame
        Данные для визуализации, содержащие столбцы с годами, терминами, кластерами и их именами.
    width : int
        Ширина диаграммы (по умолчанию 1400).
    height : int
        Высота диаграммы (по умолчанию 850).
    padding_y : int
        Вертикальные отступы (по умолчанию 50).
    padding_top : int
        Отступ сверху (по умолчанию 10).
    padding_bottom : int
        Отступ снизу (по умолчанию -120).
    padding_x_right : int
        Отступ справа (по умолчанию 50).
    padding_x_left : int
        Отступ слева (по умолчанию 50).
    node_width : int
        Фиксированная ширина узлов (по умолчанию 20).
    min_node_height : int
        Минимальная высота узла (по умолчанию 30).
    fixed_padding_between_clusters : int
        Вертикальный отступ между узлами (по умолчанию 5).
    min_flow_width : int
        Минимальная толщина линии потока (по умолчанию 2).
    max_flow_width : int
        Максимальная толщина линии потока (по умолчанию 15).
    opacity_flow : float
        Прозрачность линии потока (по умолчанию 0.3).

    Методы:
    -------
    prepare_visualization_params():
        Подготавливает параметры визуализации, включая фильтрацию столбцов,
        подсчет кластеров, обновление кластеров, генерацию уникальных имен кластеров и
        инициализацию метрик для визуализации.

    _filter_columns():
        Фильтрует DataFrame, оставляя только необходимые столбцы.

    _compute_cluster_counts():
        Вычисляет количество терминов по годам и кластерам.

    _update_clusters(cluster_counts):
        Обновляет DataFrame с новыми значениями кластеров.

    _generate_unique_cluster_names():
        Генерирует уникальные имена кластеров на основе года и номера кластера.

    _initialize_visualization_metrics():
        Инициализирует метрики и диапазоны для визуализации.

    _calculate_distances():
        Рассчитывает расстояния между узлами и колонками.

    add_flow(source, target, value, color_start, color_end):
        Добавляет поток между узлами, создавая визуализацию кривой Безье.

    draw_flows():
        Рисует потоки между узлами на основе данных.

    draw_nodes():
        Рисует узлы диаграммы, добавляя их визуальные представления.

    normalize_width_flow(couples, x, y):
        Нормализует ширину потоков для визуализации.

    create_couples():
        Создает пары узлов для визуализации потоков на основе данных.

    create_flows():
        Создает данные потоков, основываясь на последовательных годах и терминах.

    add_node(name, x, y0, y1, color):
        Добавляет узел к диаграмме с указанными параметрами.

    create_nodes_positions():
        Создает позиции узлов на диаграмме.

    draw_years():
        Рисует текстовые метки для каждого года на диаграмме.

    draw_logos():
        Рисует логотипы и текстовые источники данных на диаграмме.

    draw_sankey_map():
        Создает и сохраняет диаграмму Санки в формате SVG и PNG.

    Примечание:
    ----------
    Данный класс предназначен для визуализации взаимосвязей и потоков между кластерами терминов за различные годы,
    позволяя визуализировать изменения и связи в данных с помощью диаграмм Санки.
    """

    def __init__(self, df, area):
        self.years_text = None
        self.area = area
        self.df = df
        self.width = 1400
        self.height = 850
        self.padding_y = 50
        self.padding_top = 10
        self.padding_bottom = -120

        self.padding_x_right = 50
        self.padding_x_left = 50

        self.node_width = 20  # Фиксированная ширина узлов
        self.min_node_height = 30  # Минимальная высота узла (для минимального размера)
        self.fixed_padding_between_clusters = 5  # Пробел между узлами вертикальный
        self.min_flow_width = 2  #  Толщина мин перетока
        self.max_flow_width = 15  # Толщина макс перетока
        self.opacity_flow = 0.3  # Прозрачность перетока

    def prepare_visualization_params(self):
        # Оставляем только необходимые столбцы
        self._filter_columns()

        # Считаем количество терминов по годам и кластерам
        cluster_counts = self._compute_cluster_counts()

        # Обновляем DataFrame с новыми значениями кластеров
        self._update_clusters(cluster_counts)

        # Генерируем уникальные имена кластеров
        self._generate_unique_cluster_names()

        # Инициализируем метрики и диапазоны для визуализации
        self._initialize_visualization_metrics()

        # Рассчитываем расстояния между узлами и колонками
        self._calculate_distances()

    def _filter_columns(self):
        self.df = self.df[['year', 'term', 'cluster', 'cluster_name']]

    def _compute_cluster_counts(self):
        cluster_counts = self.df.groupby(['year', 'cluster']).size().reset_index(name='term_count')
        cluster_counts = cluster_counts.sort_values(['year', 'term_count'], ascending=[True, False])
        cluster_counts['new_cluster'] = cluster_counts.groupby('year').cumcount()
        return cluster_counts

    def _update_clusters(self, cluster_counts):
        self.df = self.df.merge(cluster_counts[['year', 'cluster', 'new_cluster']], on=['year', 'cluster'], how='left')
        self.df.drop(columns=['cluster'], inplace=True)
        self.df.rename(columns={'new_cluster': 'cluster'}, inplace=True)

    def _generate_unique_cluster_names(self):
        self.df['unique_cluster_name'] = self.df.apply(lambda row: f"{row['year']} {row['cluster']}", axis=1)

    def _initialize_visualization_metrics(self):
        self.min_year = self.df['year'].min()
        self.max_year = self.df['year'].max()
        self.min_cluster = self.df['cluster'].min()
        self.max_cluster = self.df['cluster'].max()

        self.years = list(range(self.min_year, self.max_year + 1))
        self.clusters = list(range(self.min_cluster, self.max_cluster + 1))

        self.term_counts = self.df.groupby(['year', 'cluster', 'cluster_name']).size().reset_index(name='count')
        self.count_unique_cluster = self.term_counts['cluster'].nunique()
        self.total_term_counts = self.term_counts.groupby('year')['count'].sum().to_dict()

    def _calculate_distances(self):
        self.horizontal_distance_between_nodes = ((self.width + self.padding_x_right) -
                                                  self.node_width * len(self.years)) / len(self.years)
        self.available_height = (self.height - self.padding_top + self.padding_bottom -
                                 self.count_unique_cluster * self.fixed_padding_between_clusters)
        self.horizontal_distance_between_columns = self.horizontal_distance_between_nodes - 2 * self.node_width

    def add_flow(self, source, target, value, color_start, color_end):
        # Получение координат узлов источника и цели
        x0, y0, node_height0 = self.node_positions[source][1]
        x1, y1, node_height1 = self.node_positions[target][1]

        # Вычисление центров по вертикали для источника и цели
        source_center_y = y0 + (node_height0 - y0) / 2
        target_center_y = y1 + (node_height1 - y1) / 2

        # Определение контрольных точек для кривой Безье
        control_x = (x0 + x1) / 2

        # Создание идентификатора для градиента
        source_id = source.replace(' ', '_')
        target_id = target.replace(' ', '_')
        gradient_id = f'{source_id}_{target_id}_{value}'

        # Добавление линейного градиента в defs
        gradient = self.dwg.defs.add(
            self.dwg.linearGradient(id=gradient_id, start=('0%', '0%'), end=('100%', '0%'))
        )
        gradient.add_stop_color(0, color_start, opacity=0.3)
        gradient.add_stop_color(1, color_end, opacity=0.3)

        # Добавление пути для визуализации потока
        self.dwg.add(
            self.dwg.path(
                d=f'M {x0 + self.node_width}, {source_center_y} C {control_x}, {source_center_y} '
                  f'{control_x}, {target_center_y} {x1}, {target_center_y}',
                stroke=f'url(#{gradient_id})',
                stroke_width=value,
                fill='none'
            )
        )

    def draw_flows(self):
        for (source_tuple, target_tuple), value in self.couples.items():
            source = source_tuple[0]
            target = target_tuple[0]

            try:
                cluster_source = self.df.loc[self.df["unique_cluster_name"] == source, 'cluster'].iloc[0]
                cluster_target = self.df.loc[self.df["unique_cluster_name"] == target, 'cluster'].iloc[0]
            except IndexError:
                # Логирование ошибки или пропуск итерации при отсутствии данных
                print(f"Warning: Cluster data not found for source '{source}' or target '{target}'.")
                continue

            color_start = colors_dict.get(cluster_source, '#000000')  # Использование черного по умолчанию
            color_end = colors_dict.get(cluster_target, '#000000')  # Использование черного по умолчанию

            self.add_flow(source, target, value, color_start, color_end)

    def draw_nodes(self):
        for node, values in self.node_positions.items():
            try:
                # Извлечение номера кластера из имени узла
                node_parts = node.split(' ')
                cluster_number = int(node_parts[1])
            except (IndexError, ValueError) as e:
                # Логирование ошибки и пропуск итерации при неверном формате узла
                print(f"Не удалось извлечь номер кластера из узла '{node}': {e}")
                continue

            cluster_name = values[0]
            cluster_color = colors_dict.get(cluster_number, '#000000')  # Цвет по умолчанию, если не найден
            (x, y0, y1) = values[1]

            # Добавление узла с проверкой всех значений
            self.add_node(cluster_name, x, y0, y1, cluster_color)

    def normalize_width_flow(self, couples, x, y):
        if not couples:
            print("Предупреждение: Пустой словарь 'couples'. Возвращается пустой результат.")
            return {}

        min_value = min(couples.values())
        max_value = max(couples.values())

        if min_value == max_value:
            print("Все значения в 'couples' одинаковы. Нормализация невозможна, возвращаются одинаковые значения.")
            return {key: x for key in couples.keys()}

        normalized_couples = {
            key: x + ((value - min_value) * (y - x)) / (max_value - min_value)
            for key, value in couples.items()
        }

        return normalized_couples

    def create_couples(self):
        couples = []

        for year in self.years[:-1]:
            df_cur_year = self.df[self.df["year"] == year]
            df_next_year = self.df[self.df["year"] == year + 1]

            for term in df_cur_year['term'].unique():
                term_unique_cluster_cur = df_cur_year[df_cur_year["term"] == term]["unique_cluster_name"].values
                term_unique_cluster_next = df_next_year[df_next_year["term"] == term]["unique_cluster_name"].values

                # Проверка на наличие кластеров в обоих годах
                if term_unique_cluster_cur.size > 0 and term_unique_cluster_next.size > 0:
                    couples.append([term_unique_cluster_cur, term_unique_cluster_next])

        if not couples:
            print("Не найдено пар для создания связей.")
            self.couples = {}
            return

        count_dict = defaultdict(int)

        for sublist in couples:
            # Преобразование значений для использования в качестве ключей
            tuple_key = tuple(tuple(item) for item in sublist)
            count_dict[tuple_key] += 1

        # Преобразование словаря для нормализации
        couples_dict = dict(count_dict)

        # Нормализация ширины потока
        self.couples = self.normalize_width_flow(couples_dict, self.min_flow_width, self.max_flow_width)

    def create_flows(self):
        flow_data = []

        for term in self.df['term'].unique():
            term_data = self.df[self.df['term'] == term].sort_values('year')

            if term_data.empty:
                print(f" Нет данных для термина '{term}'. Пропуск.")
                continue

            for i in range(len(term_data) - 1):
                current_year = term_data.iloc[i]['year']
                next_year = term_data.iloc[i + 1]['year']

                # Проверка, что данные относятся к последовательным годам
                if next_year - current_year == 1:
                    source_node = term_data.iloc[i]['cluster_name']
                    target_node = term_data.iloc[i + 1]['cluster_name']

                    # Проверка на пустые узлы
                    if not source_node or not target_node:
                        print(
                            f"Пустые значения узлов для термина '{term}' между {current_year} и {next_year}. Пропуск.")
                        continue

                    flow_data.append((source_node, target_node))

        if not flow_data:
            print("Потоки не были созданы. Возможно, отсутствуют переходы между последовательными годами.")

        self.flow_data = flow_data

    def add_node(self, name, x, y0, y1, color):
        height = y1 - y0  # Высота столбика
        self.dwg.add(self.dwg.rect(insert=(x, y0), size=(self.node_width, height), fill=color, opacity=0.9))

        max_text_width = self.horizontal_distance_between_columns - (self.node_width)

        font_size = 14
        max_lines = 2  # Максимальное количество строк текста

        # Для примерного вычисления длины текста
        def text_width(text, font_size):
            return font_size * 0.6 * len(text)  # Примерная ширина символов

        words = name.split()
        lines = []
        current_line = ""

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

        while len(lines) > max_lines or any(text_width(line, font_size) > max_text_width for line in lines):
            font_size -= 0.1
            lines = []
            current_line = ""

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

        text_x = x + self.node_width + 10
        text_y_start = y0 + height / 2 - (font_size + 2) * (len(lines) - 1) / 2

        for i, line in enumerate(lines[:max_lines]):
            text_y = text_y_start + i * (font_size + 2)
            self.dwg.add(self.dwg.text(line, insert=(text_x, text_y), fill='black', font_size=f'{font_size}px',
                                       font_family='Arial',
                                       text_anchor="start"))

    def create_nodes_positions(self):
        self.node_positions = {}
        self.years_text = {}
        for year in self.years:
            x_year_start = self.padding_x_left + (year - self.min_year) * self.horizontal_distance_between_nodes
            x = x_year_start

            total_count = self.term_counts.loc[self.term_counts['year'] == year, 'count'].sum()

            cluster_proportion_dict = {}
            if total_count > 0:
                for _, row in self.term_counts.loc[self.term_counts['year'] == year].iterrows():
                    cluster = row['cluster']
                    count = row['count']
                    cluster_proportion_dict[cluster] = (count / total_count) * self.available_height

            for cluster, value in cluster_proportion_dict.items():
                if value < self.min_node_height:
                    cluster_proportion_dict[cluster] = self.min_node_height

            total_sum = sum(cluster_proportion_dict.values())
            extra_height = self.available_height - total_sum

            if extra_height < 0:
                total_above_min = sum(value for value in cluster_proportion_dict.values())
                for cluster in cluster_proportion_dict:
                    value = cluster_proportion_dict[cluster]
                    proportion = value / total_above_min
                    decrease = proportion * extra_height
                    cluster_proportion_dict[cluster] += decrease

            y0 = self.padding_top
            for cluster in self.clusters:
                cluster_name = \
                    self.term_counts[(self.term_counts['year'] == year) & (self.term_counts['cluster'] == cluster)][
                        'cluster_name'].values
                cluster_name = str(cluster_name[0]) if cluster_name.size > 0 else f"Cluster {cluster}"

                node_height = cluster_proportion_dict.get(cluster, self.min_node_height)
                y1 = y0 + node_height

                self.node_positions[f'{year} {cluster}'] = [cluster_name, (x, y0, y1)]

                y0 = y1 + self.fixed_padding_between_clusters

            self.years_text[year] = [x_year_start, y1]

    def draw_years(self, ):
        for key, values in self.years_text.items():
            self.dwg.add(
                self.dwg.text(key, insert=(values[0] - 15, values[1] + 35), fill='black', font_size='24px',
                              font_family='Arial'))

    def draw_logos(self):
        with open('/Users/nikitasavvin/Desktop/HSE_work/sankey-graph/iFORA logo 2.svg', 'rb') as image_file:
            encoded_image = base64.b64encode(image_file.read()).decode('utf-8')

        data_uri = f"data:image/svg+xml;base64,{encoded_image}"
        self.dwg.add(self.dwg.image(href=data_uri, insert=(10, 790), size=(105, 60)))

        text = "Источник: Система интеллектуального анализа больших данных iFORA (правообладатель — ИСИЭЗ НИУ ВШЭ)"

        self.dwg.add(self.dwg.text(text, insert=(423, 845),
                                   fill='gray',
                                   font_size='18px',
                                   font_family='Arial',
                                   font_style='italic',
                                   text_anchor="start"))

    def draw_sankey_map(self):

        area = self.area.replace(' ', '_')
        svg_file = f'sankey_diagram_{area}.svg'

        self.dwg = svgwrite.Drawing(svg_file, profile='full', size=(self.width, self.height), )

        self.dwg.add(self.dwg.rect(insert=(0, 0), size=(2000, 1600), fill='white'))

        self.prepare_visualization_params()

        self.create_nodes_positions()

        self.draw_years()

        self.create_flows()

        self.create_couples()

        self.draw_flows()

        self.draw_nodes()

        self.draw_logos()

        self.dwg['viewBox'] = f'0 0 {self.width} {self.height}'

        self.dwg.save()

        png_file = f'sankey_diagram_{area}.png'

        svg_string = self.dwg.tostring()

        cairosvg.svg2png(bytestring=svg_string, write_to=png_file, dpi=10)  # Замените 300 на нужное значение

        print(f"Sankey диаграмма сохранена в {svg_file}")


df = pd.read_csv('/Users/nikitasavvin/Desktop/HSE_work/ifora_core/experiments/df_sankey_дорожные карты.csv')

sm = SankeyMap(df=df, area='test')

sm.draw_sankey_map()
