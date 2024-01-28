#!/usr/bin/env python
# coding: utf-8
import argparse
import os
from time import time
import pandas as pd
from sqlalchemy import create_engine

def main(parser):
    user = parser.user
    password = parser.password
    host = parser.host
    port = parser.port
    database = parser.database
    table = parser.table
    url = parser.url

    # download the csv file
    csv_name = "output.csv"
    os.system(f"curl {url} -o {csv_name}")

    engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{database}')
    # print(pd.io.sql.get_schema(df,name="yellow_tax",con=engine))
    df_iter = pd.read_csv("./data/yellow_taxi.csv",iterator=True,chunksize=100000)

    df = next(df_iter)
    # len(df)
    df.tpep_pickup_datetime = pd.to_datetime(df.tpep_pickup_datetime)
    df.tpep_dropoff_datetime = pd.to_datetime(df.tpep_dropoff_datetime)

    df.head(n=0).to_sql(name=table,con=engine,if_exists='replace')
    df.to_sql(name=table,con=engine,if_exists='append')

    while True:
        t_start = time()
        df = next(df_iter)
        df.tpep_pickup_datetime = pd.to_datetime(df.tpep_pickup_datetime)
        df.tpep_dropoff_datetime = pd.to_datetime(df.tpep_dropoff_datetime)

        df.to_sql(name=table,con=engine,if_exists='append')

        t_end = time()
        print("Inserted another data chunk, took %.3f second"% (t_end - t_start))
    
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Ingest CSV to Postgres DB")

    # user
    # password
    # host
    # port
    # database
    # table
    # url of the csv file

    parser.add_argument('--user', help='user name')
    parser.add_argument('--password', help='password')
    parser.add_argument('--host', help='host')
    parser.add_argument('--port', help='port')
    parser.add_argument('--database', help='database')
    parser.add_argument('--table', help='table')
    parser.add_argument('--url', help='url')
    args = parser.parse_args()
    main(args)