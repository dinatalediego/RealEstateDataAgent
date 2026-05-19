from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any

import pandas as pd


@dataclass(frozen=True)
class AgentProfile:
    name: str = "DecideCasa AgentOS"
    role: str = "Real Estate Intelligence Agent"
    tone: str = "ejecutivo, claro y accionable"
    allowed_scope: str = "Solo lectura sobre tablas autorizadas"


@dataclass(frozen=True)
class QueryDefinition:
    id: str
    agent: str
    title: str
    description: str
    keywords: list[str]
    sql: str
    chart: str = "table"
    confidence_rules: dict[str, Any] = field(default_factory=dict)


@dataclass
class AgentResponse:
    question: str
    query: QueryDefinition | None
    answer: str
    data: pd.DataFrame | None = None
    sql: str | None = None
    confidence_label: str = "No calculada"
    confidence_score: float | None = None
    warnings: list[str] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.now)

    @property
    def has_data(self) -> bool:
        return self.data is not None and not self.data.empty
