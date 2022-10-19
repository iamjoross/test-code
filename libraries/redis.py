from typing import Any



class _Redis:
  @staticmethod
  def start() -> dict[str, Any]:
    return {}

Redis = _Redis.start()
Redis['processed_nodes'] = []
