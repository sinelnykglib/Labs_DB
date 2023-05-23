import csv
import psycopg2
import time
import py7zr
import pandas as pd
import math

start_time = time.time()
print('Start time:', time.strftime('%H:%M:%S'))
# Підключення до бази даних
def connect():
    for attempt in range(30):
        try:
            conn = psycopg2.connect(
                host="db",
                database="db_labs",
                user="postgres",
                password="23102002Papa"
            )
            print("Connection is successful")
            return conn
        except psycopg2.OperationalError as error:
            print(error)
            print("Connection failed. Restarting in 5 seconds...")
            time.sleep(5)

CONN = connect()
CUR = CONN.cursor()


query1 = """
SELECT RegName AS Region, AVG(Ball100) AS PhysAVG19
FROM (SELECT Student_ID, Ball100 FROM Test WHERE Subject_ID = 4 AND TestStatus = 'Зараховано') AS PhysTest
LEFT JOIN (SELECT Student_id, Place_ID, RegName FROM (Student LEFT JOIN Place USING(Place_ID)) AS StudPlace WHERE ExamYear = '2019' AND RegName IS NOT NULL) AS StudReg
USING(Student_ID)
GROUP BY REGNAME
"""
query2 = """
SELECT RegName AS Region, AVG(Ball100) AS PhysAVG20
FROM (SELECT Student_ID, Ball100 FROM Test WHERE Subject_ID = 4 AND TestStatus = 'Зараховано') AS PhysTest
LEFT JOIN (SELECT Student_id, Place_ID, RegName FROM (Student LEFT JOIN Place USING(Place_ID)) AS StudPlace WHERE ExamYear = '2020' AND RegName IS NOT NULL) AS StudReg
USING(Student_ID)
GROUP BY REGNAME
"""

CUR.execute("""SELECT EXISTS (
                SELECT FROM 
                    information_schema.tables 
                WHERE 
                    table_schema LIKE 'public' AND 
                    table_type LIKE 'BASE TABLE' AND
                    table_name = 'flyway_schema_history'
                );""")
result = CUR.fetchall()[0][0]
print(result)
if result == False:

    n_row = 5000
    # Завантажуємо та розпаковуємо файл з даними за 2019 рік
    filename_1 = 'OpenDataZNO2019.7z'
    with py7zr.SevenZipFile(filename_1, 'r') as archive:
        archive.extractall()

    # Завантажуємо та розпаковуємо файл з даними за 2020 рік
    filename_2 = 'OpenDataZNO2020.7z'

    with py7zr.SevenZipFile(filename_2, 'r') as archive:
        archive.extractall()



    # Створення таблиці для даних 2019 року
    data19 = pd.DataFrame(pd.read_csv(r'Odata2019File.csv', sep=";", decimal=",", encoding="Windows-1251", low_memory=False,nrows=n_row))
    data19 = data19.rename(str.lower, axis='columns')

    data20 = pd.DataFrame(pd.read_csv(r'Odata2020File.csv', sep=";", decimal=",", encoding='windows-1251', low_memory=False,nrows=n_row))
    data20 = data20.rename(str.lower, axis='columns')
    def table_exist():
        query = """SELECT EXISTS (
                    SELECT FROM 
                        information_schema.tables 
                    WHERE 
                        table_schema LIKE 'public' AND 
                        table_type LIKE 'BASE TABLE' AND
                        table_name = 'zno_data'
                    );"""
        CUR.execute(query)
        result = CUR.fetchall()[0][0]
        if result == True:
            return True
        return False

    def create_table():
        CUR.execute('''
            CREATE TABLE zno_data(
                Year INT,
                OUTID VARCHAR(1000) PRIMARY KEY,
                Birth DECIMAL,
                SEXTYPENAME CHAR(10),
                REGNAME VARCHAR(1000),
                AREANAME VARCHAR(1000),
                TERNAME VARCHAR(1000),
                REGTYPENAME VARCHAR(1000),
                TerTypeName VARCHAR(1000),
                ClassProfileNAME VARCHAR(1000),
                ClassLangName VARCHAR(1000),
                EONAME VARCHAR(1000),
                EOTYPENAME VARCHAR(1000),
                EORegName VARCHAR(1000),
                EOAreaName VARCHAR(1000),
                EOTerName VARCHAR(1000),
                EOParent VARCHAR(1000),
                UkrTest VARCHAR(1000),
                UkrTestStatus VARCHAR(1000),
                UkrBall100 DECIMAL,
                UkrBall12 DECIMAL,
                UkrBall DECIMAL,
                UkrAdaptScale INT,
                UkrPTName VARCHAR(1000),
                UkrPTRegName VARCHAR(1000),
                UkrPTAreaName VARCHAR(1000),
                UkrPTTerName VARCHAR(1000),
                histTest VARCHAR(1000),
                HistLang VARCHAR(1000),
                histTestStatus VARCHAR(1000),
                histBall100 DECIMAL,
                histBall12 DECIMAL,
                histBall DECIMAL,
                histPTName VARCHAR(1000),
                histPTRegName VARCHAR(1000),
                histPTAreaName VARCHAR(1000),
                histPTTerName VARCHAR(1000),
                mathTest VARCHAR(1000),
                mathLang VARCHAR(1000),
                mathTestStatus VARCHAR(1000),
                mathBall100 DECIMAL,
                mathBall12 DECIMAL,
                mathBall DECIMAL,
                mathPTName VARCHAR(1000),
                mathPTRegName VARCHAR(1000),
                mathPTAreaName VARCHAR(1000),
                mathPTTerName VARCHAR(1000),
                physTest VARCHAR(1000),
                physLang VARCHAR(1000),
                physTestStatus VARCHAR(1000),
                physBall100 DECIMAL,
                physBall12 DECIMAL,
                physBall DECIMAL,
                physPTName VARCHAR(1000),
                physPTRegName VARCHAR(1000),
                physPTAreaName VARCHAR(1000),
                physPTTerName VARCHAR(1000),
                chemTest VARCHAR(1000),
                chemLang VARCHAR(1000),
                chemTestStatus VARCHAR(1000),
                chemBall100 DECIMAL,
                chemBall12 DECIMAL,
                chemBall DECIMAL,
                chemPTName VARCHAR(1000),
                chemPTRegName VARCHAR(1000),
                chemPTAreaName VARCHAR(1000),
                chemPTTerName VARCHAR(1000),
                bioTest VARCHAR(1000),
                bioLang VARCHAR(1000),
                bioTestStatus VARCHAR(1000),
                bioBall100 DECIMAL,
                bioBall12 DECIMAL,
                bioBall DECIMAL,
                bioPTName VARCHAR(1000),
                bioPTRegName VARCHAR(1000),
                bioPTAreaName VARCHAR(1000),
                bioPTTerName VARCHAR(1000),
                geoTest VARCHAR(1000),
                geoLang VARCHAR(1000),
                geoTestStatus VARCHAR(1000),
                geoBall100 DECIMAL,
                geoBall12 DECIMAL,
                geoBall DECIMAL,
                geoPTName VARCHAR(1000),
                geoPTRegName VARCHAR(1000),
                geoPTAreaName VARCHAR(1000),
                geoPTTerName VARCHAR(1000),
                engTest VARCHAR(1000),
                engTestStatus VARCHAR(1000),
                engBall100 DECIMAL,
                engBall12 DECIMAL,
                engDPALevel VARCHAR(1000),
                engBall DECIMAL,
                engPTName VARCHAR(1000),
                engPTRegName VARCHAR(1000),
                engPTAreaName VARCHAR(1000),
                engPTTerName VARCHAR(1000),
                fraTest VARCHAR(1000),
                fraTestStatus VARCHAR(1000),
                fraBall100 DECIMAL,
                fraBall12 DECIMAL,
                fraDPALevel VARCHAR(1000),
                fraBall DECIMAL,
                fraPTName VARCHAR(1000),
                fraPTRegName VARCHAR(1000),
                fraPTAreaName VARCHAR(1000),
                fraPTTerName VARCHAR(1000),
                deuTest VARCHAR(1000),
                deuTestStatus VARCHAR(1000),
                deuBall100 DECIMAL,
                deuBall12 DECIMAL,
                deuDPALevel VARCHAR(1000),
                deuBall DECIMAL,
                deuPTName VARCHAR(1000),
                deuPTRegName VARCHAR(1000),
                deuPTAreaName VARCHAR(1000),
                deuPTTerName VARCHAR(1000),
                spaTest VARCHAR(1000),
                spaTestStatus VARCHAR(1000),
                spaBall100 DECIMAL,
                spaBall12 DECIMAL,
                spaDPALevel VARCHAR(1000),
                spaBall DECIMAL,
                spaPTName VARCHAR(1000),
                spaPTRegName VARCHAR(1000),
                spaPTAreaName VARCHAR(1000),
                spaPTTerName VARCHAR(1000)
            );
        ''')
        print('Table is created.')

    if table_exist():
        print("Table exists.")
    else:
        create_table()
        print("Table doesn't exist. Creating table...")

    def check_row_not_in_db(columns_string, values_string):
        columns_string = columns_string.split(', ')
        values_string = [None if isinstance(x, float) and math.isnan(x) else x for x in values_string]
        query = "SELECT COUNT(*) FROM zno_data WHERE "
        for i in range(len(columns_string)):
            if i > 0:
                query += " AND "
            query += "{} = %s".format(columns_string[i])
        CUR.execute(query, values_string)
        result = CUR.fetchone()
        return result == (0,)


    def insert_data(df, conn, year):
        ignore_num = 0
        columns = [i for i in df.columns]
        values_string = ', '.join(['%s'] * (len(columns) + 1))
        columns_string = ', '.join(['Year'] + columns)
        left = []
        i = 0

        try:
            CUR.execute(f"SELECT COUNT(*) FROM zno_data WHERE year = {year}")
            ignore_num = CUR.fetchone()[0]

        except psycopg2.OperationalError:
            insert_data(df, CONN, year)

        for i, row in enumerate(df.head(n_row).values):
            row = [year, *row]
            left.append(row)
            if i >= ignore_num:
                if False and not check_row_not_in_db(columns_string, row):
                    print('Duplicates...')
                    continue
                query = f"INSERT INTO zno_data ({columns_string}) VALUES ({values_string})"
                try:
                    CUR.execute(query, row)
                    if i % 100 == 0:
                        conn.commit()
                        left = []
                        print(f"{i} rows inserted.")

                except psycopg2.OperationalError:
                    print("Reconnection...")
                    for y in left:
                        CUR.execute(query, y)
                    CUR.execute(query, row)
                    if i % 100 == 0:
                        conn.commit()
                        cash = []
                        print(f"{i} rows inserted.")
            i += 1
        conn.commit()
        print(f"{i} rows inserted.")
        print(f"{year} year is inserted.")

    for attempt in range(1):
        try:
            insert_data(data19, CONN, 2019)
            insert_data(data20, CONN, 2020)
            print("Inserting...")
        except psycopg2.OperationalError as error:
            print(error)
            CONN = connect()
            insert_data(data19, CONN, 2019)
            insert_data(data20, CONN, 2020)
            print("Inserting failed. Connecting and inserting...")
            time.sleep(5)

    query1 = """
            SELECT REGNAME, AVG(PhysBall100)
            FROM zno_data
            WHERE PhysTestStatus = 'Зараховано' AND Year = 2019
            GROUP BY REGNAME
            """
    query2 = """
            SELECT REGNAME, AVG(PhysBall100)
            FROM zno_data
            WHERE PhysTestStatus = 'Зараховано' AND Year = 2020
            GROUP BY REGNAME
            """


# виконання запиту для 2019 року
CUR.execute(query1)
results_2019 = CUR.fetchall()
print(results_2019)
# виконання запиту для 2020 року
CUR.execute(query2)
results_2020 = CUR.fetchall()
print(results_2020)

# запис результатів до CSV-файлу
with open('../AVG_Phys.csv', mode='w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['Region', 'AVG Phys in 2019', 'AVG Phys in 2020'])
    for row_2019, row_2020 in zip(results_2019, results_2020):
        region = row_2019[0]
        avg_2019 = row_2019[1]
        avg_2020 = row_2020[1]
        writer.writerow([region, avg_2019, avg_2020])

print("The results have been saved to 'AVG_Phys.csv' file")

elapsed_time = round(time.time() - start_time, 2)
print('Working time:', elapsed_time)