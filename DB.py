import psycopg2
import urllib.parse as urlparse


class DBLayer:
    def __init__(self, database):

        url = urlparse.urlparse(database)

        self.connection = psycopg2.connect(
            database=url.path[1:],
            user=url.username,
            password=url.password,
            host=url.hostname,
            port=url.port
        )
        self.cursor = self.connection.cursor()

    def getState(self, uid):
        self.cursor.execute("""
                SELECT state FROM chats WHERE uid = %s LIMIT 1
                """, [uid])

        if self.cursor.rowcount == 1:
            state, = self.cursor.fetchone()
            return state
        else:
            return {}



    def getUserBrand(self, uid):
        self.cursor.execute("""
                SELECT user_brand FROM chats WHERE uid = %s LIMIT 1
                """, [uid])

        if self.cursor.rowcount == 1:
            state, = self.cursor.fetchone()
            if state == 'null':
                return None
            else:
                return state
        else:
            return None



    def getBrand(self, message):
       self.cursor.execute("""
                select Auto_name
                from Brand, plainto_tsquery(%s) as query
                where to_tsvector(Brand_name) @@ query = true
                """, [message.lower()])
       if self.cursor.rowcount == 1:
            str, = self.cursor.fetchone()
            return str
       else:
           return None


    def updateState(self, uid, new_state):
        self.cursor.execute("""
                INSERT INTO chats (uid) VALUES (%(uid)s)
                ON CONFLICT (uid)
                DO UPDATE
                updated_at = now()
                """, {'uid': uid})

    def updateBrand(self, uid, new_brand):
        self.cursor.execute("""
                INSERT INTO chats (uid, user_brand) VALUES (%(uid)s, %(new_brand)s)
                ON CONFLICT (uid)
                DO UPDATE
                SET user_brand = %(new_brand)s,
                updated_at = now()
                """, {'uid': uid, 'new_brand': new_brand})
