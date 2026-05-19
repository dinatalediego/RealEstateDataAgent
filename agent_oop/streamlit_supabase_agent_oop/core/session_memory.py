from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Dict


@dataclass
class SessionMemory:
    history: List[Dict] = field(default_factory=list)

    def add(self, question: str, query_key: str | None, status: str):
        self.history.append({
            "timestamp": datetime.now().isoformat(timespec="seconds"),
            "question": question,
            "query_key": query_key,
            "status": status,
        })

    def latest(self, n: int = 10) -> List[Dict]:
        return self.history[-n:]
