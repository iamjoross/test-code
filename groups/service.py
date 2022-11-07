
from types import CoroutineType
from constants import BASE_URL
from groups.schema import GroupSchema
from libraries.mockrequests import Requests
import logging

class GroupService:

  def __init__(self, node) -> None:
    """Initialize GroupService

    Args:
        node (Node): Node attached to service
    """
    self.api_url:str = f'{BASE_URL}/v1/group'
    self.node  = node

  async def create(self, payload: GroupSchema, error:bool = False)->None:
    """Makes a request to create a group

    Args:
        payload (GroupSchema): Group payload
        error (bool, optional): To mock a raised error. Defaults to False.
    """
    logging.debug(f"[GroupService] Adding group:{payload} to node:{self.node}...")
    response:CoroutineType = await Requests.post(self.api_url, json=dict(payload), node=self.node, error=error)
    response.get('raise_for_status')()
    logging.debug(f"[GroupService] {self.node} Group {payload.groupId} added.")


  async def delete(self, payload: GroupSchema, error:bool = False):
    logging.debug(f"[GroupService] Deleting group:{payload.groupId} from node:{self.node}...")
    response = await Requests.delete(f"{self.api_url}/{payload.groupId}", id=payload.groupId, node=self.node, error=error)
    response.get('raise_for_status')()
    logging.debug(f"[GroupService] {self.node} Group {payload.groupId} deleted.")


  # def get(self, group_id: str):
    # try:
    #   response = requests.get(f"{self.api_url}/{group_id}")
    #   response.raise_for_status()
    #   logging.debug(f"Group {group_id} deleted successfully!")
    #   return True
    # except (HTTPError, Exception) as err:
    #   logging.debug(err)
    #   return False