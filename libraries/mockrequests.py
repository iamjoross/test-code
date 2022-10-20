from typing import Any

from requests import HTTPError


def raise_for_status():
    raise HTTPError("Something went wrong")


def dont_raise():
    return


class Requests:
    def __init__(self) -> None:
        pass

    @classmethod
    async def post(self, url, json: dict[str, str], node, error: bool = False):
        if not error:
            node.groups.db.add(json=json)
            return {"status_code": 200, "raise_for_status": dont_raise}
        else:
            return {"status_code": 404, "raise_for_status": raise_for_status}

    @classmethod
    def delete(self, url, id:str ,node, error: bool = False):
        if not error:
            node.groups.db.delete(id)
            return {"status_code": 200, "raise_for_status": dont_raise}
        else:
            return {"status_code": 404, "raise_for_status": raise_for_status}
