from dataclasses import dataclass, field
from constants import CLUSTER_ADD_GROUP_EVENT, CLUSTER_COMMIT_GROUP_EVENT, CLUSTER_ROLLBACK_GROUP_EVENT
from event import subscribe
from groups import Groups
from groups.schema import GroupSchema
from groups.service import GroupService
from libraries.redis import Redis

@dataclass
class Node:
  """Node Object Instance"""
  id:str
  groups: Groups = field(default_factory=Groups)

  def __str__(self) -> str:
    """Returns a string representation of the node

    Returns:
        str: node string representation
    """
    return f"<{self.id}>"

class NodesRegistry:
  """Simple Builder Registry Pattern to store nodes"""
  @staticmethod
  def build(hosts: list[str])->list[Node]:
    """Build method to create nnodes registry and attaches
       event listeners

    Args:
        hosts (list[str]): list of hosts for nodes

    Returns:
        list[Node]: registry of nodes
    """
    print("[NodesRegistry] Building nodes registry")
    registry: list[Node] = []
    for host in hosts:
      node:Node = Node(host)
      registry.append(node)

    setup_event_handlers()
    return registry


def handle_ON_CLUSTER_ADD_GROUP(node: Node, payload: GroupSchema, error: bool)->bool:
    """Event handler for ON_CLUSTER_ADD_GROUP;
      Calls GroupService to create the group on the node

    Args:
        node (Node): Node
        payload (GroupSchema): service payload
        error (bool): value to mock error

    Returns:
        bool: response value
    """
    group_service:GroupService = GroupService(node)
    response:bool = group_service.create(payload, error)
    return response

def handle_ON_CLUSTER_ROLLBACK_GROUP() -> None:
    """Event handler for ON_CLUSTER_ROLLBACK_GROUP event
       Rollbacks "flushed" node data in the database

    """
    for node in Redis['processed_nodes']:
      node.groups.db.rollback()
    Redis['processed_nodes'] = []


def handle_ON_CLUSTER_COMMIT_GROUP(node: Node) -> None:
    """Event handler for ON_CLUSTER_COMMIT_GROUP
       Commit changes in the database

    Args:
        node (Node): Node instance
    """
    node.groups.db.commit()
    Redis['processed_nodes'] = []


def setup_event_handlers() -> None:
    """Setup all event handlers for nodes"""
    subscribe(CLUSTER_ADD_GROUP_EVENT, handle_ON_CLUSTER_ADD_GROUP)
    subscribe(CLUSTER_COMMIT_GROUP_EVENT, handle_ON_CLUSTER_COMMIT_GROUP)
    subscribe(CLUSTER_ROLLBACK_GROUP_EVENT, handle_ON_CLUSTER_ROLLBACK_GROUP)
