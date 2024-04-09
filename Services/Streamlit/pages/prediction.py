import streamlit as st
import json
import requests

# Class values to be returned by the model
class_values = {
    0: "unacceptable",
    1: "acceptable",
    2: "good",
    3: "very good"
    }


def show_page(df):
    st.header('Предсказания', divider='rainbow')
    if 'state' not in st.session_state:
        st.session_state.state = 0
    if st.button("Ввести показатели"):
        st.session_state['state'] = 1
    if st.button("Ввести локацию"):
        st.session_state['state'] = 2

    if st.session_state['state'] == 1:
        co = st.number_input("Введите уровень CO", min_value=0, max_value=200, value="min")
        no = st.number_input("Введите уровень NO", min_value=0, max_value=200, value="min")
        ozone = st.number_input("Введите уровень Ozone", min_value=0, max_value=300, value="min")
        pm2 = st.number_input("Введите уровень PM2.5", min_value=0, max_value=500, value="min")

        if st.button('Узнать индекс'):
            inputs = {
                        "co": co,
                        "no": no,
                        "ozone": ozone,
                        "pm2": pm2
                    }

            res = requests.post(url="http://fastapi:8000/predict", data=json.dumps(inputs))
            with st.spinner('Classifying, please wait....'):
                st.subheader(f"Индекс качества воздуха = **{res.text}!**")

    if st.session_state['state'] == 2:
        countries = list(sorted(df['Country'].unique()))
        selected_country = st.selectbox('Страна:', countries)

        selected_df = df[df['Country'] == selected_country]
        sorted_list = list(sorted(selected_df['City'].unique()))
        # sorted_list.insert(0, '-')
        selected_city = st.selectbox('Город (Страна - {})'.format(selected_country), sorted_list)

        if st.button('Узнать индекс'):
            location_inputs = {
                "Country": selected_country,
                "City": selected_city
            }

            res = requests.post(url="http://fastapi:8000/get_data", data=json.dumps(location_inputs))
            with st.spinner('Classifying, please wait....'):
                st.subheader(f"Индекс качества воздуха = **{res.text}!**")
