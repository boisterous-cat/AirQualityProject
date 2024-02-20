from fastapi import FastAPI
import os
import numpy as np
import uvicorn
from pydantic import BaseModel
import pandas as pd
import pickle
import gzip
import json
from typing import List, Optional
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from fastapi.encoders import jsonable_encoder
from pandas import json_normalize
from data_request_model import *
import pandas as pd

from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split, cross_val_score, KFold
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import r2_score, mean_squared_error
from sklearn.neighbors import KNeighborsRegressor

with gzip.open('Data/pickle_model.pkl', 'rb') as ifp:
    MODEL = pickle.load(ifp)

app = FastAPI(title="Ham or Spam API", description="API to predict if a SMS is ham or spam")


@app.get("/")
def read_root():
    return {"message": "Welcome from the API"}

def predict_model(co, no, ozone, pm2):
    prediction = MODEL.predict(pd.DataFrame([[co, no, ozone, pm2]], columns=['CO AQI Value', 'NO2 AQI Value', 'Ozone AQI Value', 'PM2.5 AQI Value']))
    return prediction

@app.post("/predict")
def predict(parameters: MlRequest):
    return predict_model(parameters.co, parameters.no, parameters.ozone, parameters.pm2)[0]


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000, log_level="info")
