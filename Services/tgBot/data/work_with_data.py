import pandas as pd
import gzip
import pickle


with gzip.open('./data/pickle_model.pkl', 'rb') as ifp:
    MODEL = pickle.load(ifp)


def load_data():
    return pd.read_csv("data/prep_data.csv", index_col=False)


final = load_data()


def top_10():
    """
        Вывод списка 10 стран с наилучшим индексом качества воздуха из датасета
    """
    blank_index = [''] * len(final)
    df = final[['AQI Value', 'Country', 'City']].copy().sort_values(by=['AQI Value'])
    df.index = blank_index
    return df.head(10)


def less_10():
    """
        Вывод списка 10 стран с наихудшим индексом качества воздуха из датасета
    """
    blank_index = [''] * len(final)
    df2 = final[['AQI Value', 'Country', 'City']].copy().sort_values(by=['AQI Value'], ascending=False)
    df2.index = blank_index
    return df2.head(10)


def get_cat(x):
    """
        Функция для определения категории по числовому значению индекса
    """
    if x <= 50:
        return "Good"
    elif x <= 100:
        return "Moderate"
    elif x <= 150:
        return "Unhealthy for Sensitive Groups"
    elif x <= 200:
        return "Unhealthy"
    elif x <= 300:
        return "Very Unhealthy"
    elif x > 300:
        return "Hazardous"


def get_img(x):
    """
        Возвращаем адрес картинки в зависимости от категории индекса
    """
    if "Good" in x:
        return "images/good.png"
    elif "Moderate" in x:
        return "images/moderate.png"
    elif "Unhealthy for" in x:
        return "images/unhealthy for  groups.png"
    elif "Unhealthy" in x:
        return "images/unhealthy.png"
    elif "Very" in x:
        return "images/very unhealthy.png"
    elif "Hazardous" in x:
        return "images/haz.png"


def predict_model(df):
    prediction = MODEL.predict(df)
    cat = get_cat(prediction[0])
    img_link = get_img(cat)

    return prediction[0], cat, img_link
