FROM python:3.12-slim

RUN apt-get update
RUN apt-get install -y build-essential
RUN rm -rf /var/lib/apt/lists/*


WORKDIR /app
COPY expenser/requirements.txt ./expenser/
RUN pip install --no-cache-dir -r expenser/requirements.txt
COPY expenser ./expenser

EXPOSE 8000
WORKDIR /app
CMD ["sh", "-c", "python expenser/manage.py runserver 0.0.0.0:8000"]