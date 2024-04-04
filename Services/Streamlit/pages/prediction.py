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


def show_page():
    st.header('Предсказания', divider='rainbow')

    co = st.number_input("Введите уровень CO", min_value=0, max_value=200, value="min")
    no = st.number_input("Введите уровень NO", min_value=0, max_value=200, value="min")
    ozone = st.number_input("Введите уровень Ozone", min_value=0, max_value=300, value="min")
    pm2 = st.number_input("Введите уровень PM2.5", min_value=0, max_value=500, value="min")

    if st.button('Predict'):
        inputs = {
                    "co": co,
                    "no": no,
                    "ozone": ozone,
                    "pm2": pm2
                }

        res = requests.post(url="http://127.0.0.1:8000/predict", data=json.dumps(inputs))
        with st.spinner('Classifying, please wait....'):
            st.subheader(f"Индекс качества воздуха = **{res.text}!**")
