from django.urls import path, re_path 
from . import views


urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.log_in, name="login"),
    path("logout", views.log_out, name="logout"),
    path("register", views.register, name="register"),
    path("account", views.account, name="account"),
    path("addProject", views.addProject, name="addProject"),
    path("project/<int:project_id>", views.project, name="project"),
    path("mycv/<str:username>", views.mycv, name="mycv"),
    path("developers", views.developers, name="developers"),
    path("allMessages/<str:username>", views.allMessages, name="allMessages"),
   
    # API
    path("messages", views.createMessage, name="createMessage"),
    path("messages/<int:message_id>", views.message, name="message"),
    path("developerProfile", views.developerProfile, name="devProfile"),
    path("skills", views.skills, name="skills"),
    path("skills/<int:skill_id>", views.skill, name="skill"),
    path("projects", views.createProject, name="createProjects"),
    path("projects/<int:project_id>", views.projectView, name="projectView")
    
    
]