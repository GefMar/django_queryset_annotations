import dataclasses
from typing import Any, Dict


@dataclasses.dataclass
class BaseContextManager:
    context: Dict[str, Any] = dataclasses.field(default_factory=dict)

    def get_context(self) -> Dict[str, Any]:
        return self.context
