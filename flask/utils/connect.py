import mysql.connector
import os
import bcrypt
import hashlib
import secrets

class dbConnection(object):

    def __init__(self):
        self.host = "localhost"
        self.user = "root"
        self.password = "R4TK1ll3r4L1F3!!!"
        self.db = "nuisance"
        self.connection = None

    def initMySQL(self):
        self.connection = mysql.connector.connect(host=self.host,
                             database=self.db,
                             user=self.user,
                             password=self.password)

        return self.connection.cursor(prepared=True, dictionary=True)


    def loginUserCheck(self, username, password, token, cursor):
        query = "SELECT id,password FROM user WHERE username = %s AND token = %s"

        user_to_retrieve = (username, token)
        cursor.execute(query, user_to_retrieve)

        rows = cursor.fetchall()

        return str(rows[0]['id']) if len(rows) > 0 and\
                              bcrypt.checkpw(password.encode(), rows[0]['password'].encode())\
                        else False

    def getServicesFromDB(self, cursor):
        query = "SELECT * FROM services"
        cursor.execute(query)

        rows = cursor.fetchall()
        return rows

    def addServiceToCart(self, cursor, serviceid, userid):
        query = """INSERT INTO cart (serviceid,userid) VALUES (%s,%s)"""
        to_parameterize = (int(serviceid), int(userid))

        thrownEx = False

        try:
            cursor.execute(query, to_parameterize)
            self.connection.commit()
        except Exception:
            thrownEx = True

        return not thrownEx

    def getServiceFromCart(self, cursor, userid):
        rows = []

        query = """SELECT name,price FROM services AS S JOIN cart
                       as C ON S.id = C.serviceid WHERE C.userid = %s"""
        useridBind = (userid,)
        cursor.execute(query, useridBind)

        rows = cursor.fetchall()

        return rows

    def registerUser(self, username, password, cursor):
        sql_insert_query = """ INSERT INTO user
                       (username, password, token) VALUES (%s,%s,%s)"""

        token = hashlib.sha256(secrets.token_bytes(64)).hexdigest()

        hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
        user_to_inser = (username, hashed, token)
        thrownEx = False

        try:
            cursor.execute(sql_insert_query, user_to_inser)
            self.connection.commit()
        except Exception:
            thrownEx = True

        return token if not thrownEx else False
