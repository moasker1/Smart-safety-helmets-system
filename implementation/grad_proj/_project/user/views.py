from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login as auth_login
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
from management import models as ManagementModels

# cred = credentials.Certificate("D:\graduation project (smart helmet)\implementation\grad_proj\_project\smart-hemlet-firebase-adminsdk-a6yrp-13de9ef48d.json")
# firebase_admin.initialize_app(cred)
# db = firestore.client()
# config={
#     "apiKey": "AIzaSyD8hciQSvz9rFMHSDwcvA3qZXLz8wHPiVI",
#     "authDomain": "smart-hemlet.firebaseapp.com",
#     "databaseURL":"https://smart-hemlet-default-rtdb.firebaseio.com/",
#     "projectId": "smart-hemlet",
#     "storageBucket": "smart-hemlet.appspot.com",
#     "messagingSenderId": "506905334714",
#     "appId": "1:506905334714:web:8f961a0ed8e7d9a3fc4383",
# }
# firebase = pyrebase.initialize_app(config)
# authe = firebase.auth()
# database = firebase.database()
#============================================================================================================
def login(request):
    if "managerLogin" in request.POST:
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            user = authe.sign_in_with_email_and_password(username, password)
            user_info = authe.get_account_info(user['idToken'])

            # Extract email from user info and store it in the session
            email = user_info['users'][0]['email']
            request.session['username'] = email
            
            return redirect('manager')
        except:
            messages.error(request, "Invalid username or password")
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
    reports = db.collection('reports').stream()
    sites = db.collection('sites').stream()
    supervisors = db.collection('supervisors').stream()
    helmets = db.collection('helmets').stream()
    workers = db.collection('workers').stream()
    recent_actions = ManagementModels.RecentAction.objects.order_by('-timestamp')[:10]  

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
        "reports": reports,
        'total_number_of_helmets': total_number_of_helmets,
        'total_number_of_workers': total_number_of_workers,
        'not_assigned_helmets': len(not_assigned_helmets),
        'not_assigned_workers': len(not_assigned_workers),
        'total_number_of_supervisors': total_number_of_supervisors,
        'total_number_of_sites': total_number_of_sites,
        'total_workers_salary': total_workers_salary, 
        'recent_actions': recent_actions, 

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
        
        if db.collection('supervisors').where('name', '==', supervisor).get():
            site_ref = db.collection('sites').document()
            site_ref.set({
                'name': name,
                'supervisor': supervisor,  
            })

            # Get the logged-in user from the session
            username = request.session.get('username')

            if username:
                ManagementModels.RecentAction.objects.create(
                    user=username,  # Set the user here
                    action_sort='site',
                    action_type='add site',
                    model_affected=f'site added with name {name}',
                )
                messages.success(request, "New site has been added")
            else:
                messages.error(request, "User is not logged in")
            return redirect("sites")
        else:
            messages.error(request, "Supervisor does not exist")
            return redirect("sites")

    context = {
        "sites": sites,
        "supervisors": supervisors,
    }
    return render(request, "user/sites.html", context)
        
def site_delete(request, id):
    db = firestore.client()

    # Fetch the name of the site before deleting
    site_ref = db.collection('sites').document(id)
    site_data = site_ref.get().to_dict()
    site_name = site_data.get('name', 'Unknown Site')

    # Get the logged-in user from the session
    username = request.session.get('username')

    if username:
        ManagementModels.RecentAction.objects.create(
            user=username,  # Set the user here
            action_sort='site',
            action_type='delete site',
            model_affected=f'site deleted: {site_name}',
        )
        messages.success(request, "Site deleted successfully!")
    else:
        messages.error(request, "User is not logged in")

    # Delete the site
    site_ref.delete()

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
                'owner': "",
            })
            
            # Get the logged-in user from the session
            username = request.session.get('username')

            if username:
                ManagementModels.RecentAction.objects.create(
                    user=username,  # Set the user here
                    action_sort='helmet',
                    action_type='add helmet',
                    model_affected=f'helmet added with ID {helmetID}',
                )
                messages.success(request, "New Helmet has been added")
            else:
                messages.error(request, "User is not logged in")
        
        return redirect("helmets")

    context = {
        "helmets": helmets,
    }

    return render(request, "user/helmets.html", context)

def helmet_delete(request, id):
    db = firestore.client()
    db.collection('helmets').document(id).delete()

    # Get the logged-in user from the session
    username = request.session.get('username')

    if username:
        ManagementModels.RecentAction.objects.create(
            user=username,  # Set the user here
            action_sort='helmet',
            action_type='delete helmet',
            model_affected=f'helmet deleted with id {id}',
        )
        messages.success(request, "Helmet deleted successfully!")
    else:
        messages.error(request, "User is not logged in")

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
        
        # Get the logged-in user from the session
        username = request.session.get('username')

        if username:
            ManagementModels.RecentAction.objects.create(
                user=username,  # Set the user here
                action_sort='worker',
                action_type='add worker',
                model_affected=f'worker added with name {name}',
            )
            messages.success(request, "New worker has been added")
        else:
            messages.error(request, "User is not logged in")
        
        return redirect("workers")

    context = {
        "workers": workers,
        "sites": sites,
    }

    return render(request, "user/workers.html", context)

def worker_page(request, id):
    worker = db.collection('workers').document(id).get()
    worker_data = worker.to_dict()
    helmet_id = worker_data.get("helmetID")
    worker_id = worker.id
    helmet_docref = db.collection('helmets').where('helmetID', '==', helmet_id).get()
    helmet_data = helmet_docref[0].id

    helmet = None  
    if helmet_id:
        helmet = db.collection('helmets').where('helmetID', '==', helmet_id).stream()

    if "unassign2" in request.POST:
        worker_name = request.POST.get('worker')
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

            db.collection('workers').document(doc_id).update({
                'helmetID': ""
            })

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
        "worker_id": worker_id,
        "doc2_id": helmet_data,
    }
    return render(request, "user/workerpage.html", context)

def worker_delete(request, id):
    db = firestore.client()

    # Fetch the name of the worker before deleting
    worker_ref = db.collection('workers').document(id)
    worker_data = worker_ref.get().to_dict()
    worker_name = worker_data.get('name', 'Unknown Worker')

    # Get the logged-in user from the session
    username = request.session.get('username')

    if username:
        ManagementModels.RecentAction.objects.create(
            user=username,  # Set the user here
            action_sort='worker',
            action_type='delete worker',
            model_affected=f'worker deleted: {worker_name}',
        )
        messages.success(request, "Worker deleted successfully!")
    else:
        messages.error(request, "User is not logged in")

    # Delete the worker
    worker_ref.delete()

    return redirect('workers')
#============================================================================================================
#============================================================================================================
#============================================================================================================
def supervisor(request, id):
    db = firestore.client()

    # Fetch supervisor's data
    supervisor_ref = db.collection('supervisors').document(id)
    supervisor_data = supervisor_ref.get().to_dict()
    supervisor_name = supervisor_data.get('name', 'Unknown Supervisor')
    supervisor_site = supervisor_data.get('site')

    # Fetch helmets that are UnAssigned
    helmets_ref = db.collection('helmets').where('status', '==', 'UnAssigned').stream()
    helmets = [doc.to_dict() for doc in helmets_ref]

    # Fetch workers with the same site as the supervisor
    workers = []
    if supervisor_site:
        workers_ref = db.collection('workers').where('site', '==', supervisor_site).stream()
        workers = [{"id": doc.id, **doc.to_dict()} for doc in workers_ref]

    if "sendReport" in request.POST:
        report_supervisor = supervisor_name  # Use supervisor's name for logging
        report = request.POST.get('report')

        # Save report
        report_doc = db.collection('reports').document()
        report_doc.set({
            'supervisor': report_supervisor,
            'report': report,
        })
        messages.success(request, "Report sent!")

        # Log the report sent action
        username = request.session.get('username')
        if username:
            ManagementModels.RecentAction.objects.create(
                user=f"the supervisor : {supervisor_name}",
                action_sort='report',
                action_type='send report',
                model_affected=f'report sent to the manager ',
            )
        else:
            messages.error(request, "User is not logged in")

        return redirect("supervisor", id=id)

    if "assign" in request.POST:
        worker_name = request.POST.get('worker')
        helmet_id = request.POST.get('helmetID')

        # Check if worker exists
        worker_ref = db.collection('workers').where('name', '==', worker_name).stream()
        for doc in worker_ref:
            doc_id = doc.id
            if 'helmetID' in doc.to_dict() and doc.to_dict()['helmetID'] != '':
                messages.error(request, "Worker already has a helmet assigned")
                return redirect("supervisor", id=id)
        
        # Check if helmet exists and is UnAssigned
        helmet_ref = db.collection('helmets').where('helmetID', '==', helmet_id).where('status', '==', 'UnAssigned').stream()
        for doc in helmet_ref:
            doc2_id = doc.id
        if not helmet_ref:
            messages.error(request, "Helmet not found or already assigned")
            return redirect("supervisor", id=id)
        
        db.collection('workers').document(doc_id).update({
            'helmetID': helmet_id
        })
        
        db.collection('helmets').document(doc2_id).update({
            'status': 'Assigned',
            'owner': worker_name
        })

        messages.success(request, "Worker assigned to helmet successfully")

        # Log the worker assigned action
        username = request.session.get('username')
        if username:
            ManagementModels.RecentAction.objects.create(
                user=f"the supervisor : {supervisor_name}",
                action_sort='assign',
                action_type='assign worker',
                model_affected=f'worker {worker_name} assigned to helmet {helmet_id}',
            )
        else:
            messages.error(request, "User is not logged in")

        return redirect("supervisor", id=id)        

    # Unassign functionality
    if "unassign" in request.POST:
        worker_name = request.POST.get('worker')
        
        # Check if worker exists
        worker_ref = db.collection('workers').where('name', '==', worker_name).stream()
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

        # Log the helmet unassigned action
        username = request.session.get('username')
        if username:
            ManagementModels.RecentAction.objects.create(
                user=f"the supervisor : {supervisor_name}",
                action_sort='Unassign',
                action_type='unassign worker',
                model_affected=f'worker {worker_name} unassigned from helmet {helmet_id}',
            )
        else:
            messages.error(request, "User is not logged in")

        return redirect("supervisor", id=id)

    context = {
        "workers": workers,
        "helmets": helmets,
        "supervisor_site": supervisor_site,
        "supervisor_data": supervisor_data,
    }

    # Logging the view action
    return render(request, "user/supervisor.html", context)

#============================================================================================================
def supervisors(request):
    supervisors = db.collection('supervisors').stream()
    sites = db.collection('sites').stream()
    
    if "addSupervisor" in request.POST:
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
        
        # Get the logged-in user from the session
        username = request.session.get('username')

        if username:
            ManagementModels.RecentAction.objects.create(
                user=username,  # Set the user here
                action_sort='supervisor',
                action_type='add supervisor',
                model_affected=f'supervisor added with name {name}',
            )
            messages.success(request, "New supervisor has been added")
        else:
            messages.error(request, "User is not logged in")
        
        return redirect("supervisors")

    context = {
        "supervisors": supervisors,
        "sites": sites,
    }
    
    return render(request, "user/supervisors.html", context)

def supervisor_delete(request, id):
    db = firestore.client()

    # Fetch the name of the supervisor before deleting
    supervisor_ref = db.collection('supervisors').document(id)
    supervisor_data = supervisor_ref.get().to_dict()
    supervisor_name = supervisor_data.get('name', 'Unknown Supervisor')

    # Get the logged-in user from the session
    username = request.session.get('username')

    if username:
        ManagementModels.RecentAction.objects.create(
            user=username,  # Set the user here
            action_sort='supervisor',
            action_type='delete supervisor',
            model_affected=f'supervisor deleted: {supervisor_name}',
        )
        messages.success(request, "Supervisor deleted successfully!")
    else:
        messages.error(request, "User is not logged in")

    # Delete the supervisor
    supervisor_ref.delete()

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
    
