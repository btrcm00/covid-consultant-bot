FROM python:3.8

WORKDIR /app
COPY setup.py .
RUN pip install -e .

WORKDIR /app/backend
COPY . /app/backend
RUN pip install -r requirements.txt

EXPOSE 8000
CMD ["sh","-c","gunicorn -w 4 -k uvicorn.workers.UvicornWorker app:app"]