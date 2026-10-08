# Evidencia del ciclo BDD

## Alcance

La feature `features/cu11_decision.feature` contiene exactamente cinco
escenarios: dos positivos, dos negativos y uno de frontera. El glue code ejecuta
la API FastAPI con SQLite en memoria por escenario.

## Rojo

Se ejecutó `python -m behave --format progress` con una expectativa temporalmente
incorrecta: se esperaba HTTP `201` al certificar, aunque el contrato correcto de
la API es HTTP `200`.

Resultado real:

```text
0 features passed, 1 failed, 0 skipped
4 scenarios passed, 1 failed, 0 skipped
27 steps passed, 1 failed, 2 skipped
```

El paso fallido fue la aserción del código HTTP de certificación. La expectativa
se restauró a `200`.

## Verde

Con la expectativa corregida se ejecutó:

```text
python -m behave --format progress
```

Resultado real:

```text
1 feature passed, 0 failed, 0 skipped
5 scenarios passed, 0 failed, 0 skipped
30 steps passed, 0 failed, 0 skipped
```

También se ejecutó:

```text
python -m pytest
```

Resultado real:

```text
3 passed
```

## Refactor y verificación

La implementación quedó separada en dominio, servicio, repositorio SQLite, API y
glue code. La regla complementaria de versión `RETIRADA`, que no se agregó como
un sexto escenario BDD, está cubierta por pytest. No hay pasos `undefined`,
`skipped` ni pendientes en la ejecución verde.
