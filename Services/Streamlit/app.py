import base64

import streamlit as st
import pandas as pd
import plotly.express as px
from PIL import Image
import pages.prediction as pre

st.set_page_config(page_title='Индекс качества воздуха', layout='wide')

# constants
DATA = 'Data/finalData.csv'


@st.cache_data
def load_data():
    return pd.read_csv(DATA, index_col=0)


final = load_data()


def table_of_categories():
    st.subheader('Диапазоны загрязнителей (US-EPA AQI)')

    data = {
        'Загрязнитель':
            ['Good', 'Moderate', 'Unhealthy for Sensitive Groups', 'Unhealthy', 'Very Unhealthy', 'Hazardous'],
        'PM2.5 (μg/m³ per 24 hr)':
            ['0-12', '12.1-35.4', '35.5-55.4', '55.5-150.4', '150.5-250.4', '250.5+'],
        'Ozone (ppb per 8 hr)':
            ['0-54', '55-70', '71-85', '86-105', '106-200', '201+'],
        'CO (ppm per 8 hr)':
            ['0-4.4', '4.5-9.4', '9.5-12.4', '12.5-15.4', '15.5-30.4', '30.5+'],
        'NO2 (ppb per 1 hr)':
            ['0-53', '54-100', '101-360', '361-649', '650-1249', '1250+']
    }

    df = pd.DataFrame(data)

    st.data_editor(
        df,
        use_container_width=True,
        num_rows="fixed",
        disabled=True,
        hide_index=True,
    )


def plot_country(dataframe, country, param1, param2):

    temp_df = dataframe[dataframe['Country'] == country]
    # hover_name - Values from this column appear in bold in the hover tooltip
    # hover_data - columns to display in hover tooltip
    # size - Values from this column or array_like are used to assign mark sizes
    # mapbox_style– Identifier of base map style
    fig = px.scatter_mapbox(temp_df, lat='lat', lon='lng', size=param1,
                            color=param2, size_max=20,
                            mapbox_style='carto-positron',
                            color_continuous_scale=px.colors.sequential.Viridis_r,
                            hover_name=temp_df['City'], height=800,
                            width=900, zoom=4,
                            hover_data={
                                "AQI Value": True,
                                "lat": False,
                                "lng": False,
                                "CO AQI Value": True,
                                "Ozone AQI Value": True,
                                "NO2 AQI Value": True,
                                "PM2.5 AQI Value": True
                            },
                            title='{} в масштабе {} (Страна - {})'.format(param2, param1, country))

    st.plotly_chart(fig, use_container_width=True)

    st.subheader('Топ городов в {}'.format(country))

    col1, col2 = st.columns(2)
    top = dataframe[dataframe['Country'] == country][['City', param1, param2]].sort_values(by=param1, ascending=False).head(10)

    with col1:
        st.data_editor(
            top,
            use_container_width=True,
            num_rows="fixed",
            disabled=True,
            hide_index=True,
        )

    with col2:
        fig1 = px.bar(top, 'City', param1,
                      title='{} топ 10 городов в {}'.format(param1, country),
                      color=param1, color_continuous_scale=px.colors.sequential.Oryel)
        st.plotly_chart(fig1)


def plot_city(dataframe, country, city, param1, param2):

    temp_df = dataframe[(dataframe['Country'] == country) & (dataframe['City'] == city)]
    fig = px.scatter_mapbox(temp_df, lat='lat', lon='lng', size=param1,
                            color=param2, size_max=20,
                            mapbox_style='carto-positron',
                            color_continuous_scale=px.colors.sequential.Viridis_r,
                            hover_name=temp_df['City'], height=500,
                            width=700, zoom=4,
                            hover_data={
                                "AQI Value": True,
                                "lat": False,
                                "lng": False,
                                "CO AQI Value": True,
                                "Ozone AQI Value": True,
                                "NO2 AQI Value": True,
                                "PM2.5 AQI Value": True

                            },
                            title='{}'.format(city))

    col_lat, col_lng = st.columns(2)
    with col_lat:
        st.metric('Широта', value=temp_df['lat'])
    with col_lng:
        st.metric('Долгота', value=temp_df['lng'])

    col1, col2, col3, col4 = st.columns(4)
    st.plotly_chart(fig, use_container_width=True)
    with col1:
        st.metric('AQI', value=temp_df['AQI Value'])
    with col2:
        st.metric('CO AQI Value', value=temp_df['CO AQI Value'])
    with col3:
        st.metric('Ozone AQI Value', value=temp_df['Ozone AQI Value'])
    with col4:
        st.metric('PM2.5 AQI Value', value=temp_df['PM2.5 AQI Value'])
    st.markdown('---')


st.sidebar.header('Настройки')

tab1, tab2, tab3 = st.tabs(["Анализ", "Информация", "Предсказания"])
with tab1:
    st.header('Индекс качества воздуха')
    st.markdown("*Узнайте показатели воздуха по всему миру*")
    st.divider()

    table_of_categories()

    country = st.sidebar.selectbox('Страна', list(sorted(final['Country'].unique())))

    temp_df = final[final['Country'] == country]
    sorted_list = list(sorted(temp_df['City'].unique()))
    sorted_list.insert(0, '-')
    city = st.sidebar.selectbox('Город (Страна - {})'.format(country), sorted_list)
    column_names = [col for col in final.columns if 'Value' in col]

    primary = st.sidebar.selectbox('Размер меток', column_names)
    secondary = st.sidebar.selectbox('Цвет меток',
                                     [cols for cols in column_names if cols != primary])

    if city == '-':
        plot_country(final, country, primary, secondary)
    else:
        plot_city(final, country, city, primary, secondary)

with tab2:
    st.write(
        'Индекс качества воздуха (AQI) разделен на шесть категорий.'
        ' Каждая категория соответствует разному уровню проблем со здоровьем.')
    image = Image.open('Images/AQI_table.png')
    st.image(image)
    st.write(
        'В новых рекомендациях ВОЗ приводятся рекомендованные значения '
        'допустимой концентрации шести загрязняющих веществ,'
        ' о негативном влиянии которых на здоровье накоплено наибольшее количество данных.')

    st.subheader('Загрязнители:')
    st.write(
        '* Particulate Matter [PM2.5]: '
        'Атмосферные мелкодисперсные частицы, также известные как частицы атмосферного аэрозоля, '
        'представляют собой сложные смеси мелких твердых и жидких веществ, которые попадают в воздух.'
        ' При вдыхании они могут вызвать серьезные проблемы с сердцем и легкими. '
        'Международное агентство по исследованию рака (IARC) отнесло их к канцерогенам первой группы. '
        'PM10 относится к частицам диаметром 10 микрометров или меньше. '
        'PM2,5 относится к частицам диаметром 2,5 микрометра или меньше.')
    st.write(
        '* Nitrogen Dioxide [NO2]: '
        'Диоксид азота — один из нескольких оксидов азота. '
        'Он попадает в воздух в результате природных явлений, таких как проникновение из стратосферы или освещение. '
        'Однако на поверхностном уровне NO2 образуется из выбросов автомобилей, '
        'грузовиков и автобусов, электростанций и внедорожной техники. '
        'Воздействие в течение коротких периодов времени может усугубить респираторные заболевания, такие как астма. '
        'Более длительное воздействие может способствовать развитию астмы и респираторных инфекций. '
        'Люди, страдающие астмой, дети и пожилые люди подвергаются большему риску воздействия NO2 на здоровье.')
    st.write(
        '* Ozone [O3]: '
        'Молекула озона вредна для качества наружного воздуха (если находится за пределами озонового слоя). '
        'На уровне поверхности озон образуется в результате химических реакций между оксидами азота '
        'и летучими органическими соединениями (ЛОС). '
        'В отличие от полезного озона, находящегося в верхних слоях атмосферы, '
        'приземный озон может спровоцировать ряд проблем со здоровьем, таких как боль в груди, кашель,'
        ' раздражение горла и воспаление дыхательных путей. '
        'Кроме того, он может снизить функцию легких и усугубить бронхит, эмфизему и астму.'
        ' Озон влияет также на растительность и экосистемы. '
        'В частности, он повреждает чувствительную растительность в вегетационный период.')
    st.write(
        '* Carbon Monoxide [CO]: '
        'Угарный газ — бесцветный газ без запаха. '
        'На открытом воздухе он выбрасывается в воздух, прежде всего, автомобилями, грузовиками и '
        'другими транспортными средствами или оборудованием, сжигающими ископаемое топливо. '
        'Такие предметы, как керосиновые и газовые обогреватели, газовые плиты, также выделяют CO,'
        ' влияющий на качество воздуха в помещении. '
        'Вдыхание воздуха с высокой концентрацией CO снижает количество кислорода, '
        'который может транспортироваться с током крови к критически важным органам, таким как сердце и мозг.'
        ' На очень высоких уровнях, которые маловероятны на открытом воздухе, но возможны в закрытых помещениях.'
        ' CO может вызвать головокружение, спутанность сознания, потерю сознания и смерть.')

    st.divider()
    st.subheader('Мелкодисперсные частицы:')
    image_pm = Image.open('Images/PM.png')
    st.image(image_pm)
    st.write(
        'Особый интерес с точки зрения санитарно-эпидемиологического благополучия населения'
        ' представляют риски для здоровья, ассоциируемые с мелкодисперсными частицами'
        ' диаметром менее 10 и 2,5 микрон (мкм) (PM₁₀ и PM₂.₅, соответственно). '
        'Как PM₂.₅, так и PM₁₀ способны проникать глубоко в легкие, '
        'однако частицы PM₂.₅ могут попадать даже в кровоток, '
        'что в первую очередь вредит сердечно-сосудистой и дыхательной системам, а также наносит вред другим органам.'
        ' Главным источником загрязнения воздуха мелкодисперсными частицами является '
        'сжигание топлива в различных секторах экономики, включая транспорт, энергетику, '
        'промышленность и сельское хозяйство, а также в быту. '
        'В 2013 г. загрязненный атмосферный воздух и мелкодисперсные частицы были классифицированы'
        ' Международным агентством ВОЗ по изучению рака (МАИР) как канцерогены. ')

with tab3:
    pre.show_page()


st.sidebar.markdown(
    """
    <a href="https://github.com/boisterous-cat/AirQualityProject.git" target="_blank">
             <img src="data:image/png;base64,{}" width="25">
    </a>
    """.format(
        base64.b64encode(open("Images/github_icon.png", "rb").read()).decode()
    ), unsafe_allow_html=True)
