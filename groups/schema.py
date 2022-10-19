from pydantic import BaseModel


class GroupSchema(BaseModel):
  groupId: str