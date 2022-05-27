
SELECT a.nombre, SUM(a.monto)
FROM
    (SELECT ee.nombre as nombre, CASE WHEN s.pagado = 1 THEN s.montoAPagar ELSE 0 END as monto
    FROM public."ModuloFinanciero_solicitudcredito" s, public."ModuloFinanciero_estudianteestrella" ee
    WHERE s.estudiante_id = ee.id
    GROUP BY s.estudiante_id, s.carrera) a
GROUP BY a.nombre

--Calcular total creditos aprobados
SELECT COUNT(*), creditos_aprobados
FROM public."ModuloFinanciero_solicitudcredito" s
WHERE s.fechaAprobacion IS NOT NULL


SELECT *
FROM 
    (
        SELECT COUNT(*) creditos_aprobados, ee.-criterio- as criterio
        FROM public."ModuloFinanciero_solicitudcredito" s, public."ModuloFinanciero_estudianteestrella" ee
        WHERE s.estudiante_id = ee.id AND s.fechaAprobacion IS NOT NULL
        GROUP BY ee.-criterio-
    ) creds, 
    (
        SELECT b.-criterio- as criterio, 
            CASE WHEN a.creditos_aprobados IS NOT NULL THEN ROUND((a.creditos_aprobados/b.creditos_totales),2) 
            ELSE 0 END AS tasa_aprobacion
        FROM (
            SELECT CAST (COUNT(*) as numeric(9,2))creditos_aprobados, ee.-criterio-
            FROM public."ModuloFinanciero_solicitudcredito" s, public."ModuloFinanciero_estudianteestrella" ee
            WHERE s.estudiante_id = ee.id AND s."fechaAprobacion" IS NOT NULL
            GROUP BY ee.-criterio-
            ) a RIGHT JOIN
            (
            SELECT CAST (COUNT(*) as numeric(9,2)) creditos_totales, ee.-criterio-
            FROM public."ModuloFinanciero_solicitudcredito" s,public."ModuloFinanciero_estudianteestrella" ee
            WHERE s.estudiante_id = ee.id    
            GROUP BY ee.-criterio-
            ) b
        ON a.-criterio- = b.-criterio-;
    )tasa,
    (
        SELECT -criterio- as criterio, SUM("montoAPagar")
        FROM public."ModuloFinanciero_solicitudcredito" s, public."ModuloFinanciero_estudianteestrella" ee
        WHERE "fechaAprobacion" BETWEEN TO_DATE('2022-01-01', 'YYYY-MM-DD') AND 
                TO_DATE('2022-06-30', 'YYYY-MM-DD') AND 
                pagado AND
                s.estudiante_id = ee.id
        GROUP BY ee.-criterio-;
    ) recaudo,
    (
    SELECT -criterio- as criterio, COUNT(*)
    FROM public."ModuloFinanciero_solicitudcredito" s, public."ModuloFinanciero_estudianteestrella" ee
    WHERE NOT pagado AND s.estudiante_id = ee.id
    GROUP BY ee.-criterio-;
    ) mora
WHERE creds.criterio = tasa.criterio AND creds.criterio = recaudo.criterio AND creds.criterio = mora.criterio;


SELECT creds.criterio, creds.creditos_aprobados, tasa.tasa_aprobacion, recaudo.recaudo, mora.cuotas_en_mora
FROM 
    (
    SELECT COUNT(*) creditos_aprobados, ee.carrera as criterio
    FROM public."ModuloFinanciero_solicitudcredito" s, public."ModuloFinanciero_estudianteestrella" ee
    WHERE s.estudiante_id = ee.id AND s.fechaAprobacion IS NOT NULL
    GROUP BY ee.carrera
    ) creds, 
    (
    SELECT b.carrera as criterio, 
        CASE WHEN a.creditos_aprobados IS NOT NULL THEN ROUND((a.creditos_aprobados/b.creditos_totales),2) 
        ELSE 0 END AS tasa_aprobacion
    FROM (
        SELECT CAST (COUNT(*) as numeric(9,2))creditos_aprobados, ee.carrera
        FROM public."ModuloFinanciero_solicitudcredito" s, public."ModuloFinanciero_estudianteestrella" ee
        WHERE s.estudiante_id = ee.id AND s."fechaAprobacion" IS NOT NULL
        GROUP BY ee.carrera
        ) a RIGHT JOIN
        (
            SELECT CAST (COUNT(*) as numeric(9,2)) creditos_totales, ee.carrera
            FROM public."ModuloFinanciero_solicitudcredito" s,public."ModuloFinanciero_estudianteestrella" ee
            WHERE s.estudiante_id = ee.id    
            GROUP BY ee.carrera
        ) b
        ON a.carrera = b.carrera
    )tasa,
    (
        SELECT carrera as criterio, SUM("montoAPagar") as recaudo
        FROM public."ModuloFinanciero_solicitudcredito" s, public."ModuloFinanciero_estudianteestrella" ee
        WHERE "fechaAprobacion" BETWEEN TO_DATE('2022-01-01', 'YYYY-MM-DD') AND 
        TO_DATE('2022-06-30', 'YYYY-MM-DD') AND 
        pagado AND
        s.estudiante_id = ee.id
        GROUP BY ee.carrera
    ) recaudo,
    (
    SELECT carrera as criterio, COUNT(*) as cuotas_en_mora
    FROM public."ModuloFinanciero_solicitudcredito" s, public."ModuloFinanciero_estudianteestrella" ee
    WHERE NOT pagado AND s.estudiante_id = ee.id
    GROUP BY ee.carrera
    ) mora
WHERE creds.criterio = tasa.criterio AND creds.criterio = recaudo.criterio AND creds.criterio = mora.criterio;
