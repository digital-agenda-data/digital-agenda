import json
import logging

from asgiref.sync import sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from health_check.mixins import CheckMixin


logger = logging.getLogger(__name__)


class Test(AsyncWebsocketConsumer):
    async def receive(self, text_data):
        await self.send(text_data=text_data)


class HealthCheck(CheckMixin, AsyncWebsocketConsumer):
    def get_status(self):
        # XXX accessing `self.errors` actually performs the health checks
        errors = self.errors
        return {
            "healthy": not errors,
            "report": {
                str(p.identifier()): str(p.pretty_status()) for p in self.plugins
            },
        }

    async def connect(self):
        await self.accept()
        status = await sync_to_async(self.get_status)()
        await self.send(text_data=json.dumps(status))
