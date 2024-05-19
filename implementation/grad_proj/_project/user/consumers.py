# consumers.py
from channels.generic.websocket import AsyncWebsocketConsumer
from firebase_admin import firestore
import json







class WorkerPageConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.id = self.scope['url_route']['kwargs']['id']
        await self.accept()

        doc_ref = firestore.client().collection('workers').document(self.id)
        self.listener = doc_ref.on_snapshot(self.on_snapshot)

    async def disconnect(self, close_code):
        self.listener.unsubscribe()

    async def on_snapshot(self, snapshot, changes, read_time):
        for change in changes:
            data = change.document.to_dict()
            await self.send(text_data=json.dumps({
                'worker_data': data
            }))

    async def receive(self, text_data):
        pass
