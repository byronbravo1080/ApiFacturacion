## Qué cambia

<!-- Una o dos líneas. Indique el issue que cierra: Closes #N -->

Closes #

## Trazabilidad

- Historia(s): HU
- Criterio(s) de aceptación: CA
- Escenario(s): E
- ADR afectado (si aplica): ADR-

## Rúbrica de revisión (la completa quien revisa, no quien propone el cambio)

- [ ] El commit y la rama nombran el issue y siguen Conventional Commits (`feat:`, `fix:`, `docs:`, `test:`).
- [ ] Si cambió la API, se cambió primero `api/openapi.yaml` y `spectral lint api/openapi.yaml` no da errores.
- [ ] `pytest` pasa, y la prueba de E6 (CA5.3) pasa contra PostgreSQL si se tocó la facturación.
- [ ] `ruff check src tests` y `ruff format --check src tests` no reportan problemas.
- [ ] Ninguna consulta devuelve datos de otro emisor: se filtra por el emisor del token (E1).
- [ ] No hay credenciales, certificados, RUC reales ni datos personales en el cambio.
- [ ] Si se usó IA, el uso quedó registrado en `docs/04-registro-ia.md` con su verificación.
