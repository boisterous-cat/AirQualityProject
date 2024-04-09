# -*- coding: utf-8 -*-
"""Untitled9.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/175QC2ohKuGpKKUmAVO_SwkULeChkjS1K
"""

import pandas as pd
import boto3
import pickle
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score, mean_squared_error as mse
from sklearn.neighbors import KNeighborsRegressor
from typing import Any, Dict, Tuple
from config import S3_CONFIG


# Подключение к S3
s3_resource = boto3.resource(
        service_name="s3",
        endpoint_url=S3_CONFIG["endpoint_url"],
        aws_access_key_id=S3_CONFIG["aws_access_key_id"],
        aws_secret_access_key=S3_CONFIG["aws_secret_access_key"],
    )

"""# PipeLine"""


def download_data():
    obj = s3_resource.Object(bucket_name="aqi", key="cleared_data.csv")
    df = pd.read_csv(obj.get()['Body'])
    return df


data = download_data()


def preprocess_and_split_data(
        data: pd.DataFrame) -> Tuple[np.array, np.array, pd.Series, pd.Series]:
    """
        Деление данных на train/test 0.3 и предобработка данных.
    """
    # Удалим колонки с координатами, так как они только для визуализации.
    df = data.copy()
    df.drop(['lat', 'lng'], axis=1, inplace=True)
    df.drop(['City', 'Country'], axis=1, inplace=True)

    # только на вещественных признаках
    df.drop(['AQI Category', 'CO AQI Category', 'Ozone AQI Category', 'NO2 AQI Category', 'PM2.5 AQI Category'],
            axis=1, inplace=True)
    X = df.drop('AQI Value', axis=1)
    y = df['AQI Value']

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

    return X_train, X_test, y_train, y_test


X_train, X_test, y_train, y_test = preprocess_and_split_data(data)


def train_model(X_train: np.array, X_test: np.array, y_train: pd.Series,
                y_test: pd.Series) -> Tuple[Any, Dict[str, Any]]:
    """
       Обучение модели и запись результатов в словарь метрик.
    """

    # Обучение модели
    clf = KNeighborsRegressor(n_neighbors=10)
    clf.fit(X_train, y_train)
    y_pred = clf.predict(X_test)

    # Сбор метрик
    metrics = {
        "r2": r2_score(y_test, y_pred),
        "MSE": mse(y_test, y_pred)
    }

    # Добавление метрик в словарь
    metrics["model_name"] = "KNRegressor"

    return clf, metrics


clf, metrics = train_model(X_train, X_test, y_train, y_test)


def save_results(clf, model_name):
    """
        Сохранение модели на S3.
    """
    s3_resource = boto3.resource(
        service_name="s3",
        endpoint_url=S3_CONFIG["endpoint_url"],
        aws_access_key_id=S3_CONFIG["aws_access_key_id"],
        aws_secret_access_key=S3_CONFIG["aws_secret_access_key"],
    )
    pickle_byte_obj = pickle.dumps(clf)
    s3_resource.Object(bucket_name="aqi",
                       key=model_name).put(Body=pickle_byte_obj)


save_results(clf, metrics["model_name"])
