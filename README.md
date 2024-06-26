# AirQualityProject
***Предсказание качества воздуха***

Под загрязнением воздуха понимается выброс в воздух загряняющих веществ, которые наносят вред здоровью человека, способствует истощению озонового слоя, что в свою очередь ведет к изменению климата. Объем научных данных о негативном влиянии загрязнения воздуха на различные аспекты здоровья заметно возрос со времени последнего обновления глобальных рекомендаций ВОЗ в 2005 году. 
Все это актуализирует необходимость анализа качества воздуха, анализа концентраций загрязняющих веществ.

В качестве материала исследования выступает набор данных, взятый с сайта Kaggle и ВОЗ (под вопросом). Данные содержат показатели "классических" загрязнителей - мелкодисперсные частицы (МЧ), озон (O₃), диоксид азота (NO₂), диокид серы (SO₂), угарный газ (CO). Особый интерес среди мелкодисперсных представлют частицы с диаметром 10 и 2.5 микрон (мкм) (PM₁₀ и PM₂.₅, соответственно), так как способны проникать глубоко в легкие, а частицы PM₂.₅ могут проникать даже в кровоток. Именно эти частицы и представлены в наборе анализируемых данных.


***План работы***:
1) Изучить набор данных, взятых с сайта Kaggle и ВОЗ
2) Подобрать и построить статистическую модель
3) Натренировать модель и получить коэффициеты
4) Запрограммировать пользовательский интерфейс (или телеграмм бот, пока в раздумьях) для запроса параметров для прогнозирования
5) Передать параметры в модель и получить прогноз
6) Отобразить пользователю прогнозные значения (через бот или веб-сервис)

***Реализовано***:
1) Предобработаны данные как для визуализации, так и для обучения
2) Проведены ML эксперименты
3) Лучшая модель сохранена в хранилище YandexCLoud
4) Создан веб-сервис на FastAPI (также развернут на https://aqi-api-service.onrender.com)
5) Создано веб-приложение Streamlit
6) Создан телеграмм-бот https://t.me/airQualityPredictionBot

***Идеи, которые скорее всего не успеем реализовать***:
1) Подключить определение геолокации, чтобы показывать качество воздуха по определенной области нахождения пользователя
2) Разработать прогноз на десять лет
3) (может еще что-нибудь придумаю)

***Описание датасета***   
В качестве данных для анализа используются два датасета, дополняющих друг друга: global air pollution dataset, AQI and Lat Long of Countries. Для исторического отслеживания изменения индекса качества воздуха используется air_index.

**Features of global air pollution dataset**   
Country : Название страны  
City : Название города  
AQI Value : Показатель индекса воздуха  
AQI Category : AQI категория индекса воздуха  
CO AQI Value : AQI значение угарного газа  
CO AQI Category : AQI категория угарного газа  
Ozone AQI Value : AQI значение озона  
Ozone AQI Category : AQI категории озона  
NO2 AQI Value : AQI значение диоксида азота  
NO2 AQI Category : AQI категория диоксида азота  
PM2.5 AQI Value : AQI значение твердых частиц диаметром 2.5 микрометра или менее  
PM2.5 AQI Category : AQI категория твердых частиц диаметром 2.5 микрометра или менее 

**Features of AQI and Lat Long of Countries dataset**  
Помимо описанного выше набора данных имеет также:  
lat : Широта    
lng : Долгота  

**Features of air_index dataset**  
Rank : Рейтинг на 2022    
Countries : Страна  
City : Город  
2022 : AQI на 2022  
JAN-DEC : AQI по месяцам 2022  
2021 - 2017 : AQI по годам  


***Описание docker-compose***
1. Состав образа  
    1.1. Телеграм-бот  
        Ссылка - https://t.me/airQualityPredictionBot  
        Описание -  https://github.com/boisterous-cat/AirQualityProject/blob/main/TgBot_README.md    
    1.2 Веб-интерфейс  
        Работает на внутреннем порту 8501.  
        Описание - https://github.com/boisterous-cat/AirQualityProject/blob/main/Streamlit_README.md  
    1.3 Сервис кеширования Redis  
    1.4 Веб-сервис    
         Веб-сервис работает на внутреннем порту 8000. Сервис предоставляет следующие методы:
```javascript
   "/":{
         "get":{
            "summary":"Read Root",
             "responses":{
               "200":{ }
            }
         }
        },
   "/predict":{
         "post":{
            "summary":"Get one prediction",
            "requestBody":{
               "content":{
                  "application/json":{
                     "schema":{
                        "$ref":"#/components/schemas/MlRequest"
                     }
                  }
               },
               "required":true
            },
         }
      },
   "/predict_items":{
         "post":{
            "summary":"Get predictions for several items",
            "requestBody":{
               "content":{
                  "application/json":{
                     "schema":{
                        "items":{
                           "$ref":"#/components/schemas/MlRequest"
                        },
                        "type":"array",
                        "title":"Items"
                     }
                  }
               },
               "required":true
            },
         }
      },
  "/get_data":{
     "post":{
        "summary":"Get predictions for location",
        "requestBody":{
           "content":{
              "application/json":{
                 "schema":{
                    "$ref":"#/components/schemas/UserLocation"
                 }
              }
           },
           "required":true
        },
     }
  }
 }
```


***Ссылка на гугл диск*** - https://drive.google.com/drive/folders/1kCMOQM4ePzumjhv7XqXKkDg7japR5vV9?usp=sharing  
***Ссылка на телеграм бота*** - https://github.com/boisterous-cat/tgBot/blob/main/README.md  
***Список команды*** - Довгаль Анастасия Александровна  
***Куратор*** - Козлов Кирилл









