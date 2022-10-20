import asyncio

from requests import HTTPError
from event import post_event
from groups.schema import GroupSchema
from interfaces import GroupAlreadyExists, GroupNotFound
from libraries.redis import Redis
from nodes import Node, NodesRegistry
from asyncio import Task

redis = Redis


class Cluster:
    """Cluster object"""
    def __init__(self, hosts: list[str]) -> None:
        """Initialize Cluster object
        (1) Build nodes registry

        Args:
            hosts (list[str]): list of hosts as nodes
        """
        print("[Cluster] Building nodes registry...")
        self.node_registry: list[Node] = NodesRegistry.build(hosts)
        print(
            f"[Cluster] Finished building registry with {len(self.node_registry)} items."
        )

class ClusterConnection:
    def __init__(self, hosts:list[str]):
        """Initialize Cluster connection

        Args:
            hosts (list[str]): list of hosts as nodes
        """
        print("[ClusterConnection] Connecting to cluster...")
        self.cluster: Cluster = Cluster(hosts)
        print("[ClusterConnection] Connection established.")
        print("-" * 80)

    async def _process_rollback(self) -> None:
        """Rolls back flushed changes asynchronously
        (1) Flushed changes are  saved in mocked Redis instance
        (2) Coroutines are created wrapping event ON_CLUSTER_ROLLBACK_GROUP fn
        (3) Coroutines are gathered together and catches Exception on first return
        (4) Cancel coroutines after an exception is raised
        """
        tasks:list[Task] = []
        print("\n")
        for node in redis["processed_nodes"]:
            print(
                f"[ClusterConnection] Rolling back changes for node: {node} | current size: {len(node.groups.db)}..."
            )
            task: Task = asyncio.create_task(post_event("ON_CLUSTER_ROLLBACK_GROUP", node))
            tasks.append(task)
            await asyncio.sleep(1)

        try:
            await asyncio.gather(*tasks, return_exceptions=False)
            redis['processed_nodes'] = []
        except (HTTPError, GroupAlreadyExists, GroupNotFound) as e:
            print(f"[{e.__class__.__name__}]", e)
            for task in tasks:
                task.cancel()

            await self._process_rollback()

    async def _process_commit(self) -> None:
        """Commits flushed changes asynchronously
        (1) Commit in each node
        (2) Coroutines are created wrapping event ON_CLUSTER_COMMIT_GROUP fn
        (3) Coroutines are gathered together and catches Exception on first return
        (4) Cancel coroutines after an exception is raised
        """
        tasks: list[Task] = []
        print("\n")
        for node in self.cluster.node_registry:
            print(
                f"[ClusterConnection] Committing changes for node: {node} | current size: {len(node.groups.db)}..."
            )
            task:Task = asyncio.create_task(post_event("ON_CLUSTER_COMMIT_GROUP", node))
            tasks.append(task)
            await asyncio.sleep(1)

        try:
            await asyncio.gather(*tasks, return_exceptions=False)
            redis['processed_nodes'] = []
        except (HTTPError, GroupAlreadyExists, GroupNotFound) as e:
            print(f"[{e.__class__.__name__}]", e)
            for task in tasks:
                task.cancel()

            await self._process_rollback()


    async def add_group(self, group_id:str) -> None:
        """Add group to all nodes

        Args:
            group_id (str): group if of group to add
        """
        print(f"\n[ClusterConnection] Adding group id: {group_id}...")
        group:GroupSchema = GroupSchema(groupId=group_id)
        tasks: list[Task] = []
        for idx, node in enumerate(self.cluster.node_registry):
            # error = True if idx == len(self.cluster.node_registry) - 2 else False
            error = False
            print(
                f"[ClusterConnection] Publishing event ON_CLUSTER_ADD_GROUP to {node}..."
            )
            if error:
                print(f"[ClusterConnection] Simulating error on adding group...")

            task: Task = asyncio.create_task(
                post_event("ON_CLUSTER_ADD_GROUP", node, group, error)
            )
            tasks.append(task)
            await asyncio.sleep(0.01)

        try:
            await asyncio.gather(*tasks, return_exceptions=False)
        except (HTTPError, GroupAlreadyExists, GroupNotFound) as e:
            print(f"[{e.__class__.__name__}]", e)
            for task in tasks:
                task.cancel()

            await self._process_rollback()
        else:
            # commit if no errors
            await self._process_commit()

        print('-'*80)


    async def delete_group(self, group_id: str):
        """Delete group to all nodes

        Args:
            group_id (str): group if of group to delete
        """
        print(f"\n[ClusterConnection] Deleting group id: {group_id}...")
        group = GroupSchema(groupId=group_id)
        tasks: list[Task] = []
        for idx, node in enumerate(self.cluster.node_registry):
            # error = True if idx == len(self.cluster.node_registry) - 1 else False
            error = False
            print(
                f"[ClusterConnection] Publishing event ON_CLUSTER_DELETE_GROUP to {node}..."
            )
            if error:
                print(f"[ClusterConnection] Simulating error on deleting group...")

            task:Task = asyncio.create_task(
                post_event("ON_CLUSTER_DELETE_GROUP", node, group, error)
            )
            tasks.append(task)
            await asyncio.sleep(0.01)

        try :
            await asyncio.gather(*tasks, return_exceptions=False)
        except (HTTPError, GroupAlreadyExists, GroupNotFound) as e:
            print(f"[{e.__class__.__name__}]", e)
            for task in tasks:
                task.cancel()

            await self._process_rollback()
        else:
            # commit if no errors
            await self._process_commit()

        print('-'*80)
