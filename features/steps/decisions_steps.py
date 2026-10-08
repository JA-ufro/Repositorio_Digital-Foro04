from behave import given, then, when


ROLE_VALUES = {
    "Dirección": "DIRECCION",
    "Funcionario": "FUNCIONARIO",
}

DECISION_VALUES = {
    "certificada": "CERTIFICAR",
    "rechazada": "RECHAZAR",
}


@given(
    'que existe una versión enviada de la ficha "{ficha_id}" '
    'con identificador "{version_id}"'
)
def version_exists(context, ficha_id, version_id):
    response = context.client.post(
        "/versions",
        json={"version_id": version_id, "ficha_id": ficha_id},
    )
    assert response.status_code == 201, response.text
    context.version_id = version_id


@given('que actúa una persona con rol "{role}"')
def actor_has_role(context, role):
    context.actor_role = ROLE_VALUES[role]


@given('que informa la observación "{observation}"')
def actor_informs_observation(context, observation):
    context.observation = observation


@when('solicita marcar la versión como "{decision}"')
def submit_decision(context, decision):
    context.response = context.client.post(
        f"/versions/{context.version_id}/decision",
        json={
            "actor_role": context.actor_role,
            "decision": DECISION_VALUES[decision],
            "observation": context.observation,
        },
    )


@then('la respuesta tiene código HTTP {expected_status:d}')
def response_has_status(context, expected_status):
    assert context.response.status_code == expected_status, context.response.text


@then('la versión queda en estado "{expected_status}"')
def version_has_status(context, expected_status):
    assert context.response.json()["status"] == expected_status


@then('la auditoría registra la decisión de la Dirección')
def audit_records_direction(context):
    assert context.response.json()["audit"]["actor_role"] == "DIRECCION"


@then('el motivo indica que la observación es obligatoria')
def response_requires_observation(context):
    assert "observacion es obligatoria" in context.response.json()["detail"]


@then('el estado de la versión permanece "{expected_status}"')
def version_keeps_status(context, expected_status):
    response = context.client.get(f"/versions/{context.version_id}")
    assert response.status_code == 200, response.text
    assert response.json()["status"] == expected_status
