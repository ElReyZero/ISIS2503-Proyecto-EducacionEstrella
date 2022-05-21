import sys
import psycopg2 as pg


def connect():
    conn = None

    try:
        
        conn = pg.connect(
            host = "educacion-estrella-db.cgg09hgjbyvt.us-east-1.rds.amazonaws.com",
            database = "educacionEstrellaDB",
            user = "eeUser",
            password = "isis2503"
        )

        cur = conn.cursor()

        cur.execute('SELECT version()')
        db_version = cur.fetchone()

        print(db_version)
        cur.close()
    except (Exception, pg.DatabaseError) as error:
        print(error)
    except (KeyboardInterrupt):
        sys.exit()
    finally:
        if conn:
            conn.close()
            print("holi")

if __name__ == '__main__':
    connect()