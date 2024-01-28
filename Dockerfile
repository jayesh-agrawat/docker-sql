FROM python:3.9

RUN pip install pandas sqlalchemy psycopg2-binary pyarrow
WORKDIR /app

RUN mkdir data
RUN mkdir data/csv
RUN mkdir data/parquet


COPY ingest_data.py  ingest_data.py

ENTRYPOINT ["python","ingest_data.py"]