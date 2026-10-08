import pytest

from app.domain import (
    Decision,
    InvalidVersionStateError,
    MissingObservationError,
    VersionStatus,
)
from app.repository import SQLiteVersionRepository
from app.service import VersionDecisionService


@pytest.fixture
def service_and_repository():
    repository = SQLiteVersionRepository()
    service = VersionDecisionService(repository)
    yield service, repository
    repository.close()


def test_rejection_requires_a_non_empty_observation(service_and_repository):
    service, repository = service_and_repository
    service.create_version("V-001", "F-001")

    with pytest.raises(MissingObservationError):
        service.decide("V-001", "DIRECCION", Decision.REJECT, "  ")

    assert repository.get("V-001").status == VersionStatus.SUBMITTED


def test_withdrawn_version_cannot_be_decided(service_and_repository):
    service, repository = service_and_repository
    service.create_version("V-002", "F-002", VersionStatus.WITHDRAWN)

    with pytest.raises(InvalidVersionStateError):
        service.decide("V-002", "DIRECCION", Decision.CERTIFY)


def test_decision_is_persisted_with_an_audit_event(service_and_repository):
    service, repository = service_and_repository
    service.create_version("V-003", "F-003")

    version = service.decide(
        "V-003",
        "DIRECCION",
        Decision.REJECT,
        "Falta respaldo",
    )
    event = repository.latest_event("V-003")

    assert version.status == VersionStatus.REJECTED
    assert event is not None
    assert event.decision == "RECHAZAR"
    assert event.observation == "Falta respaldo"
