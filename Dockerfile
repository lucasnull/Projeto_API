FROM python:3.8.10

COPY /API /proj001/API
COPY requirements.txt /proj001

WORKDIR proj001

RUN pip install -r requirements.txt

EXPOSE 8001

CMD ["uvicorn", "src.main:app", "--host=127.0.0.1", "--reload"]