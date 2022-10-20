import traceback

from requests import HTTPError
from groups.schema import GroupSchema
from libraries.mockrequests import Requests


BASE_URL = "http://www.test.com"

class GroupService:

  def __init__(self, node) -> None:
    self.api_url = f'{BASE_URL}/v1/group'
    self.node  = node

  async def create(self, payload: GroupSchema, error:bool = False):
    print(f"[GroupService] Adding group:{payload} to node:{self.node}...")
    response = await Requests.post(self.api_url, json=dict(payload), node=self.node, error=error)
    response.get('raise_for_status')()
    print(f"[GroupService] {self.node} Group {payload.groupId} added.")


  def delete(self, payload: GroupSchema, error:bool = False):
    print(f"[GroupService] Deleting group:{payload.groupId} from node:{self.node}...")
    try:
      response = Requests.delete(f"{self.api_url}/{payload.groupId}", id=payload.groupId, node=self.node, error=error)
      response.get('raise_for_status')()
      print(f"Group {payload.groupId} deleted successfully!")
      return True
    except Exception as err:
      print(f"[GroupService] Error: {err} ")
      return False

  # def get(self, group_id: str):
    # try:
    #   response = requests.get(f"{self.api_url}/{group_id}")
    #   response.raise_for_status()
    #   print(f"Group {group_id} deleted successfully!")
    #   return True
    # except (HTTPError, Exception) as err:
    #   print(err)
    #   return False