import json
from django.contrib.auth.models import Group
from django.http.request import HttpRequest
from django.http.response import HttpResponseRedirect, JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.db import IntegrityError
from .models import SkillForm, User, Project, ProjectForm, Message, Profile, Skill, MessageForm, ProfileForm

# Create your views here.
def index(request):
    return render(request, "capstone/index.html")

@login_required
def createMessage(request):

    # Create a new message must be through "POST"
    if request.method != "POST":
        return JsonResponse({"error": "Post request required"}, status=400)

    # Content of the message
    data = json.loads(request.body)
    user = data.get("currentUser", "")
    recipient = data.get("profileUser", "")
    sender = data.get("sender", "")
    title = data.get("title", "")
    content = data.get("content", "")
    
    currentUser = User.objects.get(username=user)
    profileUser = User.objects.get(username=recipient)

    # entering the new message in the database
    message = Message.objects.create(user=currentUser, recipient=profileUser, sender=sender, title=title, content=content)
    message.save()

    return JsonResponse({"message": "Message sent."}, status=201)

# All messages sent to the user
@login_required
def allMessages(request,username):

    profileUser = User.objects.get(username=username)
    loggedUser = User.objects.get(username=request.user.username)
    messages = Message.objects.filter(recipient=loggedUser).order_by('-created')
    
    return render(request, "capstone/allMessages.html", {
        "messages": messages,
        "profileUser": profileUser,
        "loggedUser": loggedUser,
    })
   
@login_required
def message(request, message_id):
    
    # Query for requested message
    try:
         message = Message.objects.get(pk=message_id)
    except Message.DoesNotExist:
        return JsonResponse({"error": "Message not found."}, status=404)
    
    # get all message data
    if request.method == "GET":
        return JsonResponse(message.serialize())

    # delete message from database
    elif request.method == "DELETE":
        message.delete()
        return JsonResponse({"message": "Message deleted."}, status=202)

@login_required
def account(request):
    user = request.user
    # Get the account for the logged user
    account = Profile.objects.get(user=user)
    form = ProfileForm(instance=account)

    # User can add Profile and Background image,
    #  as well write biography
    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES, instance=account)
        if form.is_valid():
            form.save()
        else:
            return HttpResponse("Form not valid")
    
    return render(request, "capstone/account.html", {
        "form": form,
        "account": account,
        "user": user
    })

#API
@login_required
def createProject(request):

    allprojects = Project.objects.filter(user=request.user)
    projects = []
    for project in allprojects:
        projectId  = project.id  
    projects.append(projectId)

    return JsonResponse({"projects": projects})

@login_required
def addProject(request):

# Check if the user added project and according to that modify the form
    projects = Project.objects.filter(user=request.user)
    lastProject = projects.last()
    form = ProjectForm()
    if len(projects) == 1:
        addProject = Project.objects.get(user=request.user)

        if addProject.description == None:
            # overwrite the existing empty project
            if request.method == "POST":
                form = ProjectForm(request.POST, request.FILES, instance=addProject)
                if form.is_valid():
                    obj = form.save(commit=False)
                    obj.user = request.user
                    obj.save()
                    return HttpResponseRedirect(reverse("addProject"))

                else:
                    return HttpResponse("Form not valid")
        else:
            # if user already adde a project, create a new one
            if request.method == "POST":
                form = ProjectForm(request.POST, request.FILES)
                if form.is_valid():
                    obj = form.save(commit=False)
                    obj.user = request.user
                    obj.save()
                    return HttpResponseRedirect(reverse("addProject"))

                else:
                    return HttpResponse("Form not valid")
            
    else:
        if request.method == "POST":
                form = ProjectForm(request.POST, request.FILES)
                if form.is_valid():
                    obj = form.save(commit=False)
                    obj.user = request.user
                    obj.save()
                    return HttpResponseRedirect(reverse("addProject"))

                else:
                    return HttpResponse("Form not valid")

    return render(request, "capstone/addProject.html", {
        "number": len(projects),
        "form": form,
        "projects": projects,
        "lastProject": lastProject
    })

@login_required
def project(request, project_id):

    user = request.user
    profileUserId = request.session.get('profileUserId')
    project = Project.objects.get(user=profileUserId, pk=project_id)
    form = ProjectForm()

    # save the uploaded files and data to database
    if request.method == "POST":
        form = ProjectForm(request.POST, request.FILES, instance=project)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.user = request.user
            obj.save()
            return HttpResponseRedirect(reverse("project",args=[project_id]))
        else:
            return HttpResponse("Form not valid") 

    return render(request, "capstone/project.html", {
        "project": project,
        "user": user,
        "profileUserId": profileUserId,
        "form": form
    })

# API
def projectView(request, project_id):

    # Get project
    project = Project.objects.get(pk=project_id)
    if request.method == "GET":
        return JsonResponse(project.serialize())
    
    # Delete project from the database
    if request.method == "DELETE":
        project.delete()
        return JsonResponse({"message": "Project Deleted"}, status=202)

    if request.method == "PUT":
        # edit the the projects title and description
        data = json.loads(request.body)
        user= request.user
        title = data.get("title", "")
        description = data.get("description", "")
        video = data.get("video", "")
        project.user = user
        project.title = title
        project.description = description
        project.save()

        return JsonResponse({"message": "project edited"}, status=202)
    
    return JsonResponse({"message": "project"})

# Developers page
def developers(request):
    user = request.user
    developers = Profile.objects.all()

    return render(request, "capstone/developers.html", {
        "developers": developers,
        "user": user
    })    

# Used for react.js in index page for the Contact Form sender
def developerProfile(request):

    # Currently logged User
    currentUser = User.objects.get(username=request.user)
    profileUser = request.session.get('profileUser')

    return JsonResponse({
        # Map only the necesary fields of User
        "currentUser": currentUser.username,
        "profileUser": profileUser
    })

# Profile page
@login_required
def mycv(request, username):

    if request.user.is_authenticated:
        # Query database and save the data in variables
        currentUser = User.objects.get(username=request.user)
        profileUser = User.objects.get(username=username).username
        profileUserId = User.objects.get(username=username).id
        request.session["profileUserId"] = profileUserId
        profileUsername = User.objects.get(username=username)
        request.session["profileUser"] = profileUser
        account = Profile.objects.get(user=profileUsername)
       
        projects = Project.objects.filter(user=profileUsername).order_by('-created')
        allSkills = Skill.objects.filter(user=profileUsername)

        userGroup = Group.objects.get(user=request.user)

        return render(request, "capstone/mycv.html", {
        "currentUser": currentUser,
        "profileUser": profileUser,
        "account": account,
        "projects": projects,
        "allSkills": allSkills,
        "group": userGroup,
    })
        
    else:
        return HttpResponseRedirect(reverse("login"))

@login_required
def skills(request):
    currentUser = request.user
    profileUserId = request.session.get('profileUserId')

    if request.method == "GET":
        usersSkills = []
        allSkills = Skill.objects.filter(user=profileUserId)
        for skill in allSkills:
            usersSkills.append(skill.serialize())

    # get json data and save it in the database
    if request.method == "POST":
        data = json.loads(request.body)
        devSkills = data.get("devSkills", "")
        skill = Skill.objects.create(user=currentUser,devSkills=devSkills)
        skill.save()
        return JsonResponse({"message": "Skill added successfully."}, status=201)
    
    return JsonResponse({
        "usersSkills" : usersSkills,
        "currentUser": currentUser.id,
        "profileUserId": profileUserId
    })

@login_required
def skill(request, skill_id):

    # Query for skill
    try:
        skill = Skill.objects.get(user=request.user,pk=skill_id)
    except Skill.DoesNotExist:
        return JsonResponse({"error": "Skill not found."}, status=404)

    if request.method == "GET":

        return JsonResponse(skill.serialize())
    if request.method == "DELETE":
        skill.delete()
        return JsonResponse({"message": "Skill deleted."}, status=202)

def log_in(request):
    if request.method == "POST":

        # Sign in user
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check for successful authentication
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "capstone/login.html", {
                "message": "Username and/or password are not valid."
            })
    else:
        return render(request, "capstone/login.html")

    
def log_out(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":

        # User's credentials
        userGroups = request.POST.get("group")
        if userGroups == None:
            group, created = Group.objects.get_or_create(name="developer")
        else:
            group, created = Group.objects.get_or_create(name="employer")
        username = request.POST["username"]
        email = request.POST["email"]

        # Check that password matches with the confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "capstone/register.html", {
                "message": "Passwords didn't match"
            })
        
        # Try to create new user
        try:
            user = User.objects.create_user(username=username, email=email, password=password)
            user.groups.add(group)
            user.save()
                
            # Create user account when register
            account = Profile.objects.create(user=user)
            account.save()
            if user.groups.first == "developer":
                project = Project.objects.create(user=user)
                project.save()
            
        
        except IntegrityError:
            return render(request, "capstone/register.html", {
                "message": "That username already exists."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))

    else:
        return render(request, "capstone/register.html")
 