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


class SankeyMap():

    def __init__(self, df, area):
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

        self.df = self.df[['year', 'term', 'cluster', "cluster_name"]]

        cluster_counts = self.df.groupby(['year', 'cluster']).size().reset_index(name='term_count')

        cluster_counts = cluster_counts.sort_values(['year', 'term_count'], ascending=[True, False])

        cluster_counts['new_cluster'] = cluster_counts.groupby('year').cumcount()

        self.df = self.df.merge(cluster_counts[['year', 'cluster', 'new_cluster']], on=['year', 'cluster'], how='left')

        self.df = self.df.drop(columns=['cluster'])

        self.df.rename(columns={'new_cluster': 'cluster'}, inplace=True)

        self.df['unique_cluster_name'] = self.df.apply(lambda row: f"{row['year']} {row['cluster']}", axis=1)

        self.min_year = min(self.df["year"])
        self.max_year = max(self.df["year"])

        self.min_cluster = min(self.df["cluster"])
        self.max_cluster = max(self.df["cluster"])

        self.years = list(range(self.min_year, self.max_year + 1))
        self.clusters = list(range(self.min_cluster, self.max_cluster + 1))

        self.term_counts = self.df.groupby(['year', 'cluster', 'cluster_name']).size().reset_index(name='count')

        self.count_unique_cluster = len(self.term_counts["cluster"].unique())

        self.total_term_counts = self.term_counts.groupby('year')['count'].sum().to_dict()

        self.horizontal_distance_between_nodes = ((self.width + self.padding_x_right) - self.node_width * (
            len(self.years))) / (len(self.years))

        self.available_height = (self.height - self.padding_top + self.padding_bottom -
                                 self.count_unique_cluster * self.fixed_padding_between_clusters)

        self.horizontal_distance_between_columns = self.horizontal_distance_between_nodes - 2 * self.node_width

    def add_flow(self, source, target, value, color_start, color_end):
        x0, y0, node_height0 = self.node_positions[source][1]
        x1, y1, node_height1 = self.node_positions[target][1]

        source_center_y = y0 + (node_height0 - y0) / 2
        target_center_y = y1 + (node_height1 - y1) / 2

        control_x = (x0 + x1) / 2
        control_y0 = source_center_y
        control_y1 = target_center_y

        source_id = source.replace(' ', '_')
        target_id = target.replace(' ', '_')

        id = f'{source_id}_{target_id}_{value}'

        gradient = self.dwg.defs.add(self.dwg.linearGradient(id=id, start=('0%', '0%'), end=('100%', '0%')))

        gradient.add_stop_color(0, color_start, opacity=0.3)
        gradient.add_stop_color(1, color_end, opacity=0.3)

        self.dwg.add(self.dwg.path(
            d=f'M {x0 + self.node_width}, {control_y0} C {control_x},'
              f' {control_y0} {control_x}, {control_y1} {x1}, {control_y1}',
            stroke=f'url(#{id})',
            stroke_width=value, fill='none'
        ))

    def draw_flows(self):
        for key, value in self.couples.items():
            source = key[0][0]
            target = key[1][0]

            cluster_source = self.df[self.df["unique_cluster_name"] == source]['cluster'].iloc[0]
            cluster_target = self.df[self.df["unique_cluster_name"] == target]['cluster'].iloc[0]

            color_start = colors_dict[cluster_source]
            color_end = colors_dict[cluster_target]

            self.add_flow(source, target, value, color_start, color_end)

    def draw_nodes(self):
        for node, values in self.node_positions.items():
            node = node.split(' ')
            cluster_number = int(node[1])
            cluster_name = values[0]
            cluster_color = colors_dict.get(cluster_number)
            (x, y0, y1) = values[1]
            self.add_node(cluster_name, x, y0, y1, cluster_color)

    def normalize_width_flow(self, couples, x, y):
        min_value = min(couples.values())
        max_value = max(couples.values())

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

                if term_unique_cluster_next.size > 0:
                    couples.append([term_unique_cluster_cur, term_unique_cluster_next])

        count_dict = defaultdict(int)

        for sublist in couples:
            tuple_key = tuple(tuple(item) for item in sublist)
            count_dict[tuple_key] += 1

        couples = dict(count_dict)

        self.couples = self.normalize_width_flow(couples, self.min_flow_width, self.max_flow_width)

    def create_flows(self):
        flow_data = []
        for term in self.df['term'].unique():
            term_data = self.df[self.df['term'] == term].sort_values('year')
            for i in range(len(term_data) - 1):
                current_year = term_data.iloc[i]['year']
                next_year = term_data.iloc[i + 1]['year']

                if next_year - current_year == 1:  # переток только на следующий год
                    source_node = f"{term_data.iloc[i]['cluster_name']}"
                    target_node = f"{term_data.iloc[i + 1]['cluster_name']}"
                    flow_data.append((source_node, target_node))

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
        node_positions = {}
        years_text = {}
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

                node_positions[f'{year} {cluster}'] = [cluster_name, (x, y0, y1)]

                y0 = y1 + self.fixed_padding_between_clusters

            years_text[year] = [x_year_start, y1]

        return node_positions, years_text

    def draw_years(self, years_text):
        for key, values in years_text.items():
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
                                   fill='gray',  # Цвет шрифта
                                   font_size='18px',
                                   font_family='Arial',
                                   font_style='italic',  # Наклон
                                   text_anchor="start"))

    def draw_sankey_map(self):

        area = self.area.replace(' ', '_')
        svg_file = f'sankey_diagram_{area}.svg'

        self.dwg = svgwrite.Drawing(svg_file, profile='full', size=(self.width, self.height), )

        self.dwg.add(self.dwg.rect(insert=(0, 0), size=(2000, 1600), fill='white'))

        self.prepare_visualization_params()

        self.node_positions, years_text = self.create_nodes_positions()

        self.draw_years(years_text)

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
