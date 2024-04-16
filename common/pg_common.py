import psycopg
import pandas as pd


def notice_handler(message):
    # print("Received notice:", message)
    # print(dir(message))
    print(message.message_primary)


def connect():
    conn_info = f'host=localhost port=5432 dbname=dvdrental user=postgres password=1234'
    conn = psycopg.connect(conninfo=conn_info)

    # 创建游标对象
    conn.add_notice_handler(notice_handler)
    return conn.cursor()


def connect2():
    conn_info = f'host=localhost port=5432 dbname=dvdrental user=postgres password=1234'
    conn = psycopg.connect(conninfo=conn_info)

    # 创建游标对象
    return conn


def run_sql(cursor, sql_stat):
    cursor.execute(sql_stat)
    display_data(cursor)


def run_sql_pl(cursor, sql_stat):
    cursor.execute(sql_stat)
    display_data(cursor)


def display_data(cursor):
    data = cursor.fetchall()
    col_names = [desc[0] for desc in cursor.description]

    df = pd.DataFrame(data, columns=col_names)
    print(df)
