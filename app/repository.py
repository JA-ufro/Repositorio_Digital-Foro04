from __future__ import annotations

import sqlite3
from dataclasses import dataclass

from .domain import Version, VersionStatus


@dataclass(frozen=True)
class DecisionEvent:
    decision: str
    observation: str | None
    actor_role: str
    decided_at: str


class SQLiteVersionRepository:
    """Persistencia SQLite pequena y real para el vertical slice."""

    def __init__(self, database: str = ":memory:") -> None:
        self._connection = sqlite3.connect(database, check_same_thread=False)
        self._connection.row_factory = sqlite3.Row
        self._create_schema()

    def _create_schema(self) -> None:
        self._connection.executescript(
            """
            CREATE TABLE IF NOT EXISTS versions (
                version_id TEXT PRIMARY KEY,
                ficha_id TEXT NOT NULL,
                status TEXT NOT NULL,
                observation TEXT,
                decided_by TEXT,
                decided_at TEXT
            );

            CREATE TABLE IF NOT EXISTS decision_events (
                event_id INTEGER PRIMARY KEY AUTOINCREMENT,
                version_id TEXT NOT NULL,
                decision TEXT NOT NULL,
                observation TEXT,
                actor_role TEXT NOT NULL,
                decided_at TEXT NOT NULL,
                FOREIGN KEY (version_id) REFERENCES versions(version_id)
            );
            """
        )
        self._connection.commit()

    def add(self, version: Version) -> None:
        self._connection.execute(
            """
            INSERT INTO versions (
                version_id, ficha_id, status, observation, decided_by, decided_at
            ) VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                version.version_id,
                version.ficha_id,
                version.status.value,
                version.observation,
                version.decided_by,
                version.decided_at,
            ),
        )
        self._connection.commit()

    def get(self, version_id: str) -> Version | None:
        row = self._connection.execute(
            "SELECT * FROM versions WHERE version_id = ?",
            (version_id,),
        ).fetchone()
        if row is None:
            return None
        return Version(
            version_id=row["version_id"],
            ficha_id=row["ficha_id"],
            status=VersionStatus(row["status"]),
            observation=row["observation"],
            decided_by=row["decided_by"],
            decided_at=row["decided_at"],
        )

    def record_decision(
        self,
        version_id: str,
        status: VersionStatus,
        observation: str | None,
        actor_role: str,
        decided_at: str,
        decision: str,
    ) -> None:
        with self._connection:
            cursor = self._connection.execute(
                """
                UPDATE versions
                SET status = ?, observation = ?, decided_by = ?, decided_at = ?
                WHERE version_id = ?
                """,
                (
                    status.value,
                    observation,
                    actor_role,
                    decided_at,
                    version_id,
                ),
            )
            if cursor.rowcount != 1:
                raise KeyError(version_id)
            self._connection.execute(
                """
                INSERT INTO decision_events (
                    version_id, decision, observation, actor_role, decided_at
                ) VALUES (?, ?, ?, ?, ?)
                """,
                (version_id, decision, observation, actor_role, decided_at),
            )

    def latest_event(self, version_id: str) -> DecisionEvent | None:
        row = self._connection.execute(
            """
            SELECT decision, observation, actor_role, decided_at
            FROM decision_events
            WHERE version_id = ?
            ORDER BY event_id DESC
            LIMIT 1
            """,
            (version_id,),
        ).fetchone()
        if row is None:
            return None
        return DecisionEvent(
            decision=row["decision"],
            observation=row["observation"],
            actor_role=row["actor_role"],
            decided_at=row["decided_at"],
        )

    def close(self) -> None:
        self._connection.close()
