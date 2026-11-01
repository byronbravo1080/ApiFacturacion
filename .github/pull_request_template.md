## Qué cambia y por qué

<!-- Describa brevemente el propósito de este Pull Request. Indique el número de issue que cierra para activar el cierre automático en GitHub: -->

Closes #

## Trazabilidad con FacturaEC

- **Tipo de cambio (Conventional Commits):** <!-- feat / fix / docs / chore / ci / test / build -->
- **Historia / Escenario / Tarea (si aplica):** <!-- Ej.: HU1–HU7, E1, E2, E6, T4–T9 -->
- **ADR o documento relacionado:** <!-- Ej.: ADR-004, docs/08-matriz-git-vs-svn.md, CONTRIBUTING.md -->

## Lista de verificación del autor (antes de pedir revisión)

- [ ] La rama nació actualizada desde `main` y sigue el formato `<tipo>/issue-N-<descripcion>`.
- [ ] Los commits son atómicos y cumplen **Conventional Commits** (`feat:`, `fix:`, `docs:`, `chore:`, `ci:`, `test:`).
- [ ] No se incluyen secretos, URI de bases de datos con clave, certificados `.p12` ni RUC/datos reales (LOPDP / NIST SSDF).
- [ ] Si se modificó `pyproject.toml`, la dependencia quedó registrada en `docs/10-gobierno-seguridad-y-dependencias.md`.

## Rúbrica de revisión cruzada (la completa el compañero revisor)

> **Nota para el revisor:** Deje además un comentario sustantivo en la revisión explicando qué comprobó en los archivos modificados.

- [ ] El PR está vinculado a su issue (`Closes #N`) y el alcance del cambio es coherente y atómico.
- [ ] Si se tocó `api/openapi.yaml`, pasa `spectral lint api/openapi.yaml` con 0 errores.
- [ ] Si se tocó código en `src/` o `tests/`, pasan `ruff check src tests` y `pytest`.
- [ ] Si es documentación técnica (ADR, matriz, reporte), cumple la estructura requerida y las citas en APA 7.
- [ ] Si se utilizó asistencia de IA, quedó registrada y verificada en `docs/04-registro-ia.md`.
