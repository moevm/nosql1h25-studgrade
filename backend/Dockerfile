FROM python:3.12

WORKDIR /app

COPY ./requirements.txt .

RUN python3 -m pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["python3", "-m", "src.main"]
