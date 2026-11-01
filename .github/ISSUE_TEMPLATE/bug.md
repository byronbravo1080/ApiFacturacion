---
name: Reporte de Defecto (Bug)
about: Reportar un fallo en la API, el contrato OpenAPI, las pruebas BDD o la documentación
title: "[BUG] "
labels: ["bug"]
assignees: []
---

## 1. Descripción del defecto
<!-- Describa claramente qué falló y en qué componente (contrato OpenAPI, endpoint FastAPI, prueba pytest-bdd o documento). -->


## 2. Trazabilidad y criterio afectado
- **Escenario de calidad / Historia / Criterio Gherkin afectado:** <!-- Ej.: E1, E2, E6 / HU5 / CA5.3 -->
- **Archivo o endpoint donde ocurre:** <!-- Ej.: src/facturaec/facturacion.py o api/openapi.yaml -->

## 3. Pasos para reproducir
1. Ejecutar el comando `...`
2. Enviar los datos `...`
3. Observar la salida o código de error.

## 4. Comportamiento esperado vs. comportamiento actual
- **Esperado:** 
- **Actual:** 

## 5. Verificación de la corrección
- [ ] `spectral lint api/openapi.yaml` sin errores.
- [ ] `ruff check src tests` sin hallazgos.
- [ ] `PYTHONPATH=src pytest -v` pasa todas las pruebas.
