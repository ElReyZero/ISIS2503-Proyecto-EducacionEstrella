
tasa de creditos = aceptados/solicitados
total recaudo semestral 
total cuotas en mora

SELECTSELECT a.nombre, SUM(a.monto)
FROM
    (SELECT ee.nombre as nombre, CASE WHEN s.pagado = 1 THEN s.montoAPagar ELSE 0 as monto
    FROM public."ModuloFinanciero_solicitudcredito" s, public."ModuloFinanciero_estudianteestrella" ee
    WHERE s.estudiante_id = ee.id
    GROUP BY s.estudiante_id, s.carrera) a
GROUP BY a.nombre
