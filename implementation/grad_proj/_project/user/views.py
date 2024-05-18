from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.db.models import Sum
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from datetime import date
from decimal import Decimal
from django.db.models import F , DecimalField, ExpressionWrapper
from django.http import JsonResponse
import pyrebase
import firebase_admin
from firebase_admin import credentials, firestore, auth

cred = credentials.Certificate("D:\Graduation project\implementation\grad_proj\_project\smart-hemlet-firebase-adminsdk-a6yrp-13de9ef48d.json")
firebase_admin.initialize_app(cred)
db = firestore.client()
config={
    "apiKey": "AIzaSyD8hciQSvz9rFMHSDwcvA3qZXLz8wHPiVI",
    "authDomain": "smart-hemlet.firebaseapp.com",
    "databaseURL":"https://smart-hemlet-default-rtdb.firebaseio.com/",
    "projectId": "smart-hemlet",
    "storageBucket": "smart-hemlet.appspot.com",
    "messagingSenderId": "506905334714",
    "appId": "1:506905334714:web:8f961a0ed8e7d9a3fc4383",
}
firebase = pyrebase.initialize_app(config)
authe = firebase.auth()
database = firebase.database()
#============================================================================================================
def login(request):
    if "managerLogin" in request.POST:
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            user = auth.get_user_by_email(username)
            user = auth.update_user(
                user.uid,
                password=password
            )
            id_token = auth.create_custom_token(user.uid)
            return redirect('manager')
        except firebase_admin.auth.UserNotFoundError:
            messages.error(request, "Wrong username")
            return redirect('login')
        except ValueError as e:
            messages.error(request, "Wrong password")
            return redirect('login')
            
    return render(request, 'user/index.html')

def home(request):
    return render(request, "home.html")


def supervisor_login(request):
    if "supervisorLogin" in request.POST:
        email = request.POST.get('email')
        password = request.POST.get('password')

        # Check if supervisor with provided email exists
        supervisor_ref = db.collection('supervisors').where('email', '==', email).stream()
        supervisor = None
        for doc in supervisor_ref:
            supervisor = doc.to_dict()
            break

        if supervisor:
            # Check password
            if supervisor['password'] == password:
                # Redirect to supervisor page
                return redirect('supervisor', id=doc.id)
            else:
                messages.error(request, "Wrong password")
                return redirect('login')
        else:
            messages.error(request, "Supervisor with this email does not exist")
            return redirect('login')

def logout_user(request):
    logout(request)
    return render(request, 'logout.html')

def manager(request):
    sites = db.collection('sites').stream()
    supervisors = db.collection('supervisors').stream()
    helmets = db.collection('helmets').stream()
    workers = db.collection('workers').stream()

    total_number_of_helmets = len(list(helmets))
    total_number_of_workers = len(list(workers))
    total_number_of_supervisors = len(list(supervisors))
    total_number_of_sites = len(list(sites))

    not_assigned_helmets = list(db.collection('helmets').where('status', '==', 'UnAssigned').stream())
    not_assigned_workers = list(db.collection('workers').where('helmetID', '==', '').stream())

    total_workers_salary = sum(worker.get('salary', 0) for worker in workers)

    context = {
        'sites': sites,
        'supervisors': supervisors,
        'helmets': helmets,
        'workers': workers,
        'total_number_of_helmets': total_number_of_helmets,
        'total_number_of_workers': total_number_of_workers,
        'not_assigned_helmets': len(not_assigned_helmets),
        'not_assigned_workers': len(not_assigned_workers),
        'total_number_of_supervisors': total_number_of_supervisors,
        'total_number_of_sites': total_number_of_sites,
        'total_workers_salary': total_workers_salary, 
    }

    return render(request, "user/manager.html", context)
#============================================================================================================
#============================================================================================================
#============================================================================================================
#==========================================Sites=========================================================
#============================================================================================================
#============================================================================================================
#============================================================================================================
#============================================================================================================
#============================================================================================================
def sites(request):
    sites = db.collection('sites').stream()
    supervisors = db.collection('supervisors').stream()
    
    if "addSite" in request.POST:
        name = request.POST.get('name')
        supervisor = request.POST.get('supervisor')  
        site_ref = db.collection('sites').document()
        site_ref.set({
            'name': name,
            'supervisor': supervisor,  
        })

        messages.success(request, "New site has been added")
        return redirect("sites")

    context = {
        "sites": sites,
        "supervisors": supervisors,
    }

    return render(request, "user/sites.html", context)

def site_delete(request, id):
    db = firestore.client()
    db.collection('sites').document(id).delete()
    messages.success(request, "site deleted successfully !!")
    return redirect('sites')
#============================================================================================================
#==========================================Helmets===========================================================
#============================================================================================================
def helmets(request):
    helmets = db.collection('helmets').stream()
    
    if "addHelmet" in request.POST:
        helmetID = request.POST.get('helmetID')

        existing_helmet = db.collection('helmets').where('helmetID', '==', helmetID).stream()
        if any(existing_helmet):
            messages.error(request, "ID is taken")
        else:
            helmet_doc = db.collection('helmets').document()
            helmet_doc.set({
                'helmetID': helmetID,
                'status': "NotAssigned",
            })
            messages.success(request, "New Helmet has been added")
        
        return redirect("helmets")

    context = {
        "helmets": helmets,
    }

    return render(request, "user/helmets.html", context)

def helmet_delete(request, id):
    db = firestore.client()
    db.collection('helmets').document(id).delete()
    messages.success(request, "helmet deleted successfully !!")
    return redirect('helmets')
#============================================================================================================
#========================================Workers=============================================================
#============================================================================================================
def workers(request):
    workers = db.collection('workers').stream()
    sites = db.collection('sites').stream()
    
    if "addWorker" in request.POST:
        name = request.POST.get('name')
        address = request.POST.get('address')
        phone = request.POST.get('phone')
        salary = request.POST.get('salary')
        site = request.POST.get('site')

        workers_ref = db.collection('workers').document()
        workers_ref.set({
            'name': name,
            'address': address,
            'phone': phone,
            'salary': salary,
            'helmetID': "",
            'site': site,
        })
        messages.success(request, "New worker has been added")
        return redirect("workers")

    context = {
        "workers": workers,
        "sites": sites,
    }

    return render(request, "user/workers.html", context)

# def worker_page(request, id):
#     worker = db.collection('workers').document(id).get()

#     worker_data = worker.to_dict()
#     helmet_id = worker_data.get("helmetID")

#     helmet = None  

#     if helmet_id: 
#         helmet = db.collection('helmets').where('helmetID', '==', helmet_id).stream()

#     if "unassign2" in request.POST:
#         worker_name = request.POST.get('worker')
        
#         # Check if worker exists
#         worker_ref = db.collection('workers').where('name', '==', worker_name).stream()

#         if not worker_ref:
#             messages.error(request, "Worker not found")
#             return redirect("worker_page", id=id)

#         for doc in worker_ref:
#             doc_id = doc.id
#             helmet_id = doc.to_dict().get('helmetID', None)
#             if not helmet_id:
#                 messages.error(request, "Worker doesn't have a helmet assigned")
#                 return redirect("worker_page", id=id)
#             # Update worker document
#             db.collection('workers').document(doc_id).update({
#                 'helmetID': ""
#             })

#             # Update helmet document
#             helmet_ref = db.collection('helmets').where('helmetID', '==', helmet_id).stream()
#             for doc in helmet_ref:
#                 doc2_id = doc.id
#                 db.collection('helmets').document(doc2_id).update({
#                     'status': 'UnAssigned',
#                     'owner': ''
#                 })

#         messages.success(request, "Helmet unassigned successfully")
#         return redirect("worker_page", id=id)


#     context = {
#         "worker": worker_data if worker.exists else None,
#         "helmet": helmet,
#     }
#     return render(request, "user/workerpage.html", context)


def worker_delete(request, id):
    db = firestore.client()
    db.collection('workers').document(id).delete()
    messages.success(request, "worker deleted successfully !!")
    return redirect('workers')
#============================================================================================================
#============================================================================================================
#============================================================================================================
def supervisor(request, id):

    supervisor_site = None
    sup_site_ref = db.collection('supervisors').document(id).get()
    if sup_site_ref.exists:
        supervisor_site = sup_site_ref.get("site")

    # Fetch workers with the same site as the supervisor
    workers = []
    if supervisor_site:
        workers_ref = db.collection('workers').where('site', '==', supervisor_site).stream()
        workers = [{"id": doc.id, **doc.to_dict()} for doc in workers_ref]


    if "sendReport" in request.POST:
        supervisor = request.POST.get('supervisor')
        report = request.POST.get('report')

        # Save report
        report_doc = db.collection('reports').document()
        report_doc.set({
            'supervisor': supervisor,
            'report': report,
        })
        messages.success(request, "Report sent!")

        return redirect("supervisor", id=id)
    
    if "assign" in request.POST:
        worker_name = request.POST.get('worker')
        helmet_id = request.POST.get('helmetID')

        # Check if worker exists
        worker_ref = db.collection('workers').where('name', '==', worker_name).stream()

        if not worker_ref:
            messages.error(request, "Worker not found")
            return redirect("supervisor", id=id)

        # Check if worker already has a helmet assigned
        for doc in worker_ref:
            doc_id = doc.id
            if 'helmetID' in doc.to_dict() and doc.to_dict()['helmetID'] != '':
                messages.error(request, "Worker already has a helmet assigned")
                return redirect("supervisor", id=id)
        
        # Check if helmet exists
        helmet_ref = db.collection('helmets').where('helmetID', '==', helmet_id).stream()
        if not helmet_ref:
            messages.error(request, "Helmet not found")
            return redirect("supervisor", id=id)

        # Check if helmet is already assigned
        for doc in helmet_ref:
            doc2_id = doc.id
            if 'status' in doc.to_dict() and doc.to_dict()['status'] == "Assigned":
                messages.error(request, "Helmet is already assigned")
                return redirect("supervisor", id=id)
        
        db.collection('workers').document(doc_id).update({
            'helmetID': helmet_id
        })
        
        db.collection('helmets').document(doc2_id).update({
            'status': 'Assigned',
            'owner': worker_name
        })

        messages.success(request, "Worker assigned to helmet successfully")
        return redirect("supervisor", id=id)        

    # Unassign functionality
    if "unassign" in request.POST:
        worker_name = request.POST.get('worker')
        
        # Check if worker exists
        worker_ref = db.collection('workers').where('name', '==', worker_name).stream()

        if not worker_ref:
            messages.error(request, "Worker not found")
            return redirect("supervisor", id=id)

        for doc in worker_ref:
            doc_id = doc.id
            helmet_id = doc.to_dict().get('helmetID', None)
            if not helmet_id:
                messages.error(request, "Worker doesn't have a helmet assigned")
                return redirect("supervisor", id=id)
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
        return redirect("supervisor", id=id)

    context = {
        "workers": workers,
        "supervisor_site": supervisor_site,
    }
    return render(request, "user/supervisor.html", context)

#============================================================================================================
def supervisors(request):
    supervisors = db.collection('supervisors').stream()
    sites = db.collection('sites').stream()
    if "addSupervisor" in request.POST :
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        password = request.POST.get('password')
        site = request.POST.get('site')

        supervisor_ref = db.collection('supervisors').document()
        supervisor_ref.set({
            'name': name,
            'phone': phone,
            'email': email,
            'password': password,
            'site': site,
        })
        messages.success(request, "new supervisor has been added")
        return redirect("supervisors")

    context = {
        "supervisors": supervisors,
        "sites": sites,
    }
    
    return render(request, "user/supervisors.html", context)

def supervisor_delete(request, id):
    db = firestore.client()
    db.collection('supervisors').document(id).delete()
    messages.success(request, "supervisor deleted successfully !!")
    return redirect('supervisors')
#============================================================================================================
#============================================================================================================
#============================================================================================================
def organization(request):
    return render(request, "user/organization.html")
#============================================================================================================
def reports(request):
    reports = db.collection('reports').stream()
    if "addreport" in request.POST :
        supervisor = request.POST.get('supervisor')
        report = request.POST.get('report')

        report_doc = db.collection('reports').document()
        report_doc.set({
            'supervisor': supervisor,
            'report': report,
        })
        messages.success(request, "report sent !")
        return redirect("supervisors")

    context = {
        "reports": reports,
    }
    
    return render(request, "user/reports.html", context)
#============================================================================================================
def management_send_data():
    sites = db.collection('sites').stream()
    
