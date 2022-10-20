import asyncio
import os
import sys

from requests import HTTPError
from event import post_event
from groups.schema import GroupSchema
from nodes import Node, NodesRegistry
from libraries.redis import Redis


BASE_URL = "http://www.test.com"
redis = Redis


class Cluster:
    def __init__(self, hosts) -> None:
        print("[Cluster] Building nodes registry...")
        self.node_registry: list[Node] = NodesRegistry.build(hosts)
        print(
            f"[Cluster] Finished building registry with {len(self.node_registry)} items."
        )


async def delete():
    tasks = []
    for node in Redis["processed_nodes"]:
        print(
            f"[ClusterConnection] Rolling back changes for node: {node} | current size: {len(node.groups.db)}..."
        )
        task = asyncio.create_task(post_event("ON_CLUSTER_ROLLBACK_GROUP", node))
        tasks.append(task)
        await asyncio.sleep(1)

    try:
        await asyncio.gather(*tasks, return_exceptions=False)
    except HTTPError as e:
        print("[HTTPError]", e)
        for task in tasks:
            task.cancel()


class ClusterConnection:
    def __init__(self, hosts):
        print("[ClusterConnection] Connecting to cluster...")
        self.cluster = Cluster(hosts)
        print("[ClusterConnection] Connection established.")
        print("-" * 80)

    async def add_group(self, group_id):
        """
        publish an event ADD_GROUP
        """
        print("-" * 80)
        print(f"[ClusterConnection] Adding group id: {group_id}...")
        group = GroupSchema(groupId=group_id)
        # event_loop = asyncio.new_event_loop()
        # asyncio.set_event_loop(event_loop)
        tasks = []
        for idx, node in enumerate(self.cluster.node_registry):
            error = True if idx == len(self.cluster.node_registry) - 2 else False

            print(
                f"[ClusterConnection] Publishing event ON_CLUSTER_ADD_GROUP to {node}..."
            )
            if error:
                print(f"[ClusterConnection] Simulating error on adding group...")

            task = asyncio.create_task(
                post_event("ON_CLUSTER_ADD_GROUP", node, group, error)
            )
            tasks.append(task)
            await asyncio.sleep(1)

            # if response if False, we got an error
            # stop adding and rollback changes
        #     if not response:
        #         print(f"[{__class__.__name__}] Ending adding of group early")
        #         post_event("ON_CLUSTER_ROLLBACK_GROUP")
        #         break

        #     # add successful node to redis
        #     redis["processed_nodes"].append(node)
        #     print(" " * 80)

        # # no reported issues
        # for node in self.cluster.node_registry:
        #     post_event("ON_CLUSTER_COMMIT_GROUP", node)
        # re = await asyncio.gather(*tasks)
        try:
            await asyncio.gather(*tasks, return_exceptions=False)
        except HTTPError as e:
            print("[HTTPError]", e)
            for task in tasks:
                task.cancel()

        await delete()

    def delete_group(self, group_id):
        """
        publish an event ADD_GROUP
        """
        print("-" * 80)
        print(f"[ClusterConnection] Deleting group id: {group_id}...")
        group = GroupSchema(groupId=group_id)
        for idx, node in enumerate(self.cluster.node_registry):
            error = True if idx == len(self.cluster.node_registry) - 1 else False

            print(
                f"[ClusterConnection] Publishing event ON_CLUSTER_DELETE_GROUP to {node}..."
            )
            if error:
                print(f"[ClusterConnection] Simulating error on deleting group...")

            response = post_event("ON_CLUSTER_DELETE_GROUP", node, group, error)

            # if response if False, we got an error
            # stop adding and rollback changes
            if not response:
                print(f"[{__class__.__name__}] Ending deleting of group early")
                post_event("ON_CLUSTER_ROLLBACK_GROUP")
                break

            # add successful node to redis
            redis["processed_nodes"].append(node)
            print(" " * 80)

        # no reported issues
        for node in self.cluster.node_registry:
            post_event("ON_CLUSTER_COMMIT_GROUP", node)


# Disable
def blockPrint():
    sys.stdout = open(os.devnull, "w")


# Restore
def enablePrint():
    sys.stdout = sys.__stdout__


async def main():
    HOSTS = [
        "node01.app.internal.com",
        "node02.app.internal.com",
        "node03.app.internal.com",
        "node04.app.internal.com",
    ]
    conn = ClusterConnection(HOSTS)
    await conn.add_group("group1")
    # conn.add_group("group2")

    # conn.delete_group("group1")


if __name__ == "__main__":
    asyncio.run(main())
