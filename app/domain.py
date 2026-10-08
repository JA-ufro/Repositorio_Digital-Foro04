from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class Role(str, Enum):
    DIRECTION = "DIRECCION"
    FUNCTIONARY = "FUNCIONARIO"


class Decision(str, Enum):
    CERTIFY = "CERTIFICAR"
    REJECT = "RECHAZAR"


class VersionStatus(str, Enum):
    SUBMITTED = "ENVIADA"
    CERTIFIED = "CERTIFICADA"
    REJECTED = "RECHAZADA"
    WITHDRAWN = "RETIRADA"


@dataclass(frozen=True)
class Version:
    version_id: str
    ficha_id: str
    status: VersionStatus
    observation: str | None = None
    decided_by: str | None = None
    decided_at: str | None = None


class BusinessRuleError(Exception):
    """Error producido por una regla del caso de uso."""


class AuthorizationError(BusinessRuleError):
    pass


class VersionNotFoundError(BusinessRuleError):
    pass


class InvalidVersionStateError(BusinessRuleError):
    pass


class MissingObservationError(BusinessRuleError):
    pass
