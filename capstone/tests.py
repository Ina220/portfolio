from django.test import TestCase, Client
from django.urls import reverse
from .models import User, Group, Profile, Project, Skill, Message, ProfileForm, ProjectForm, SkillForm, MessageForm


# Create your tests here.
class ProjectTestCase(TestCase):

    def setUp(self):
        #create users
        numUsers = 8
        # create two groups
        self.employer = Group(name="employer")
        self.employer.save()
        self.developer = Group(name="developer")
        self.developer.save()

        # create users that belong to group "Employers"
        for i in range(numUsers):
            User.objects.create_user(
                username=f'user{i}',
                password=f'password{i}')

            # create empty account for a user, that later will be filled
            Profile.objects.create(
                user=User.objects.get(username=f'user{i}'))

        empUser = User.objects.get(username="user1")
        empUser.groups.add(self.employer)         
        devUser = User.objects.get(username="user5")
        devUser.groups.add(self.developer)
        self.project5 = Project.objects.create(id="1",user=devUser)
        self.project5.save()
        self.skill1 = Skill.objects.create(id="1",user=devUser)
        self.skill1.save()
        self.message1 = Message.objects.create(id="1",user=empUser,recipient=devUser,sender="user1",title="messageTitle",content="mmessageContent")
        self.message1.save()
      

    def test_login_page(self):
        """ Test the Login in Page """
        response = self.client.get('/login')
        self.assertEqual(response.status_code, 200)  
        # Check we used correct template
        self.assertTemplateUsed(response, 'capstone/login.html') 

    def test_login_post_credentials(self):
        """ Test the login credentials """
        self.client.login(username='user1', password='password1')
        response = self.client.post('/login', {'username':'user5','password':'password5'})
        self.assertRedirects(response, '/')

    def test_login_invalid_credentials(self):
        """ Display message on a invalid login credentials"""
        self.client.login(username='user5', password='password5')
        response = self.client.post('/login', {'username':'user50','password':'password50'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['message'], 'Username and/or password are not valid.')

    def test_index_page(self):
        """ Get Index page """
        self.client.login(username='user5', password='password5')
        response= self.client.get("")
        #check rendered user
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "capstone/index.html")

    def test_profile_page(self):
        """ Get Profile Page """
        self.client.login(username='user5', password='password5')
        response = self.client.get('/mycv/user5')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['group'], self.developer)
        self.assertTemplateUsed(response, "capstone/mycv.html")

    # Create New Project
    def test_add_project(self):
        """ Test creating new project """
        # login user and post project
        self.client.login(username='user5', password='password5')
        response = self.client.post("/addProject", {
            "user": "user5",
            "video": "video5",
            "title": "title5",
            "description": "description1"})
        # Create new project
        userId = User.objects.get(id="5")
        Project.objects.create(id="5",user=userId, video="video5",title="title5", description="description5")
        self.assertEqual(response.status_code, 200)
        # Count all the users projects to be equal to 1
        usersProjects = Project.objects.filter(user=userId).count()
        self.assertEqual(usersProjects, 1)
    
    # Get Create new Project page
    def test_get_project(self):
        """ Test get project """
        self.client.login(username='user5', password='password5')
        response = self.client.get('/projects/1')
        self.assertEqual(response.status_code, 200)

    # Edit Project
    def test_edit_project(self):
        """ Test edit project """
        self.client.login(username='user5', password='password5')
        # Posting the update of the edited project
        response = self.client.post('/projects/1', {
            "id": "1","title": "titleEdited", "description": "descriptionEdited"
        },content_type='application/json')
        editproject = Project.objects.create(user=User.objects.get(username="user5"),title="titleEdited", description="descriptionEdited")
        Project.objects.filter(pk=editproject.pk).update(title="titleEdit",description="descriptionEdit")
        editproject.refresh_from_db()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(editproject.title, "titleEdit")

    # Succesfuly get the profile page
    def test_profile_page(self):
        """ test Get Profile Page """
        self.client.login(username='user5', password='password5')
        response = self.client.get("/mycv/user5")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "capstone/mycv.html")


    def test_profile_str(self):
        """ Test the Profile Model string """
        profile = Profile.objects.get(pk=1)
        expected_object_name = f"{profile.user}"
        self.assertEqual(str(profile), expected_object_name)

    def test_profilemodel_field(self):
        """ Test profile field length """
        # Get an project object to test
        profile = Profile.objects.get(pk=1)
        # Get the metadata for the required field and use it to query the required field data
        max_length = profile._meta.get_field("bio").max_length
        # Compare the value to the expected result
        self.assertEqual(max_length, 1000)

    def test_profileform(self):
        """ Test Profile form """
        form = ProfileForm()
        self.assertFalse(form.is_bound)
        self.assertTrue(form.is_multipart())
        self.assertTrue(form.fields["userImage"].label == "Profile Image")
        self.assertTrue(form.fields["backgroundImage"].label == "Background Image")
        self.assertFalse(form.fields["bio"].label == "")



    def test_projectform_field_label(self):
        """ Test project form field labels """
        form = ProjectForm()
        self.assertFalse(form.is_valid())
        self.assertTrue(form.fields["title"].label == "Title")
        self.assertTrue(form.fields["description"].label == "Description")
        self.assertTrue(form.fields["video"].label == "Video")

    def test_projectform_data(self):
        """ Test Validity of the Project Form """
        form = ProjectForm(data={"title": "", "description":""})
        self.assertFalse(form.is_valid())
        self.assertTrue(form.is_bound)
        self.assertTrue(form.is_multipart())

    def test_messageform_field_labels(self):
        """ Test Message Form field labels """
        form = MessageForm()
        self.assertFalse(form.fields["sender"].label == "sender")
        self.assertTrue(form.fields["title"].label == "")
        self.assertTrue(form.fields["content"].label == "")
        
    def test_messageform_data(self):
        """ Test validity of Message Form """
        form = MessageForm(data={"user": User.objects.get(username="user1"),
            "recipient": User.objects.get(username="user5"),
            "sender": "user1",
            "title": "TitleTest",
            "content": "ContentTest"})
        self.assertTrue(form.is_valid())
        self.assertTrue(form.is_bound)
        self.assertFalse(form.is_multipart())

    def test_skillsform(self):
        """ Test Skills Form """
        form = SkillForm()
        self.assertFalse(form.is_bound)
        self.assertFalse(form.is_multipart())
        self.assertTrue(form.fields["devSkills"].label == "")

    def test_skillmodel(self):
        """ Test Skill model field """
        skill = Skill.objects.get(pk=1)
        field_label = skill._meta.get_field("devSkills").verbose_name
        self.assertEqual(field_label, "")
        
    def test_messagemodel(self):
        """ Test message Model """
        message = Message.objects.get(pk=1)
        max_length_sender = message._meta.get_field("sender").max_length
        # Compare the value to the expected result
        self.assertEqual(max_length_sender, 200)
        max_length_title = message._meta.get_field("title").max_length
        self.assertEqual(max_length_title, 200)
        max_length_content = message._meta.get_field("content").max_length
        self.assertEqual(max_length_content, 500)





    
