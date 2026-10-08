from __future__ import annotations

from fastapi import FastAPI, HTTPException, status

from .domain import (
    AuthorizationError,
    InvalidVersionStateError,
    MissingObservationError,
    VersionNotFoundError,
)
from .repository import SQLiteVersionRepository
from .schemas import (
    AuditResponse,
    CreateVersionRequest,
    DecisionRequest,
    VersionResponse,
)
from .service import VersionDecisionService


def _to_response(repository: SQLiteVersionRepository, version) -> VersionResponse:
    event = repository.latest_event(version.version_id)
    audit = (
        AuditResponse(
            decision=event.decision,
            observation=event.observation,
            actor_role=event.actor_role,
            decided_at=event.decided_at,
        )
        if event is not None
        else None
    )
    return VersionResponse(
        version_id=version.version_id,
        ficha_id=version.ficha_id,
        status=version.status.value,
        observation=version.observation,
        decided_by=version.decided_by,
        decided_at=version.decided_at,
        audit=audit,
    )


def create_app(repository: SQLiteVersionRepository | None = None) -> FastAPI:
    repository = repository or SQLiteVersionRepository()
    service = VersionDecisionService(repository)
    app = FastAPI(title="Foro 04 - CU-11")
    app.state.repository = repository
    app.state.service = service

    @app.post(
        "/versions",
        response_model=VersionResponse,
        status_code=status.HTTP_201_CREATED,
    )
    def create_version(request: CreateVersionRequest) -> VersionResponse:
        try:
            version = service.create_version(
                version_id=request.version_id,
                ficha_id=request.ficha_id,
            )
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="La version ya existe.",
            )
        return _to_response(repository, version)

    @app.get("/versions/{version_id}", response_model=VersionResponse)
    def get_version(version_id: str) -> VersionResponse:
        try:
            version = service.get_version(version_id)
        except VersionNotFoundError as error:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=str(error),
            ) from error
        return _to_response(repository, version)

    @app.post("/versions/{version_id}/decision", response_model=VersionResponse)
    def decide_version(
        version_id: str,
        request: DecisionRequest,
    ) -> VersionResponse:
        try:
            version = service.decide(
                version_id=version_id,
                actor_role=request.actor_role,
                decision=request.decision,
                observation=request.observation,
            )
        except VersionNotFoundError as error:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=str(error),
            ) from error
        except AuthorizationError as error:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=str(error),
            ) from error
        except MissingObservationError as error:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=str(error),
            ) from error
        except InvalidVersionStateError as error:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=str(error),
            ) from error
        return _to_response(repository, version)

    return app


app = create_app()
