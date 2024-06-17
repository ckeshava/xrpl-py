"""Sending duplicate requests through the Websocket client"""

import asyncio

from xrpl.asyncio.clients import AsyncWebsocketClient
from xrpl.models.requests import ServerInfo


async def main() -> None:
    """Demonstration of duplicate requests in Websocket clients"""
    async with AsyncWebsocketClient("wss://s1.ripple.com") as client:
        for _ in range(10):
            asyncio.create_task(client.request(ServerInfo()))

        # wait for the requests to be registered on the server side
        await asyncio.sleep(3)
        print(f"Queued items: {client._open_requests}")
        queued_requests = client._open_requests

        counter = 0
        for k in queued_requests:
            if k[:26] == "RequestMethod.SERVER_INFO_":
                counter += 1

        print("Total Server_Info requests = " + str(counter))
        # sleep to wait for all tasks to complete (or) throw an exception
        # Once the debug information is displayed, please feel free to Kill this process
        await asyncio.sleep(20)


if __name__ == "__main__":
    asyncio.run(main())
