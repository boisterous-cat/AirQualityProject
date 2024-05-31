FROM python:3.11-slim

RUN mkdir /fastapi

COPY requirements.txt /fastapi

WORKDIR /fastapi

RUN pip install --no-cache-dir -r requirements.txt
RUN apt-get update && apt-get install -y --no-install-recommends apt-utils
RUN apt-get -y install curl
RUN apt-get install libgomp1

COPY . /fastapi

EXPOSE 8000:8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]