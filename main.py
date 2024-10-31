import pandas as pd
import svgwrite

import cairosvg



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

svg = """
<svg width="324" height="159" viewBox="0 0 324 159" fill="none" xmlns="http://www.w3.org/2000/svg">
<mask id="mask0_68_354" style="mask-type:luminance" maskUnits="userSpaceOnUse" x="5" y="0" width="302" height="112">
<path d="M12.0237 0L288.55 31.9228L306.791 57.7875V94.5259L274.233 111.614L5.80493 21.812L12.0237 0Z" fill="white"/>
</mask>
<g mask="url(#mask0_68_354)">
<g filter="url(#filter0_f_68_354)">
<ellipse cx="269.363" cy="55.3885" rx="131.029" ry="130.328" transform="rotate(-20.2612 269.363 55.3885)" fill="#C782FE"/>
</g>
<g filter="url(#filter1_f_68_354)">
<circle cx="101.558" cy="17.4918" r="66.7158" transform="rotate(-20.2612 101.558 17.4918)" fill="#94CEFF"/>
</g>
<g filter="url(#filter2_f_68_354)">
<ellipse cx="195.615" cy="13.1429" rx="48.7791" ry="48.5603" transform="rotate(-20.2612 195.615 13.1429)" fill="#59B3FF"/>
</g>
<g filter="url(#filter3_f_68_354)">
<circle cx="141.252" cy="57.1708" r="48.5603" transform="rotate(-20.2612 141.252 57.1708)" fill="#90F6FD"/>
</g>
<g filter="url(#filter4_f_68_354)">
<circle cx="203.476" cy="82.5243" r="48.5603" transform="rotate(-20.2612 203.476 82.5243)" fill="#DA92FC"/>
</g>
<g filter="url(#filter5_f_68_354)">
<circle cx="29.6787" cy="11.2294" r="48.5603" transform="rotate(-20.2612 29.6787 11.2294)" fill="#3EA6F9"/>
</g>
<g filter="url(#filter6_f_68_354)">
<ellipse cx="238.868" cy="7.21755" rx="64.2855" ry="64.2855" transform="rotate(-20.2612 238.868 7.21755)" fill="#DCFEBC"/>
</g>
<g filter="url(#filter7_f_68_354)">
<ellipse cx="212.097" cy="-8.69847" rx="64.2855" ry="64.2855" transform="rotate(-20.2612 212.097 -8.69847)" fill="#745DFC"/>
</g>
</g>
<path d="M88.0398 31.8711V47.7409H70.5984C60.7067 47.7409 52.664 55.7836 52.664 65.6753H88.0398V81.5451H52.664V115.349H36.7942V65.6753C36.7942 47.0013 51.9244 31.8711 70.5984 31.8711H88.0398Z" fill="black"/>
<path d="M205.969 81.5451V115.349H190.1V65.6753C190.1 47.0013 205.23 31.8711 223.904 31.8711H241.345V47.7409H223.904C214.012 47.7409 205.969 55.7836 205.969 65.6753" fill="black"/>
<path d="M139.069 49.1276C152.073 49.1276 162.643 59.6972 162.643 72.7012C162.643 85.7051 152.073 96.2747 139.069 96.2747C126.065 96.2747 115.496 85.7051 115.496 72.7012C115.496 59.6972 126.065 49.1276 139.069 49.1276ZM139.069 31.8711C116.512 31.8711 98.2083 50.1445 98.2083 72.732C98.2083 95.3195 116.482 113.593 139.069 113.593C161.626 113.593 179.93 95.3195 179.93 72.732C179.93 50.1445 161.657 31.8711 139.069 31.8711Z" fill="black"/>
<path d="M282.514 49.1276C295.518 49.1276 306.087 59.6972 306.087 72.7012C306.087 85.7051 295.518 96.2747 282.514 96.2747C269.51 96.2747 258.94 85.7051 258.94 72.7012C258.94 59.6972 269.51 49.1276 282.514 49.1276ZM282.514 31.8711C259.957 31.8711 241.653 50.1445 241.653 72.732C241.653 95.3195 259.926 113.593 282.514 113.593C305.07 113.593 323.374 95.3195 323.374 72.732C323.374 50.1445 305.101 31.8711 282.514 31.8711Z" fill="black"/>
<path d="M19.3517 31.8711H3.48193V115.38H19.3517V31.8711Z" fill="black"/>
<path d="M323.374 72.7012H307.412V113.562H323.374V72.7012Z" fill="black"/>
<path d="M11.4324 22.8648C17.7464 22.8648 22.8648 17.7464 22.8648 11.4324C22.8648 5.11847 17.7464 0 11.4324 0C5.11847 0 0 5.11847 0 11.4324C0 17.7464 5.11847 22.8648 11.4324 22.8648Z" fill="black"/>
<path d="M7.20708 132.953V151H5.19612V132.953H7.20708ZM19.3641 151V144.168C19.3641 141.383 18.1266 140.894 16.8117 140.894C15.239 140.894 13.6922 142.389 12.764 143.498V151H10.882V139.347H12.764V141.229C13.8468 140.172 15.4711 139.012 17.1727 139.012C19.6735 139.012 21.2462 140.275 21.2462 143.73V151H19.3641ZM27.5937 141.1V147.545C27.5937 148.912 27.8257 149.556 28.7023 149.556C29.2952 149.556 30.0687 149.35 31.0999 148.86V150.691C30.2234 151.077 29.2179 151.309 28.3671 151.309C26.1241 151.309 25.7116 149.711 25.7116 146.849V141.074H23.6491V139.347H25.7116V135.376H27.5937V139.347H31.0742V141.1H27.5937ZM32.2688 145.173C32.2688 141.667 34.8985 139.012 38.4048 139.012C41.8595 139.012 44.1799 141.1 44.1799 145.044C44.1799 145.328 44.1541 145.637 44.1541 145.921H34.1508C34.6149 148.087 36.3681 149.53 38.5595 149.53C40.1837 149.53 41.5759 148.705 42.633 147.391L43.8963 148.525C42.6072 150.355 40.6994 151.309 38.5337 151.309C35.0274 151.309 32.2688 148.68 32.2688 145.173ZM38.4048 140.662C36.1618 140.662 34.486 142.131 34.1251 144.271H42.4009C42.1173 142.105 40.5962 140.662 38.4048 140.662ZM47.0869 131.664H48.969V151H47.0869V131.664ZM52.4749 131.664H54.3569V151H52.4749V131.664ZM57.8113 151V139.347H59.6933V151H57.8113ZM57.5019 134.732C57.5019 134.062 58.0949 133.494 58.7652 133.494C59.4097 133.494 60.0027 134.062 60.0027 134.732C60.0027 135.402 59.4097 135.969 58.7652 135.969C58.0949 135.969 57.5019 135.402 57.5019 134.732ZM67.997 151.335C64.3876 151.335 62.5571 148.705 62.5571 145.173C62.5571 141.641 64.3876 138.986 67.997 138.986C69.6728 138.986 71.065 139.785 72.0963 140.919V139.347H73.8752V151.284C73.8752 155.357 71.1939 157.188 68.0228 157.188C66.115 157.188 64.9032 156.517 62.9954 155.177L64.0009 153.656C65.6251 154.867 66.5275 155.434 68.0228 155.434C70.1884 155.434 71.9932 154.223 71.9932 151.438V149.582C70.9877 150.665 69.647 151.335 67.997 151.335ZM64.4392 145.173C64.4392 147.7 65.6509 149.505 68.1517 149.505C69.9048 149.505 71.2197 148.525 71.9932 147.081V143.266C71.2197 141.822 69.9048 140.842 68.1517 140.842C65.6509 140.842 64.4392 142.647 64.4392 145.173ZM76.6564 145.173C76.6564 141.667 79.2861 139.012 82.7924 139.012C86.2471 139.012 88.5675 141.1 88.5675 145.044C88.5675 145.328 88.5417 145.637 88.5417 145.921H78.5384C79.0025 148.087 80.7557 149.53 82.9471 149.53C84.5713 149.53 85.9635 148.705 87.0206 147.391L88.2839 148.525C86.9948 150.355 85.087 151.309 82.9213 151.309C79.415 151.309 76.6564 148.68 76.6564 145.173ZM82.7924 140.662C80.5494 140.662 78.8736 142.131 78.5127 144.271H86.7886C86.505 142.105 84.9838 140.662 82.7924 140.662ZM99.9567 151V144.168C99.9567 141.383 98.7192 140.894 97.4043 140.894C95.8316 140.894 94.2848 142.389 93.3566 143.498V151H91.4746V139.347H93.3566V141.229C94.4394 140.172 96.0637 139.012 97.7653 139.012C100.266 139.012 101.839 140.275 101.839 143.73V151H99.9567ZM108.186 141.1V147.545C108.186 148.912 108.418 149.556 109.295 149.556C109.888 149.556 110.661 149.35 111.693 148.86V150.691C110.816 151.077 109.81 151.309 108.96 151.309C106.717 151.309 106.304 149.711 106.304 146.849V141.074H104.242V139.347H106.304V135.376H108.186V139.347H111.667V141.1H108.186ZM120.584 151V132.953H129.53V134.912H122.595V140.636H128.885V142.595H122.595V151H120.584ZM136.468 140.765C134.07 140.765 132.317 142.75 132.317 145.173C132.317 147.571 134.07 149.556 136.468 149.556C138.892 149.556 140.567 147.571 140.567 145.173C140.567 142.75 138.892 140.765 136.468 140.765ZM130.435 145.173C130.435 141.77 133.065 139.012 136.468 139.012C139.871 139.012 142.449 141.77 142.449 145.173C142.449 148.551 139.871 151.309 136.468 151.309C133.065 151.309 130.435 148.551 130.435 145.173ZM151.928 139.347L151.413 141.203C150.949 140.997 150.536 140.945 150.124 140.945C148.731 140.945 147.829 141.77 147.236 143.343V151H145.354V139.347H147.236V140.842C147.7 139.733 149.067 139.012 150.356 139.012C150.845 139.012 151.361 139.089 151.928 139.347ZM152.843 145.173C152.843 141.667 155.473 139.012 158.979 139.012C162.434 139.012 164.754 141.1 164.754 145.044C164.754 145.328 164.728 145.637 164.728 145.921H154.725C155.189 148.087 156.942 149.53 159.134 149.53C160.758 149.53 162.15 148.705 163.207 147.391L164.47 148.525C163.181 150.355 161.274 151.309 159.108 151.309C155.602 151.309 152.843 148.68 152.843 145.173ZM158.979 140.662C156.736 140.662 155.06 142.131 154.699 144.271H162.975C162.692 142.105 161.17 140.662 158.979 140.662ZM173.597 147.7C173.597 145.044 166.945 146.978 166.945 142.337C166.945 140.301 168.518 138.986 170.941 138.986C172.823 138.986 174.19 139.682 175.273 141.177L174.009 142.415C173.21 141.229 172.308 140.739 170.941 140.739C169.575 140.739 168.724 141.332 168.724 142.312C168.724 145.122 175.402 143.008 175.402 147.674C175.402 149.969 173.597 151.361 170.864 151.361C169.034 151.361 167.616 150.691 166.223 149.144L167.435 147.803C168.827 149.221 169.627 149.659 170.864 149.659C172.463 149.659 173.597 148.834 173.597 147.7ZM177.983 151V139.347H179.865V151H177.983ZM177.673 134.732C177.673 134.062 178.266 133.494 178.937 133.494C179.581 133.494 180.174 134.062 180.174 134.732C180.174 135.402 179.581 135.969 178.937 135.969C178.266 135.969 177.673 135.402 177.673 134.732ZM188.168 151.335C184.559 151.335 182.728 148.705 182.728 145.173C182.728 141.641 184.559 138.986 188.168 138.986C189.844 138.986 191.236 139.785 192.268 140.919V139.347H194.047V151.284C194.047 155.357 191.365 157.188 188.194 157.188C186.286 157.188 185.075 156.517 183.167 155.177L184.172 153.656C185.796 154.867 186.699 155.434 188.194 155.434C190.36 155.434 192.164 154.223 192.164 151.438V149.582C191.159 150.665 189.818 151.335 188.168 151.335ZM184.61 145.173C184.61 147.7 185.822 149.505 188.323 149.505C190.076 149.505 191.391 148.525 192.164 147.081V143.266C191.391 141.822 190.076 140.842 188.323 140.842C185.822 140.842 184.61 142.647 184.61 145.173ZM205.903 151V144.168C205.903 141.383 204.665 140.894 203.35 140.894C201.778 140.894 200.231 142.157 199.303 143.291V151H197.421V131.664H199.303V141.023C200.386 139.965 202.01 139.012 203.711 139.012C206.212 139.012 207.785 140.275 207.785 143.73V151H205.903ZM214.132 141.1V147.545C214.132 148.912 214.364 149.556 215.241 149.556C215.834 149.556 216.607 149.35 217.639 148.86V150.691C216.762 151.077 215.757 151.309 214.906 151.309C212.663 151.309 212.25 149.711 212.25 146.849V141.074H210.188V139.347H212.25V135.376H214.132V139.347H217.613V141.1H214.132ZM227.355 151H225.112L232.666 132.953H233.31L240.864 151H238.621L236.482 145.792H229.469L227.355 151ZM232.975 137.207L230.294 143.781H235.657L232.975 137.207ZM251.625 151V144.168C251.625 141.383 250.387 140.894 249.072 140.894C247.5 140.894 245.953 142.389 245.025 143.498V151H243.143V139.347H245.025V141.229C246.108 140.172 247.732 139.012 249.433 139.012C251.934 139.012 253.507 140.275 253.507 143.73V151H251.625ZM260.061 151.309C257.792 151.309 256.297 149.969 256.297 147.726C256.297 144.787 258.101 143.601 263.928 143.601V143.523C263.928 141.564 263.103 140.739 261.35 140.739C259.932 140.739 259.004 141.1 257.74 142.595L256.529 141.28C257.998 139.63 259.365 139.012 261.479 139.012C265.346 139.012 265.81 141.616 265.81 143.498V151H263.928V149.195C262.948 150.536 261.582 151.309 260.061 151.309ZM260.318 149.634C261.582 149.634 262.639 148.937 263.928 146.952V145.173C259.468 145.173 258.179 145.792 258.179 147.726C258.179 149.118 258.978 149.634 260.318 149.634ZM269.176 131.664H271.058V151H269.176V131.664ZM275.286 156.93L277.89 150.82L273.069 139.347H275.105L278.947 148.37L282.711 139.347H284.748L277.323 156.93H275.286ZM289.715 141.1V147.545C289.715 148.912 289.947 149.556 290.823 149.556C291.416 149.556 292.19 149.35 293.221 148.86V150.691C292.344 151.077 291.339 151.309 290.488 151.309C288.245 151.309 287.833 149.711 287.833 146.849V141.074H285.77V139.347H287.833V135.376H289.715V139.347H293.195V141.1H289.715ZM295.435 151V139.347H297.317V151H295.435ZM295.125 134.732C295.125 134.062 295.718 133.494 296.389 133.494C297.033 133.494 297.626 134.062 297.626 134.732C297.626 135.402 297.033 135.969 296.389 135.969C295.718 135.969 295.125 135.402 295.125 134.732ZM309.823 147.519L311.292 148.525C310.132 150.227 308.328 151.309 306.239 151.309C302.836 151.309 300.181 148.551 300.181 145.173C300.181 141.77 302.836 139.012 306.239 139.012C308.328 139.012 310.132 140.094 311.292 141.796L309.823 142.801C308.998 141.59 307.709 140.765 306.239 140.765C303.816 140.765 302.063 142.75 302.063 145.173C302.063 147.571 303.816 149.556 306.239 149.556C307.709 149.556 308.998 148.731 309.823 147.519ZM320.053 147.7C320.053 145.044 313.402 146.978 313.402 142.337C313.402 140.301 314.974 138.986 317.398 138.986C319.28 138.986 320.646 139.682 321.729 141.177L320.466 142.415C319.667 141.229 318.764 140.739 317.398 140.739C316.031 140.739 315.181 141.332 315.181 142.312C315.181 145.122 321.858 143.008 321.858 147.674C321.858 149.969 320.053 151.361 317.321 151.361C315.49 151.361 314.072 150.691 312.68 149.144L313.892 147.803C315.284 149.221 316.083 149.659 317.321 149.659C318.919 149.659 320.053 148.834 320.053 147.7Z" fill="black"/>
<defs>
<filter id="filter0_f_68_354" x="79.3831" y="-134.059" width="379.961" height="378.895" filterUnits="userSpaceOnUse" color-interpolation-filters="sRGB">
<feFlood flood-opacity="0" result="BackgroundImageFix"/>
<feBlend mode="normal" in="SourceGraphic" in2="BackgroundImageFix" result="shape"/>
<feGaussianBlur stdDeviation="29.5" result="effect1_foregroundBlur_68_354"/>
</filter>
<filter id="filter1_f_68_354" x="-53.1755" y="-137.242" width="309.468" height="309.468" filterUnits="userSpaceOnUse" color-interpolation-filters="sRGB">
<feFlood flood-opacity="0" result="BackgroundImageFix"/>
<feBlend mode="normal" in="SourceGraphic" in2="BackgroundImageFix" result="shape"/>
<feGaussianBlur stdDeviation="44" result="effect1_foregroundBlur_68_354"/>
</filter>
<filter id="filter2_f_68_354" x="10.8484" y="-171.457" width="369.532" height="369.2" filterUnits="userSpaceOnUse" color-interpolation-filters="sRGB">
<feFlood flood-opacity="0" result="BackgroundImageFix"/>
<feBlend mode="normal" in="SourceGraphic" in2="BackgroundImageFix" result="shape"/>
<feGaussianBlur stdDeviation="68" result="effect1_foregroundBlur_68_354"/>
</filter>
<filter id="filter3_f_68_354" x="-50.3213" y="-134.402" width="383.147" height="383.146" filterUnits="userSpaceOnUse" color-interpolation-filters="sRGB">
<feFlood flood-opacity="0" result="BackgroundImageFix"/>
<feBlend mode="normal" in="SourceGraphic" in2="BackgroundImageFix" result="shape"/>
<feGaussianBlur stdDeviation="71.5" result="effect1_foregroundBlur_68_354"/>
</filter>
<filter id="filter4_f_68_354" x="51.9026" y="-69.0488" width="303.147" height="303.146" filterUnits="userSpaceOnUse" color-interpolation-filters="sRGB">
<feFlood flood-opacity="0" result="BackgroundImageFix"/>
<feBlend mode="normal" in="SourceGraphic" in2="BackgroundImageFix" result="shape"/>
<feGaussianBlur stdDeviation="51.5" result="effect1_foregroundBlur_68_354"/>
</filter>
<filter id="filter5_f_68_354" x="-97.8948" y="-116.344" width="255.147" height="255.146" filterUnits="userSpaceOnUse" color-interpolation-filters="sRGB">
<feFlood flood-opacity="0" result="BackgroundImageFix"/>
<feBlend mode="normal" in="SourceGraphic" in2="BackgroundImageFix" result="shape"/>
<feGaussianBlur stdDeviation="39.5" result="effect1_foregroundBlur_68_354"/>
</filter>
<filter id="filter6_f_68_354" x="84.5647" y="-147.085" width="308.606" height="308.605" filterUnits="userSpaceOnUse" color-interpolation-filters="sRGB">
<feFlood flood-opacity="0" result="BackgroundImageFix"/>
<feBlend mode="normal" in="SourceGraphic" in2="BackgroundImageFix" result="shape"/>
<feGaussianBlur stdDeviation="45" result="effect1_foregroundBlur_68_354"/>
</filter>
<filter id="filter7_f_68_354" x="57.7942" y="-163.001" width="308.606" height="308.605" filterUnits="userSpaceOnUse" color-interpolation-filters="sRGB">
<feFlood flood-opacity="0" result="BackgroundImageFix"/>
<feBlend mode="normal" in="SourceGraphic" in2="BackgroundImageFix" result="shape"/>
<feGaussianBlur stdDeviation="45" result="effect1_foregroundBlur_68_354"/>
</filter>
</defs>
</svg>

"""

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
height = 850  # Высота графика
padding_y = 50
padding_top = 10
padding_bottom = -120

padding_x_right = 95
padding_x_left = -650


node_width = 20  # Фиксированная ширина узлов
min_node_height = 30  # Минимальная высота узла (для минимального размера)

horizontal_distance_between_nodes = ((width + padding_x_right) - node_width*(len(years))) / (len(years))


print(f'horizontal_distance_between_nodes = {horizontal_distance_between_nodes}')

# Создаем SVG-документ
svg_file = 'sankey_diagram.svg'
dwg = svgwrite.Drawing(svg_file, profile='full', size=(width, height),)

# Добавляем белый фон
dwg.add(dwg.rect(insert=(-820, -220), size=(2000, 1600), fill='white'))

# dwg.add(dwg.image('/Users/nikitasavvin/Desktop/HSE_work/sankey-graph/iFORA logo 2.svg', insert=(-680, 790), size=(105, 60)))


import svgwrite
import base64

# Читаем изображение и кодируем его в Base64
with open('/Users/nikitasavvin/Desktop/HSE_work/sankey-graph/iFORA logo 2.svg', 'rb') as image_file:
    encoded_image = base64.b64encode(image_file.read()).decode('utf-8')


data_uri = f"data:image/svg+xml;base64,{encoded_image}"
dwg.add(dwg.image(href=data_uri, insert=(-680, 790), size=(105, 60)))





text = "Источник: Система интеллектуального анализа больших данных iFORA (правообладатель — ИСИЭЗ НИУ ВШЭ)"


dwg.add(dwg.text(text, insert=(-280, 845),
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
    # Определяем начальную позицию по X для каждого года
    x_year_start = padding_x_left + (year - min_year) * horizontal_distance_between_nodes
    x = x_year_start  # Начальная позиция X для текущего года

    # Вычисление пропорций и высот
    cluster_count_dict = term_counts.loc[term_counts['year'] == year, ['cluster', 'count']].set_index('cluster')['count'].to_dict()
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
        cluster_name = term_counts[(term_counts['year'] == year) & (term_counts['cluster'] == cluster)]['cluster_name'].values
        cluster_name = str(cluster_name[0]) if cluster_name.size > 0 else f"Cluster {cluster}"

        count = count[0] if count.size > 0 else 0
        node_height = cluster_proportion_dict.get(cluster, min_node_height)
        y1 = y0 + node_height

        # Сохраняем позиции для текущего столбика
        node_positions[f'{year} {cluster}'] = [cluster_name, (x, y0, y1)]

        # Смещаем y0 для следующего кластера
        y0 = y1 + fixed_padding_between_clusters

    # Отображаем год под колонками
    dwg.add(dwg.text(year, insert=(x_year_start - 15, y1 + 35), fill='black', font_size='24px', font_family='Arial'))


horizontal_distance_between_columns = horizontal_distance_between_nodes - 2*node_width



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
        dwg.add(dwg.text(line, insert=(text_x, text_y), fill='black', font_size=f'{font_size}px', font_family='Arial', text_anchor="start"))




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



for node, values in node_positions.items():
    node = node.split(' ')
    cluster_number = int(node[1])
    cluster_name = values[0]
    cluster_color = colors_dict.get(cluster_number)
    (x, y0, y1) = values[1]
    add_node(cluster_name, x, y0, y1, cluster_color, dwg, horizontal_distance_between_columns)

dwg['viewBox'] = f'0 0 {width} {height}'

# Сохраняем SVG файл
dwg.save()

png_file = 'sankey_diagram.png'


svg_string = dwg.tostring()

# Конвертация SVG в PNG
cairosvg.svg2png(bytestring=svg_string, write_to='output4.png', dpi=10)  # Замените 300 на нужное значение

print("Sankey диаграмма сохранена в sankey_diagram.svg")
