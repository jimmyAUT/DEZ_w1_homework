# DEZ_w1_homework

## Data Engineering Zoomcamp Week 1 homework

Q1: Run docker with the python:3.12.8
    **Ans: pip 24.3.1**
        ```bash
        docker run -it --entrypoint bash python:3.12.8

        pip --version
        >>> pip 24.3.1 from /usr/local/lib/python3.12/site-packages/pip (python 3.12)
        ```

Q2: Given the following docker-compose.yaml, what is the hostname and port that pgadmin should use to connect to the postgres database?
    **Ans: Hostname is "db", port is "5432"**
        ```yaml
        services:
        db:
            container_name: postgres
            image: postgres:17-alpine
            environment:
            POSTGRES_USER: 'postgres'
            POSTGRES_PASSWORD: 'postgres'
            POSTGRES_DB: 'ny_taxi'
            ports:
            - '5433:5432'
            volumes:
            - vol-pgdata:/var/lib/postgresql/data

        pgadmin:
            container_name: pgadmin
            image: dpage/pgadmin4:latest
            environment:
            PGADMIN_DEFAULT_EMAIL: "pgadmin@pgadmin.com"
            PGADMIN_DEFAULT_PASSWORD: "pgadmin"
            ports:
            - "8080:80"
            volumes:
            - vol-pgadmin_data:/var/lib/pgadmin  

        volumes:
        vol-pgdata:
            name: vol-pgdata
        vol-pgadmin_data:
            name: vol-pgadmin_data
        ```

Q3: During the period of October 1st 2019 (inclusive) and November 1st 2019 (exclusive), how many trips, respectively, happened:

1. Up to 1 mile:

    **Ans: 104802**
        ```sql
        SELECT COUNT(*) FROM "green_tripdata_2019-10"
        WHERE lpep_pickup_datetime >= '2019-10-01'
        AND lpep_dropoff_datetime < '2019-11-01'
        AND trip_distance <= 1;
        ```

2. In between 1 (exclusive) and 3 miles (inclusive):

    **Ans: 198924**
        ```sql
        SELECT COUNT(*) FROM "green_tripdata_2019-10"
        WHERE lpep_pickup_datetime >= '2019-10-01'
        AND lpep_dropoff_datetime < '2019-11-01'
        AND trip_distance > 1 AND trip_distance <= 3;
        ```

3. In between 3 (exclusive) and 7 miles (inclusive):

    **Ans: 109603**
        ```sql
        SELECT COUNT(*) FROM "green_tripdata_2019-10"
        WHERE lpep_pickup_datetime >= '2019-10-01'
        AND lpep_dropoff_datetime < '2019-11-01'
        AND trip_distance > 3 AND trip_distance <= 7;
        ```

4. In between 7 (exclusive) and 10 miles (inclusive):

    **Ans: 27678**
        ```sql
        SELECT COUNT(*) FROM "green_tripdata_2019-10"
        WHERE lpep_pickup_datetime >= '2019-10-01'
        AND lpep_dropoff_datetime < '2019-11-01'
        AND trip_distance > 7 AND trip_distance <= 10;
        ```

5. Over 10 miles:

    **Ans: 35189**
        ```sql
        SELECT COUNT(*) FROM "green_tripdata_2019-10"
        WHERE lpep_pickup_datetime >= '2019-10-01'
        AND lpep_dropoff_datetime < '2019-11-01'
        AND trip_distance > 10;
        ```

Q4: Longest trip for each day. Which was the pick up day with the longest trip distance? Use the pick up time for your calculations.

**Ans: 2019-10-11**
    ```sql
    SELECT DATE(lpep_pickup_datetime), trip_distance
    FROM "green_tripdata_2019-10"
    WHERE DATE(lpep_pickup_datetime) = DATE(lpep_dropoff_datetime)
    ORDER BY trip_distance DESC
    LIMIT 5;
    ```

Q5: Which were the top pickup locations with over 13,000 in total_amount (across all trips) for 2019-10-18?
Consider only lpep_pickup_datetime when filtering by date.
    **Ans:East Harlem North, East Harlem South, Morningside Heights**
        ```sql
        SELECT t."PULocationID", z."Zone" ,SUM(t.total_amount)
        FROM "green_tripdata_2019-10" t
        JOIN "taxi_zone_lookup" z
        ON t."PULocationID" = z."LocationID"
        WHERE DATE(t.lpep_pickup_datetime) = '2019-10-18'
        GROUP BY t."PULocationID", z."Zone"
        HAVING SUM(t.total_amount) > 13000
        ```
Q6: For the passengers picked up in October 2019 in the zone name "East Harlem North" which was the drop off zone that had the largest tip?
    **Ans: JFK Airport**
        ```sql
        SELECT
            pz."Zone" AS "pickup_zone",
            dz."Zone" AS "dropoff_zone",
            t.tip_amount
        FROM "green_tripdata_2019-10" t
        JOIN "taxi_zone_lookup" pz
            ON t."PULocationID" = pz."LocationID"
        JOIN "taxi_zone_lookup" dz
            ON t."DOLocationID" = dz."LocationID"
        WHERE DATE(t.lpep_pickup_datetime) BETWEEN '2019-10-01' AND '2019-10-31'
            AND pz."Zone" = 'East Harlem North'
        ORDER BY t.tip_amount DESC
        LIMIT 1
        ```
