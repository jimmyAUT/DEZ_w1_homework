#!/usr/bin/env python
# coding: utf-8

import pandas as pd
from sqlalchemy import create_engine
from time import time

# download the data 
import os
import argparse

def main(params):
    # Define variables
    user = params.user
    password = params.password
    host = params.host
    port = params.port
    trip_url = params.trip_url
    zone_url = params.zone_url
    db = params.db
    trip_table_name = params.trip_table_name
    zone_table_name = params.zone_table_name
   
    trip_file = "trip_data"
    zone_file = "zone_data"
    if trip_url.endswith("csv.gz"):
        trip_file = f"{trip_file}.csv.gz"
    else:
        trip_file = f"{trip_file}.csv"
        
    os.system(f"wget {trip_url} -O {trip_file}")
    print(f"Downloaded {trip_file}")

    if zone_url.endswith("csv.gz"):
        zone_file = f"{zone_file}.csv.gz"
    else:
        zone_file = f"{zone_file}.csv" 

    os.system(f"wget {zone_url} -O {zone_file}")
    print(f"Downloaded {zone_file}")



    df_trip_iter = pd.read_csv(trip_file, iterator=True, chunksize=100000)
    df_trip = next(df_trip_iter)

    # transforming datetime datatype
    df_trip['lpep_pickup_datetime'] = pd.to_datetime(df_trip['lpep_pickup_datetime'])
    df_trip['lpep_dropoff_datetime'] = pd.to_datetime(df_trip['lpep_dropoff_datetime'])


    # prepare zone date
    df_zone = pd.read_csv(zone_file)   

    # Create sqlalchemy connection engine
    engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{db}')

    # Build tripdata table on postgres
    df_trip.head(0).to_sql(name=trip_table_name, con=engine, if_exists="replace")

    # Load first chunk of data to postgres
    df_trip.to_sql(name=trip_table_name, con=engine, if_exists="append")

    # Load the rest of chunk
    while True:
        try:
            t_start = time()
            
            df_trip = next(df_trip_iter)
            df_trip['lpep_pickup_datetime'] = pd.to_datetime(df_trip['lpep_pickup_datetime'])
            df_trip['lpep_dropoff_datetime'] = pd.to_datetime(df_trip['lpep_dropoff_datetime'])
            df_trip.to_sql(name=trip_table_name, con=engine, if_exists="append")
            
            t_end = time()
            print("load the next chunk..., spent %.3f second" %(t_end-t_start))
        except StopIteration:
            print("Finished ingesting data into the postgres database")
            break
        
    # load zone date to postgres
    df_zone.head(0).to_sql(con=engine, name='taxi_zone_lookup', if_exists='replace')
    df_zone.to_sql(con=engine, name=zone_table_name, if_exists='append')



if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Ingest csv data to postgres')

    # User
    parser.add_argument('--user', required=True,help='user name')
    # Password
    parser.add_argument('--password', required=True,help='Password for postgres')
    # host
    parser.add_argument('--host', required=True,help='host address')
    # port
    parser.add_argument('--port', required=True,help='port')
    # DB name
    parser.add_argument('--db', required=True,help='database name')
    # table name
    parser.add_argument('--trip_table_name', required=True,help='table where to write trip data into')
    parser.add_argument('--zone_table_name', required=True,help='table where to write zone data into')
    # url of trip data download
    parser.add_argument('--trip_url', required=True,help='trip data url')
    # url of zone look up data download
    parser.add_argument('--zone_url', required=True,help='zone data url')

    args = parser.parse_args()

    main(args)