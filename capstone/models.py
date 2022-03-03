from django import forms
from django.db import models
from django.contrib.auth.models import AbstractUser, Group
from django.db.models.fields import TextField
from django.db.models.fields.related import ForeignKey
from django.forms.fields import CharField, ChoiceField
from django.forms.widgets import HiddenInput, Textarea, ClearableFileInput,TextInput
from django.forms import ModelForm, ImageField



# Create your models here.

class User(AbstractUser):
    pass


class Project(models.Model):
    user = models.ForeignKey(User,default=None,blank=True,on_delete=models.CASCADE,related_name="projectuser")
    video = models.FileField(upload_to="videos/",null=True)
    title = models.CharField(max_length=200,default=None,null=True)
    description = models.TextField(max_length=700,default=None,null=True)
    created = models.DateTimeField(auto_now_add=True)

    def serialize(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description
        }

class ProjectForm(ModelForm):
    description = Textarea(attrs={'class':'form-control','rows':'4','label':'Profile Image','placeholder':'Add a video description here'})
    class Meta:
        model = Project
        fields = ["title","description","video"]
        exclude = ["user"]


class Skill(models.Model):
    SKILLS_CHOICES = [
        ('', 'Skills'),
        ('Python', 'Python'),
        ('Django','Django'),
        ('JavaScript', 'JavaScript'),
        ('React','React'),
        ('Vue','Vue'),
        ('C', 'C'),
        ('HTML', 'HTML'),
        ('CSS', 'CSS'),
        ('SASS', 'SASS'),
    ]
    
    user = models.ForeignKey(User,default=None,blank = True,on_delete=models.CASCADE,related_name="userskills")
    devSkills = models.CharField(max_length=20,choices=SKILLS_CHOICES,default='',verbose_name="")
    
    def serialize(self):
        return {
            "id": self.id,
            "devSkills": self.devSkills,
        }

class SkillForm(ModelForm):
   
    class Meta:
        model = Skill
        exclude = ["user"]
        
    SKILLS_CHOICES = [
    ('', 'Skills'),
    ('Python', 'Python'),
    ('Django','Django'),
    ('JavaScript', 'JavaScript'),
    ('React','React'),
    ('Vue','Vue'),
    ('C', 'C'),
    ('HTML', 'HTML'),
    ('CSS', 'CSS'),
    ('SASS', 'SASS'),

]
    devSkills = ChoiceField(label="",choices=SKILLS_CHOICES,widget=forms.Select(attrs={'class': 'custom-select'}))       

class Message(models.Model):
    user = models.ForeignKey(User,blank = True,on_delete=models.CASCADE,related_name="messanger")
    recipient = models.ForeignKey(User,default=None,blank = True,null=True,on_delete=models.CASCADE,related_name="receiver")
    sender = models.CharField(max_length=200,default=None)
    title = models.CharField(max_length=200,default=None)
    content = models.TextField(max_length=500,default="")
    created = models.DateTimeField(auto_now_add=True)
    
    def serialize(self):
        return {
            "id": self.id,
            "sender": self.sender,
            "title": self.title,
            "content": self.content,
            "created": self.created
        }

class MessageForm(ModelForm):
    class Meta:
        model = Message
        fields = ["user","recipient","sender","title", "content"]
        
        labels = {
            "user": "",
            "recipient": "",
            "sender": "",
            "title": "",
            "content": ""
        }
        widgets = {
            "user": HiddenInput(attrs={'class': "form-control",'id':'messageUser'}),
            "recipient": HiddenInput(attrs={'class': "form-control",'id':'messageTo'}),
            "sender": TextInput(attrs={'class': "form-control",'id':'messageName','placeholder':'Name','required':True}),
            "title": TextInput(attrs={'class': "form-control",'id':'messageTitle','placeholder':'Title..','required':True}),
            "content": Textarea(attrs={'class': "form-control",'id':'messageContent','rows': "4",'placeholder':'Your message here...','required': True})
        }


class Profile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,related_name="profileuser")
    userImage = models.ImageField(upload_to="images/",blank=True,null=True)
    backgroundImage = models.ImageField(upload_to="images/",blank=True,null=True)
    bio = models.TextField(max_length=1000, default="",null=True)
    
    def __str__(self):
        return f"{self.user}"

    # Method for user Image field to add default image if the user didn't add one
    def profileimage(self):
        if self.userImage and hasattr(self.userImage, 'url'):
            return self.userImage.url
        else:
            return "capstone\static\capstone\noimg.png"

    def background(self):
        if self.backgroundImage and hasattr(self.backgroundImage, 'url'):
            return self.backgroundImage.url
        else:
            return "capstone\static\capstone\nobackground.png"    

class MyClearableFileInput(ClearableFileInput):
    initial_text = "Currently"
    input_text = "change"
    clear_checkbox_label = "Clear Image"

class ProfileForm(ModelForm):
    userImage = ImageField(label="Profile Image", required=False, widget=MyClearableFileInput)
    backgroundImage = ImageField(label="Background Image", required=False, widget=MyClearableFileInput)
    bio = Textarea(attrs={'placeholder':'Your Professional Biography goes here ...'})
    
    class Meta:
        model = Profile
        fields = ["userImage","backgroundImage","bio"]
        exclude = ["user"]
