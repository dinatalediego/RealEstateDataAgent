from __future__ import annotations

from datetime import datetime
from pathlib import Path

import pandas as pd

from decidecasa_agentos.core.models import AgentResponse


class QueryAuditTrail:
    """Guarda auditoría local de preguntas, consultas y estado."""

    def __init__(self, log_path: Path) -> None:
        self.log_path = log_path
        self.log_path.parent.mkdir(parents=True, exist_ok=True)

    def record(self, response: AgentResponse, status: str = "ok") -> None:
        row = {
            "created_at": datetime.now().isoformat(timespec="seconds"),
            "status": status,
            "question": response.question,
            "query_id": response.query.id if response.query else None,
            "agent": response.query.agent if response.query else None,
            "confidence_label": response.confidence_label,
            "rows": len(response.data) if response.data is not None else 0,
            "warnings": " | ".join(response.warnings),
        }
        df = pd.DataFrame([row])
        if self.log_path.exists():
            df.to_csv(self.log_path, mode="a", header=False, index=False)
        else:
            df.to_csv(self.log_path, index=False)
