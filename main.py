import asyncio
from cluster import ClusterConnection
from constants import HOSTS


async def main():
    conn = ClusterConnection(HOSTS)
    await conn.add_group("group1")
    await conn.add_group("group2")
    # await conn.add_group("group3")
    # await conn.add_group("group3")

    # await conn.delete_group("group1")



if __name__ == "__main__":
    asyncio.run(main())
