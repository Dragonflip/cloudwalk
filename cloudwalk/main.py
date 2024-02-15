import asyncio
import uvicorn

from cloudwalk.app import app as app_fastapi
from cloudwalk.scheduler import app as app_rocketry


class Server(uvicorn.Server):
    """Customized uvicorn.Server

    Uvicorn server overrides signals and we need to include
    Rocketry to the signals."""

    def handle_exit(self, sig: int, frame) -> None:
        app_rocketry.session.shut_down()
        return super().handle_exit(sig, frame)


async def main():
    """Run Rocketry and FastAPI"""
    server = Server(
        config=uvicorn.Config(app_fastapi, workers=1, loop='asyncio')
    )

    api = asyncio.create_task(server.serve())
    sched = asyncio.create_task(app_rocketry.serve())

    await asyncio.wait([sched, api])


if __name__ == '__main__':
    asyncio.run(main())
