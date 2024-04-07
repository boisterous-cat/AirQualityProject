FROM python:3.11-slim

RUN mkdir /fastapi

COPY requirements.txt /fastapi

WORKDIR /fastapi

RUN pip install --no-cache-dir -r requirements.txt

COPY . /fastapi

EXPOSE 8000:8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]