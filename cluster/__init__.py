import asyncio
from enum import Enum
import logging

from requests import HTTPError
from event import post_event
from groups.schema import GroupSchema
from interfaces import GroupAlreadyExists, GroupNotFound
from libraries.redis import Redis
from nodes import Node, NodesRegistry
from asyncio import Task

redis = Redis

class ProcessOperation(Enum):
    ROLLBACK = 'ON_CLUSTER_ROLLBACK_GROUP'
    COMMIT = 'ON_CLUSTER_COMMIT_GROUP'

class GroupOperation(Enum):
    ADD = 'ON_CLUSTER_ADD_GROUP'
    DELETE = 'ON_CLUSTER_DELETE_GROUP'

class Cluster:
    """Cluster object"""
    def __init__(self, hosts: list[str]) -> None:
        """Initialize Cluster object
        (1) Build nodes registry

        Args:
            hosts (list[str]): list of hosts as nodes
        """
        logging.debug("[Cluster] Building nodes registry...")
        self.node_registry: list[Node] = NodesRegistry.build(hosts)
        logging.debug(
            f"[Cluster] Finished building registry with {len(self.node_registry)} items."
        )

class ClusterConnection:
    def __init__(self, hosts:list[str]):
        """Initialize Cluster connection

        Args:
            hosts (list[str]): list of hosts as nodes
        """
        logging.debug("[ClusterConnection] Connecting to cluster...")
        self.cluster: Cluster = Cluster(hosts)
        self.redis = redis
        logging.debug("[ClusterConnection] Connection established.")
        logging.debug("-" * 80)

    async def _process(self, operation:ProcessOperation)-> None:
        tasks:list[Task] = []
        logging.debug("\n")
        nodes = self.cluster.node_registry if operation == ProcessOperation.COMMIT else redis["processed_nodes"]
        for node in nodes:
            logging.debug(
                f"[ClusterConnection - {operation.name}] node: {node} | current size: {len(node.groups.db)}..."
            )
            task: Task = asyncio.create_task(post_event(operation.value, node))
            tasks.append(task)

        try:
            await asyncio.gather(*tasks, return_exceptions=False)
            redis['processed_nodes'] = []
        except (HTTPError, GroupAlreadyExists, GroupNotFound) as e:
            logging.debug(f"[{e.__class__.__name__}]", e)
            await self._cancel_and_rollback(tasks)

    async def _cancel_and_rollback(self, tasks: list[Task]) -> None:
        for task in tasks:
            task.cancel()

        await self._process(ProcessOperation.ROLLBACK)

    async def group_handle(self, operation: GroupOperation, group_id: str, should_error: bool = False) -> None:
        logging.debug(f"\n[ClusterConnection | {operation.name}] For group id: {group_id}...")
        group:GroupSchema = GroupSchema(groupId=group_id)
        tasks: list[Task] = []
        for idx, node in enumerate(self.cluster.node_registry):
            # error = True if idx == len(self.cluster.node_registry) - 1 else False
            logging.debug(
                f"[ClusterConnection | {operation.name}] Publishing event with {node}..."
            )
            if should_error:
                logging.debug(f"[ClusterConnection | {operation.name}] Simulating error...")

            task: Task = asyncio.create_task(
                post_event(operation.value, node, group, should_error)
            )
            tasks.append(task)


        try:
            await asyncio.gather(*tasks, return_exceptions=False)
        except (HTTPError, GroupAlreadyExists, GroupNotFound) as e:
            logging.debug(f"[{e.__class__.__name__}]", e)
            await self._cancel_and_rollback(tasks)
        else:
            # commit if no errors
            await self._process(ProcessOperation.COMMIT)

        logging.debug('-'*80)

