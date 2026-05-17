FROM python:3.11-slim

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8501

<<<<<<< HEAD
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
=======
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
>>>>>>> 7028d1e4f1feb1a8345e4574fe949030da8577ca
