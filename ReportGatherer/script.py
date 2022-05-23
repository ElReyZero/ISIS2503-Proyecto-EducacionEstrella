import sys
import psycopg2 as pg
import csv

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
        print("Connected to database")
        #cur.execute()
        #db_version = cur.fetchall()
        #print(db_version)
        cur.close()
    except (Exception, pg.DatabaseError) as error:
        print(error)
    except (KeyboardInterrupt):
        sys.exit()
    finally:
        if conn:
            conn.close()


def insertEstudiantes(conn, cur):
    with open(r'C:\Users\ElRey\Documents\Scripts\ISIS2503-Proyecto-EducacionEstrella\ReportGatherer\estudiantes.csv', 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        cont = 0
        for row in reader:
            if len(row[3]) > 50:
                row[3] = row[3][:50]
            cur.execute(
            'INSERT INTO public."ModuloFinanciero_estudianteestrella" VALUES (%s, %s, %s, %s, %s, %s, %s)',
            row)
            cont += 1
            print("\r" + str(cont), end="")
        conn.commit()
        cur.close()

def insertSolicitudes(conn, cur):
    with open(r'C:\Users\ElRey\Documents\Scripts\ISIS2503-Proyecto-EducacionEstrella\ReportGatherer\solicitudes.csv', 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        cont = 0
        for row in reader:
            if row[3] == "":
                row[3] = None
                row[6] = 'false'
            cur.execute(
            'INSERT INTO public."ModuloFinanciero_solicitudcredito" VALUES (%s, %s, %s, %s, %s, %s, %s)', row)
            cont += 1
            print(f"\r{cont}/1000", end="\n")
        conn.commit()

if __name__ == '__main__':
    connect()