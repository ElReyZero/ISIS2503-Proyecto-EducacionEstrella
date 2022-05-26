
tasa de creditos = aceptados/solicitados
total recaudo semestral 
total cuotas en mora

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

SELECT COUNT(*) creditos_aprobados, ee.-criterio-
FROM public."ModuloFinanciero_solicitudcredito" s, public."ModuloFinanciero_estudianteestrella" ee
WHERE s.estudiante_id = ee.id AND s.fechaAprobacion IS NOT NULL
GROUP BY ee.-criterio-

SELECT b.-criterio-, 
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


-- Total Recaudo Semestral
SELECT -criterio-, SUM("montoAPagar")
FROM public."ModuloFinanciero_solicitudcredito" s, public."ModuloFinanciero_estudianteestrella" ee
WHERE "fechaAprobacion" BETWEEN TO_DATE('2022-01-01', 'YYYY-MM-DD') AND 
        TO_DATE('2022-06-30', 'YYYY-MM-DD') AND 
        pagado AND
        s.estudiante_id = ee.id
GROUP BY ee.-criterio-;