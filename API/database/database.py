import psycopg2
import os

from dotenv import load_dotenv


class BaseDAO():
    @staticmethod
    def connection_db():
        load_dotenv()

        connection = psycopg2.connect(host=os.environ.get('PG_HOST'),
                                      port=os.environ.get('PG_PORT'),
                                      user=os.environ.get('PG_USER'),
                                      password=os.environ.get('PG_PASSWORD'),
                                      dbname=os.environ.get('PG_DATABASE'),
                                      sslmode='require')
        connection.autocommit = True
        return connection

    @staticmethod
    def select_value(sql):
        db_execute = BaseDAO.connection_db()
        cursor = db_execute.cursor()
        cursor.execute(sql)
        return cursor.fetchall()

    @staticmethod
    def create_value(sql, record):
        db_execute = BaseDAO.connection_db()
        cursor = db_execute.cursor()
        cursor.execute(sql, record)
        db_execute.commit()
        return cursor.rowcount

    @staticmethod
    def delete_value(sql, id):
        db_execute = BaseDAO.connection_db()
        cursor = db_execute.cursor()
        cursor.execute(sql, (id,))
        db_execute.commit()
        return cursor.rowcount

    @staticmethod
    def patch_value(sql):
        db_execute = BaseDAO.connection_db()
        cursor = db_execute.cursor()
        cursor.execute(sql)
        db_execute.commit()
        return cursor.rowcount