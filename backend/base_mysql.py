import pymysql

class MYSQL:
    def connectDatabase(self):
        connection = pymysql.connect(host='localhost',
                                     user='root',
                                     password='12345678',
                                     db='spoc',
                                     charset='utf8')
        cursor = connection.cursor()
        return connection, cursor

    def closeDatabase(self, connection, cursor):
        connection.close()
        cursor.close()