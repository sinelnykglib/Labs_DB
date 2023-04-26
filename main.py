import csv
import psycopg2



POSTGRES_DB = 'db_labs'


username = 'postgres'
password = '23102002Papa'
database = 'db_labs'

input_csv_file1 = 'Odata2019File.csv'
input_csv_file2 = 'Odata2020File.csv'

query_create = '''
CREATE TABLE IF NOT EXISTS phys19_20
(
  id      char(50)  NOT NULL ,
  phys_region char(50) ,
  phystest char(20) ,
  phystest_status char(20) ,
  physball numeric ,
  year numeric ,
  num numeric ,
  numcsv numeric ,
  CONSTRAINT pk_id PRIMARY KEY (id)
);
'''

query_ins = '''
insert into phys19_20(id, phys_region, phystest, phystest_status, physball, year, num, numcsv) values (%s, %s, %s, %s, %s, %s, %s, %s) 
'''

query_count_rows = '''
select count(*) from phys19_20
'''

query_find_last = '''
select numcsv from phys19_20 where num = (select count(*) from phys19_20)
'''

query_start_sec = '''
select count(*) from phys19_20 where year=2020
'''

conn = psycopg2.connect(user=username, password=password, dbname=database, host='db', port=5432)

with conn:
    cur = conn.cursor()
    cur.execute(query_create)
    cur.execute(query_count_rows)
    count_records = cur.fetchone()[0]

    with open(input_csv_file1, 'r', encoding='windows-1251') as inf:
        reader = csv.DictReader(inf, delimiter=';')
        cur.execute(query_start_sec)
        count_st_last = int(float(cur.fetchone()[0]))
        if count_st_last == 0:
            if count_records != 0:
                cur.execute(query_find_last)
                count_csv = int(cur.fetchone()[0])
                for i in range(count_csv):
                    next(reader)
            else:
                count_csv = 0

            for row in reader:
                if row['physTestStatus'] == 'Зараховано':
                    values1 = (row['OUTID'], row['physPTRegName'], row['physTest'], row['physTestStatus'], float(row['physBall100'].replace(",", ".")), 2019, count_records+1, count_csv+1)
                    cur.execute(query_ins, values1)
                    count_records += 1
                    conn.commit()
                count_csv += 1

    with open(input_csv_file2, 'r', encoding='windows-1251') as inf:
        reader = csv.DictReader(inf, delimiter=';')
        cur.execute(query_find_last)
        count_csv = int(float(cur.fetchone()[0]))
        cur.execute(query_start_sec)
        count_st_last = int(float(cur.fetchone()[0]))
        if count_st_last == 0:
            count_csv = 0
        else:
            for i in range(count_csv):
                next(reader)

        for row in reader:
            if row['physTestStatus'] == 'Зараховано':
                values2 = (row['OUTID'], row['physPTRegName'], row['physTest'], row['physTestStatus'], float(row['physBall100'].replace(",", ".")), 2020, count_records+1, count_csv+1)
                cur.execute(query_ins, values2)
                count_records += 1
                conn.commit()
            count_csv += 1

    cur.execute('create view Help as select phys_region, avg(physball) as avg_19  from phys19_20  where year = 2019 group by phys_region')
    cur.execute('create view Help2 as select phys_region, avg(physball) as avg_20 from phys19_20  where year = 2020 group by phys_region')
    cur.execute('select *  from Help join Help2 using(phys_region)')

    with open('ZNOphys19_20_results.csv', 'w', newline='') as csvfile:
        fieldnames = ['region', 'avgBall2019', 'avgBall2020', 'higherBallInYear']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        better = '2019'
        for row in cur:
            if row[2] > row[1]:
                better = 2020
            else:
                better = 2019
            writer.writerow({'region': row[0], 'avgBall2019': row[1], 'avgBall2020': row[2], 'higherBallInYear': better})

    cur.execute('drop view Help')
    cur.execute('drop view Help2')

    conn.commit()