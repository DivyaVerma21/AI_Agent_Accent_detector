FROM python:3.11-slim
WORKDIR /app
COPY packages.txt ./
RUN apt-get update && apt-get install -y --no-install-recommends git
COPY requirements.txt ./
RUN pip install --upgrade pip && pip install -r requirements.txt

COPY . .

EXPOSE 8501

CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]