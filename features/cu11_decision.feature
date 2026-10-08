# language: es

Característica: Certificar o rechazar una versión de ficha
  Como persona de Dirección
  Quiero decidir una versión enviada
  Para dejarla certificada o rechazada con trazabilidad

  Antecedentes:
    Dado que existe una versión enviada de la ficha "F-001" con identificador "V-001"

  @positivo
  Escenario: Dirección certifica una versión enviada
    Dado que actúa una persona con rol "Dirección"
    Cuando solicita marcar la versión como "certificada"
    Entonces la respuesta tiene código HTTP 200
    Y la versión queda en estado "CERTIFICADA"
    Y la auditoría registra la decisión de la Dirección

  @positivo
  Escenario: Dirección rechaza una versión con observación
    Dado que actúa una persona con rol "Dirección"
    Y que informa la observación "La evidencia está incompleta"
    Cuando solicita marcar la versión como "rechazada"
    Entonces la respuesta tiene código HTTP 200
    Y la versión queda en estado "RECHAZADA"
    Y la auditoría registra la decisión de la Dirección

  @negativo
  Escenario: Un funcionario no puede decidir una versión
    Dado que actúa una persona con rol "Funcionario"
    Cuando solicita marcar la versión como "certificada"
    Entonces la respuesta tiene código HTTP 403
    Y el estado de la versión permanece "ENVIADA"

  @negativo
  Escenario: El rechazo sin observación es inválido
    Dado que actúa una persona con rol "Dirección"
    Cuando solicita marcar la versión como "rechazada"
    Entonces la respuesta tiene código HTTP 422
    Y el motivo indica que la observación es obligatoria
    Y el estado de la versión permanece "ENVIADA"

  @frontera
  Escenario: El rechazo acepta la observación mínima no vacía
    Dado que actúa una persona con rol "Dirección"
    Y que informa la observación "X"
    Cuando solicita marcar la versión como "rechazada"
    Entonces la respuesta tiene código HTTP 200
    Y la versión queda en estado "RECHAZADA"
