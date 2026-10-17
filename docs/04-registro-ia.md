# 04 · Registro de uso de IA

Registro de los contrastes con IA del dossier (Módulo 8, Sesiones 1 a 3). Cada fila indica qué se pidió, qué produjo la IA, qué decisión se toma y cómo se verificó.

**Herramienta y versión:** Claude Sonnet 5.5 (`claude-sonnet-5-5`), Anthropic, mediante claude.ai con herramientas de archivos y ejecución de comandos.
**Protección de datos:** no se ingresaron credenciales, certificados de firma, RUC reales ni datos de clientes. Solo se compartieron el texto de las actividades y los nombres de los integrantes (para la autoría del `README`).

> **Cómo leer las columnas.** «Hallazgo de la IA» y la verificación del asistente describen lo que hizo la IA y lo que ella misma comprobó. Las decisiones están redactadas como **propuesta**: el equipo las confirma o las cambia antes de la entrega. La verificación humana pendiente aparece señalada y no se da por hecha.

## Registro del contraste

| Sesión y uso | Qué se pidió | Hallazgo de la IA | Decisión | Cómo se verificó |
|---|---|---|---|---|
| **S2 · Borrador de diagrama como código** | C4 niveles 1 y 2 en Mermaid con nombres consistentes y relaciones etiquetadas (verbo y, en el nivel 2, tecnología), a partir de la descripción del sistema | Produjo `c1-contexto.md` (C4Context), `c2-contenedores.md` (C4Container) y una vista complementaria `c3-componentes-api.md` (flowchart), con una sola convención de nombres: Dueño de negocio, Contador externo, Cliente final, FacturaEC, SRI, Aplicación web, API REST, Base de datos, SriGateway. Al decidirse entregar solo la documentación se cambió el texto de dos etiquetas, sin alterar la estructura | *Propuesta (el equipo confirma):* aceptar C1 y C2 como base del dossier y C3 como vista complementaria; corregir etiquetas si la revisión cruzada detecta ambigüedades | **Asistente:** la sintaxis de los tres diagramas se validó con el parser de Mermaid (válidos) y se revisó la consistencia de nombres entre C1, C2 y C3. **Pendiente del equipo:** abrir los archivos en GitHub y confirmar el renderizado; la revisión cruzada de otro equipo está en `02-vistas-c4/revision-cruzada.md` |
| **S3 · Recálculo de la matriz ponderada** | Verificar la aritmética de la matriz (3 alternativas × 7 criterios), los totales y las variantes de pesos | Un script reprodujo los totales A1 4,40, A2 3,30 y A3 3,90 y las tres variantes de pesos originales (4,25 / 3,90 / 3,45; 4,35 / 3,80 / 3,70; 4,29 / 3,29 / 3,86). Al incorporar E8 se añadieron dos variantes: con A1 = 3 en fiabilidad, 4,20 / 3,30 / 3,90; y con además más peso a la fiabilidad, 4,00 / 3,80 / 3,70. A1 gana en todas y el margen mínimo frente a A2 es 0,20 | *Propuesta (el equipo confirma):* mantener puntajes y pesos; el punto de sensibilidad de E8 ya consta en el ADR-003 | **Asistente:** script en Python (Σ peso × puntaje / 100) cuyos resultados coinciden con las tablas de `01-contexto-y-drivers.md`. **Pendiente del equipo:** repetir el cálculo en una hoja de cálculo (`=SUMAPRODUCTO(pesos; puntajes)/100`) y acordar los puntajes, que son juicios y no mediciones |

