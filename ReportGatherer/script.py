import sys
import psycopg2 as pg
import csv
import traceback
from openpyxl import Workbook
from openpyxl.workbook.protection import WorkbookProtection
from openpyxl.styles import Font
import os
from datetime import datetime
from multiprocessing import Process, Manager


def createReport():
    manager = Manager()
    queries = manager.dict()
    procesoCarrera = Process(target=query, args=(queries, "carrera"))
    procesoUniversidad = Process(target=query, args=(queries,"universidad"))
    procesoCiudad = Process(target=query, args=(queries,"ciudad"))
    procesoGenero = Process(target=query, args=(queries,"genero"))
    procesoEdad = Process(target=query, args=(queries,"edad"))

    procesoCarrera.start()
    procesoUniversidad.start()
    procesoCiudad.start()
    procesoGenero.start()
    procesoEdad.start()

    procesoCarrera.join()
    procesoUniversidad.join()
    procesoCiudad.join()
    procesoGenero.join()
    procesoEdad.join()

    if len(queries) != 5:
        return False

    queryToExcel(queries)
    print("Done")
    return True

def query(queries, criterio):
    try:
        conn = pg.connect(
            host = "educacion-estrella-db.cgg09hgjbyvt.us-east-1.rds.amazonaws.com",
            database = "educacionEstrellaDB",
            user = "eeUser",
            password = "isis2503"
            )
        cursor = conn.cursor()
        print("Connected to database")

        query = f"""SELECT creds.criterio, creds.creditos_aprobados, tasa.tasa_aprobacion, recaudo.recaudo, mora.cuotas_en_mora
        FROM 
            (
            SELECT COUNT(*) creditos_aprobados, ee.{criterio} as criterio
            FROM public."ModuloFinanciero_solicitudcredito" s, public."ModuloFinanciero_estudianteestrella" ee
            WHERE s.estudiante_id = ee.id AND s."fechaAprobacion" IS NOT NULL
            GROUP BY ee.{criterio}
            ) creds, 
            (
            SELECT b.{criterio} as criterio, 
                CASE WHEN a.creditos_aprobados IS NOT NULL THEN ROUND((a.creditos_aprobados/b.creditos_totales),2) 
                ELSE 0 END AS tasa_aprobacion
            FROM (
                SELECT CAST (COUNT(*) as numeric(9,2))creditos_aprobados, ee.{criterio}
                FROM public."ModuloFinanciero_solicitudcredito" s, public."ModuloFinanciero_estudianteestrella" ee
                WHERE s.estudiante_id = ee.id AND s."fechaAprobacion" IS NOT NULL
                GROUP BY ee.{criterio}
                ) a RIGHT JOIN
                (
                    SELECT CAST (COUNT(*) as numeric(9,2)) creditos_totales, ee.{criterio}
                    FROM public."ModuloFinanciero_solicitudcredito" s,public."ModuloFinanciero_estudianteestrella" ee
                    WHERE s.estudiante_id = ee.id    
                    GROUP BY ee.{criterio}
                ) b
                ON a.{criterio} = b.{criterio}
            )tasa,
            (
                SELECT {criterio} as criterio, SUM("montoAPagar") as recaudo
                FROM public."ModuloFinanciero_solicitudcredito" s, public."ModuloFinanciero_estudianteestrella" ee
                WHERE "fechaAprobacion" BETWEEN TO_DATE('2022-01-01', 'YYYY-MM-DD') AND 
                TO_DATE('2022-06-30', 'YYYY-MM-DD') AND 
                pagado AND
                s.estudiante_id = ee.id
                GROUP BY ee.{criterio}
            ) recaudo,
            (
            SELECT {criterio} as criterio, COUNT(*) as cuotas_en_mora
            FROM public."ModuloFinanciero_solicitudcredito" s, public."ModuloFinanciero_estudianteestrella" ee
            WHERE NOT pagado AND s.estudiante_id = ee.id
            GROUP BY ee.{criterio}
            ) mora
        WHERE creds.criterio = tasa.criterio AND creds.criterio = recaudo.criterio AND creds.criterio = mora.criterio;
    """

        cursor.execute(query)
        data = cursor.fetchall()
        queries[criterio.capitalize()] = data
        cursor.close()
        conn.close()
    except (Exception, pg.DatabaseError):
        print(traceback.format_exc())
    except (KeyboardInterrupt):
        if conn:
            conn.close()
        sys.exit()
    finally:
        if conn:
            conn.close()

def queryToExcel(queries:dict):
    headings = ("Nombre Criterio", "Créditos Aprobados", "Tasa Aprobación", "Recaudo", "Cuotas en Mora")
    wb = Workbook()
    sheet = wb.active
    last = list(queries.keys())[-1]
    for name, query in queries.items():
        sheet.title = name
        sheet.row_dimensions[1].font = Font(bold = True)
        # Spreadsheet row and column indexes start at 1
        # so we use "start = 1" in enumerate so
        # we don't need to add 1 to the indexes.
        for colno, heading in enumerate(headings, start = 1):
            if heading == "Nombre Criterio":
                sheet.cell(row = 1, column = colno).value = name
            else:
                sheet.cell(row = 1, column = colno).value = heading

        # This time we use "start = 2" to skip the heading row.
        for rowno, row in enumerate(query, start = 2):
            for colno, cell_value in enumerate(row, start = 1):
                try:
                    if isinstance(cell_value, datetime):
                        cell_value = datetime.strftime(cell_value, "%d/%m/%Y")
                except TypeError:
                    pass
                sheet.cell(row = rowno, column = colno).value = cell_value
        if not name == last:
            sheet = wb.create_sheet(f"Hoja {name}")
    try:
        os.makedirs("./reports")
    except FileExistsError:
        pass
    wb.security = WorkbookProtection(workbookPassword="pass", revisionsPassword="pass", lockStructure=True, lockRevision=True)
    wb.save("./reports/reporte.xlsx")


def insertEstudiantes(conn, cur):
    with open(r'C:\Users\ElRey\Documents\Scripts\ISIS2503-Proyecto-EducacionEstrella\ReportGatherer\estudiantes.csv', 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        cont = 0
        for row in reader:
            if len(row[4]) > 50:
                row[4] = row[4][:50]
            cur.execute(
            'INSERT INTO public."ModuloFinanciero_estudianteestrella" VALUES (%s, %s, %s, %s, %s, %s, %s)',
            row)
            cont += 1
            print(f"\r{cont}/1000", end="")
        conn.commit()
        cur.close()
        print("\nCarga finalizada")

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
            print(f"\r{cont}/1000", end="")
        conn.commit()
        cur.close()
        print("\nCarga finalizada")