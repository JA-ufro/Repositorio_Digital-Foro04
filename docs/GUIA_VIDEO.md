# Guía de video

Duración sugerida: entre 2 y 4 minutos.

1. Mostrar la rama `feature/foro04-bdd` y explicar que `contexto/` está ignorado.
2. Abrir `features/cu11_decision.feature` y señalar la distribución exacta:
   dos escenarios positivos, dos negativos y uno de frontera.
3. Mostrar `features/steps/decisions_steps.py` y explicar que los pasos envían
   solicitudes a la API FastAPI, no a funciones simuladas.
4. Ejecutar `behave` y mostrar los cinco escenarios exitosos, sin pasos undefined,
   skipped o pendientes.
5. Mostrar `app/service.py`, destacando autorización, observación obligatoria,
   transiciones de estado y auditoría SQLite.
6. Ejecutar `pytest` para enseñar las reglas complementarias, incluida la versión
   retirada, y cerrar mostrando `docs/evidencias/bdd-cycle.md`.
