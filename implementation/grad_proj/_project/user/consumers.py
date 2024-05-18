from django.shortcuts import render
from django.http import JsonResponse
from firebase_admin import firestore
from channels.generic.websocket import AsyncWebsocketConsumer
import json
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
db = firestore.client()

class WorkerPageConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.id = self.scope['url_route']['kwargs']['id']
        # Accept the WebSocket connection
        await self.accept()

    async def disconnect(self, close_code):
        # Clean up when the WebSocket closes
        pass

    async def receive(self, text_data):
        # Receive data from WebSocket
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        # Send message back to the client
        await self.send(text_data=json.dumps({
            'message': message
        }))

def worker_page(request, id):
    worker = db.collection('workers').document(id).get()

    worker_data = worker.to_dict()
    helmet_id = worker_data.get("helmetID")

    helmet = None  

    if helmet_id: 
        helmet = db.collection('helmets').where('helmetID', '==', helmet_id).stream()

    if "unassign2" in request.POST:
        worker_name = request.POST.get('worker')
        
        # Check if worker exists
        worker_ref = db.collection('workers').where('name', '==', worker_name).stream()

        if not worker_ref:
            messages.error(request, "Worker not found")
            return redirect("worker_page", id=id)

        for doc in worker_ref:
            doc_id = doc.id
            helmet_id = doc.to_dict().get('helmetID', None)
            if not helmet_id:
                messages.error(request, "Worker doesn't have a helmet assigned")
                return redirect("worker_page", id=id)
            # Update worker document
            db.collection('workers').document(doc_id).update({
                'helmetID': ""
            })

            # Update helmet document
            helmet_ref = db.collection('helmets').where('helmetID', '==', helmet_id).stream()
            for doc in helmet_ref:
                doc2_id = doc.id
                db.collection('helmets').document(doc2_id).update({
                    'status': 'UnAssigned',
                    'owner': ''
                })

        messages.success(request, "Helmet unassigned successfully")
        return redirect("worker_page", id=id)


    context = {
        "worker": worker_data if worker.exists else None,
        "helmet": helmet,
    }
    return render(request, "workerpage.html", context)
