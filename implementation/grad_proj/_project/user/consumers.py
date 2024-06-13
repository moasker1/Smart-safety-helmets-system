# from channels.generic.websocket import AsyncWebsocketConsumer
# from firebase_admin import firestore
# import json

# class WorkerPageConsumer(AsyncWebsocketConsumer):
#     async def connect(self):
#         self.id = self.scope['url_route']['kwargs']['id']
#         await self.accept()

#         doc_ref = firestore.client().collection('workers').document(self.id)
#         self.listener = doc_ref.on_snapshot(self.on_snapshot)

#     async def disconnect(self, close_code):
#         self.listener.unsubscribe()

#     async def on_snapshot(self, snapshot, changes, read_time):
#         for change in changes:
#             data = change.document.to_dict()
#             await self.send(text_data=json.dumps({
#                 'worker_data': data
#             }))

#     async def receive(self, text_data):
#        pass

import json
from channels.generic.websocket import AsyncWebsocketConsumer
from firebase_admin import firestore

# Initialize Firestore
db = firestore.client()

class WorkerConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.worker_id = self.scope['url_route']['kwargs']['worker_id']
        self.worker_group_name = f'worker_{self.worker_id}'

        await self.channel_layer.group_add(
            self.worker_group_name,
            self.channel_name
        )

        await self.accept()

        # Fetch and send initial data
        helmet_data = await self.fetch_helmet_data(self.worker_id)
        await self.send(text_data=json.dumps({
            'worker_data': helmet_data
        }))

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.worker_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json.get('message')

        # Fetch data from Firestore based on message if needed
        helmet_data = await self.fetch_helmet_data(self.worker_id)

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'worker_data': helmet_data
        }))

    async def fetch_helmet_data(self, worker_id):
        worker_ref = db.collection('workers').document(worker_id)
        worker_doc = worker_ref.get()
        if worker_doc.exists:
            worker_data = worker_doc.to_dict()
            helmet_id = worker_data.get("helmetID")
            if helmet_id:
                helmet_ref = db.collection('helmets').where('helmetID', '==', helmet_id).stream()
                helmet_data = [helmet.to_dict() for helmet in helmet_ref]
                return helmet_data[0] if helmet_data else {}
        return {}

    async def worker_message(self, event):
        message = event['message']

        await self.send(text_data=json.dumps({
            'message': message
        }))
