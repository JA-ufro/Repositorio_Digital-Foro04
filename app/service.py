from __future__ import annotations

from datetime import datetime, timezone

from .domain import (
    AuthorizationError,
    Decision,
    InvalidVersionStateError,
    MissingObservationError,
    Role,
    Version,
    VersionNotFoundError,
    VersionStatus,
)
from .repository import SQLiteVersionRepository


class VersionDecisionService:
    def __init__(self, repository: SQLiteVersionRepository) -> None:
        self._repository = repository

    def create_version(
        self,
        version_id: str,
        ficha_id: str,
        status: VersionStatus = VersionStatus.SUBMITTED,
    ) -> Version:
        version = Version(version_id=version_id, ficha_id=ficha_id, status=status)
        self._repository.add(version)
        return version

    def get_version(self, version_id: str) -> Version:
        version = self._repository.get(version_id)
        if version is None:
            raise VersionNotFoundError(f"No existe la version {version_id}.")
        return version

    def decide(
        self,
        version_id: str,
        actor_role: str,
        decision: Decision,
        observation: str | None = None,
    ) -> Version:
        version = self.get_version(version_id)
        if actor_role != Role.DIRECTION.value:
            raise AuthorizationError("Solo la Direccion puede decidir una version.")
        if version.status == VersionStatus.WITHDRAWN:
            raise InvalidVersionStateError(
                "No se puede certificar ni rechazar una version retirada."
            )
        if version.status != VersionStatus.SUBMITTED:
            raise InvalidVersionStateError(
                "La version debe estar ENVIADA para ser decidida."
            )

        if decision == Decision.REJECT:
            cleaned_observation = observation.strip() if observation is not None else ""
            if not cleaned_observation:
                raise MissingObservationError(
                    "La observacion es obligatoria para rechazar una version."
                )
        else:
            cleaned_observation = None

        decided_at = datetime.now(timezone.utc).isoformat()
        resulting_status = (
            VersionStatus.CERTIFIED
            if decision == Decision.CERTIFY
            else VersionStatus.REJECTED
        )
        self._repository.record_decision(
            version_id=version_id,
            status=resulting_status,
            observation=cleaned_observation,
            actor_role=actor_role,
            decided_at=decided_at,
            decision=decision.value,
        )
        return self.get_version(version_id)
