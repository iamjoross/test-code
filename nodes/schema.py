
from pydantic import BaseModel


class NodeSchema(BaseModel):
  id: str
  groups: list[str] | None = []