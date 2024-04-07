FROM python:3.11-slim

RUN mkdir /streamlit
COPY requirements.txt /streamlit
#COPY ./Images /streamlit

WORKDIR /streamlit

RUN pip install --no-cache-dir -r requirements.txt
COPY . /streamlit
EXPOSE 8501
CMD ["streamlit", "run", "app.py"]