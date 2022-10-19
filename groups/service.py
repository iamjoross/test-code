import traceback
from groups.schema import GroupSchema
from libraries.mockrequests import Requests


BASE_URL = "http://www.test.com"

class GroupService:

  def __init__(self, node) -> None:
    self.api_url = f'{BASE_URL}/v1/group'
    self.node  = node

  def create(self, payload: GroupSchema, error:bool = False):
    try:
      response = Requests.post(self.api_url, json=dict(payload), node=self.node, error=error)
      response.get('raise_for_status')()
      print(f"{self.node} Group {payload.groupId} added.")
      return True
    except Exception as err:
      # print(traceback.format_exc())
      print(f"[GroupService] Error: {err} ")
      return False

  # def delete(self, payload: GroupSchema):
  #   try:
  #     response = requests.delete(self.api_url, json=dict(payload))
  #     response.raise_for_status()
  #     print(f"Group {payload.groupId} deleted successfully!")
  #     return True
  #   except (HTTPError, Exception) as err:
  #     print(err)
  #     return False

  # def get(self, group_id: str):
    # try:
    #   response = requests.get(f"{self.api_url}/{group_id}")
    #   response.raise_for_status()
    #   print(f"Group {group_id} deleted successfully!")
    #   return True
    # except (HTTPError, Exception) as err:
    #   print(err)
    #   return False