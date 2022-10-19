
from event import post_event
from groups.schema import GroupSchema
from nodes import Node, NodesRegistry
from libraries.redis import Redis


BASE_URL = "http://www.test.com"
redis = Redis

class Cluster:
  def __init__(self, hosts) -> None:
    self.node_registry: list[Node] = NodesRegistry.build(hosts)

  def add_group(self, group_id):
    """
    publish an event ADD_GROUP
    """
    group = GroupSchema(groupId=group_id)
    for idx, node in enumerate(self.node_registry):
      error = True if idx == len(self.node_registry)- 1 else False
      response = post_event("ON_CLUSTER_ADD_GROUP", node, group, error)

      # if response if False, we got an error
      # stop adding and rollback changes
      if not response:
        print(f"[{__class__.__name__}] Ending adding of group early")
        post_event("ON_CLUSTER_ROLLBACK_GROUP")
        break

      # add successful node to redis
      redis['processed_nodes'].append(node)


    # no reported issues
    for node in self.node_registry:
      post_event("ON_CLUSTER_COMMIT_GROUP", node)




def main():


  HOSTS = [
  'node01.app.internal.com',
  'node02.app.internal.com',
  'node03.app.internal.com',
  ]
  cluster = Cluster(HOSTS)
  cluster.add_group('group1')
  # cluster.add_group('group2')
  print("["," - ".join(cluster.node_registry[0].groups),"]")

if __name__ == '__main__' and __package__ is None:
    import sys
    sys.path.append("..")
    main()
