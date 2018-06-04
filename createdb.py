import psycopg2
import config
import urllib.parse as urlparse

def createtables():

    url = urlparse.urlparse(config.database)

    connection = psycopg2.connect(
        database=url.path[1:],
        user=url.username,
        password=url.password,
        host=url.hostname,
        port=url.port
    )
    cursor = connection.cursor()

    cursor.execute('''CREATE SEQUENCE IF NOT EXIST public.chats_id_seq
      INCREMENT 0
      MINVALUE 0
      MAXVALUE 0
      START 0
      CACHE 0;
    ALTER TABLE public.chats_id_seq''')
    connection.commit()

    cursor.execute('''
       CREATE TABLE IF NOT EXIST chats
(
  id bigint NOT NULL DEFAULT nextval('chats_id_seq'::regclass),
  uid bigint NOT NULL,
  state jsonb DEFAULT '{}'::jsonb,
  created_at timestamp with time zone NOT NULL DEFAULT now(),
  updated_at timestamp with time zone NOT NULL DEFAULT now(),
  CONSTRAINT chats_pkey PRIMARY KEY (id),
  CONSTRAINT chats_uid_key UNIQUE (uid)
)''')
    connection.commit()

    connection.close()