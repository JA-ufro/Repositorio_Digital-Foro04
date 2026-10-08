# Foro 04: BDD para CU-11

Vertical slice ejecutable del caso de uso `CU-11 – Certificar o rechazar versión`.
La aplicación expone una API FastAPI, aplica las reglas en un servicio de dominio y
persiste versiones y decisiones en SQLite. Cada escenario BDD usa una base SQLite
en memoria independiente.

## Trazabilidad

La especificación vigente es el SRS 1.2. El PDF del Foro 03 contiene el caso
histórico `CU-08 – Certificar e Inmovilizar Ficha de Resolución`; sus escenarios
relevantes se conservaron y se adaptaron al nombre y reglas de `CU-11`.

| Clasificación | Escenario | Origen o regla |
| --- | --- | --- |
| Positivo | Dirección certifica una versión enviada | Escenario positivo del Foro 03 y CU-11 |
| Positivo | Dirección rechaza con observación | Escenario de rechazo del Foro 03 y CU-11 |
| Negativo | Funcionario intenta decidir | Escenario de autorización del Foro 03 |
| Negativo | Rechazo sin observación | RF-11.3 del SRS 1.2 |
| Frontera | Rechazo con observación de un carácter | Límite de la regla de observación no vacía |

La regla de no decidir una versión `RETIRADA` también está implementada y cubierta
por pytest, pero no se agrega como un sexto escenario BDD.

## Instalación y ejecución

```text
python -m venv .venv
python -m pip install -e ".[test]"
behave
pytest
```

Para levantar la API:

```text
uvicorn app.main:app --reload
```

El glue code está en `features/steps/decisions_steps.py` y ejecuta solicitudes
contra la aplicación real usando `TestClient`. No usa mocks ni pasos pendientes.

## Estructura

- `app/`: dominio, servicio, persistencia SQLite y API.
- `features/`: feature Gherkin, entorno y glue code Behave.
- `tests/`: pruebas pytest de reglas y auditoría.
- `docs/evidencias/bdd-cycle.md`: evidencia del ciclo rojo, verde y refactor.
- `docs/GUIA_VIDEO.md`: guion para presentar el trabajo.
- `contexto/`: material docente local, excluido por `.gitignore`.
