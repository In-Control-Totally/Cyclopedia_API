FROM python:3.8-slim-buster
ARG sql_host=None
ENV sql_host=$sql_host
ARG sql_port=None
ENV sql_port=$sql_port
ARG sql_user=None
ENV sql_user=$sql_user
ARG sql_pass=None
ENV sql_pass=$sql_pass
ARG sql_db=None
ENV sql_db=$sql_db


WORKDIR /app



COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
COPY . .

WORKDIR /app/api
CMD ["uvicorn", "main:app", "--reload", "--host", "0.0.0.0"]

EXPOSE 8000
