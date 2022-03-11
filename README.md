WEB APPLICATION CAPSTONE
======
***
- [Distinctiveness and complexity](#distinctiveness-and-complexity)
- [Content of the files created](#content-of-the-files-created)
  - [Template Inheritance](#template-inheritance)
  - [Index](#index)
  - [Register](#register)
  - [Login](#login)
  - [Logout](#logout)
  - [Account](#account)
  - [Add Project](#add-project)
  - [Messages](#messages)
  - [Home](#home)
  - [Developers](#developers)
- [Models](#models)
- [Run this application](#run-this-application)

## _Distinctiveness and complexity_

This is a Django project called `final_project` that contains single app called `capstone` and its functionality is a great tool for tech developers who would like to build their online portfolio. It represents all aspects of a proffesional portfolio with a showcase in sections regarding Developers Proffesional Biography,  Skills like programming languages and uploading videos with description of their completed Projects.

*Moreover*, the other group of users that can register on this web application is the ***Employer*** user who can see the user ***Developer*** portfolio and contact the same, through contact form.

*On the other hand*, all users can not make a posts, comments, likes, shares or send messages with each other like in online social networking, neither can sell or offer for sale at an auction their projects.

 ## *Content of the files created*
 
- #### Template Inheritance 
  all the next templates mentioned in this project inherit from `capstone/layout.html`, `navigation bar` with `navigation links` that are displayed according to :
 1. *If the user is not authenticated*
 
|   About    |    Login      |    Register  |
|   :----:   |    :---:      |    :----:    |

2. *If user is authenticated and is Employer*
 
|  Home    |    Account    |    Developers |    Logout   |  
| :----:   |    :---:      |    :----:     |    :----:   | 

3. *If user is authenticated and is Developer*

|  Home    |    Account    |    +Project   |    Messages  |    Logout   |  
| :----:   |    :---:      |    :----:     |    :----:    |    :----:   |
   
 
 In `capstone/urls.py` the default route loads an `index` function in `views.py` and renders simple template `capstone/index.html`.
- #### Index 
  is the introductory page that displays text as general information regarding the functionality of the application according to unauthenticated users, authenticated users of each group.

> ### If you are an Employer or a Developer
> By registering as an Employer, you will have a an accsess to the  Developers Profiles where you can contact them.
Or register as a Developer, and make your portfolio of Biography, Skills, Projects and employeers will find you.

##

 `/register` route renders template with register form `capstone/register.html`
- #### Register 
  User can register through form on _Capstone_ as user *Employer* by clicking the checkbox `Mark if Employer`,
 
 - [x] Mark if Employer

 while leaving it unchecked the user will be automatically signed into the user group *Developer*. Furthermore, `register` function in `views.py`  checks the registration form for validity, if the user already exists, if password is confirmed and if all fields are filled. At last, when users register they will have automatically created for them Account that later on can be filled. 
 
##
 
`/login` route renders template with login form, `capstone/login.html` 
- #### Login
  By entering the credentials in the form, the `login` function in `views.py` gets user's credential, authenticates the user and redirects to the index page. Login form is checked for validity of its credentials.
##

- #### Logout
  `/logout` route has `logout` function in `views.py` that logs the user out and redirects to the index page.
  
##

 `/account` route renders template `capstone/account.html` of django form with fields that use [django-widget-tweaks](https://pypi.org/project/django-widget-tweaks/)
- #### Account
   User can get into the account settings and add a profile image, then background image, as well as the biography which is a required field in difference with the other two fields from the form. Also if user wants to make changes to the account, the biography field will be populated and needs to be edited, while the images fields will show the already uploaded images that will be changed by choosing new files, or just clear out the current images by checking the 

- [ ] Clear Image

`account` function in `views.py` renders the form when a user tries to GET the page, after user submits the form with the uploaded Files using the POST request method, checks the form for validity and saves it.

##

`/addProject` route renders template `capstone/addProject.html` of django form with widget-tweaks customized form fields. 
- #### Add Project
  First, by clicking the `+Project` link in the navigaton bar User *Developer* is being taken to the page with the form that contains the fields `Title`, `Description` and Upload Video and by sumbitting the form user can add a project to his portfolio. Second, on the same page user can see preview of the project that was last added. 
`addProject` function in `views.py` renders the form when a user tries to GET the page and checks with conditions if the user has already added a project. After the submission of the form with the uploaded file through POST method, if form was valid, then it is saved.

##

- #### Messages
   When visiting messages page, User *Developer* can only see, without replying, for any received messages from an *Employer*, view a chosen message or delete the same.
`/allMessages/<str:username>` , where <str:username> is the username of the currently logged user, route renders template `capstone/allMessages.html`. Moreover the template has two main sections, first section contains all the messages sent to the user (element with an `id` of `msgContainer`) and the second contains a view of a chosen message (`div` with an `id` of `messageView`). When user clicks the **view** button on the message then the first section is hidden and second shown, or if the **Messages** button in `messageWiew` is clicked then the second section is hidden and the first shown. For this feature is used JavaScript file `capstone/myscript.js`, where when the DOM content of the page has been loaded all the elements inside the `messageView` section are created with event listener `onclick` attached on the button. When clicked `fetch` web `GET` request is made to `/messages/${msgId}`, which converts the result response into JSON, and the data needed to display the messageView. When visitng `GET/messages/<int:message_id>` data is displayed like this:

   ```json
   {
    "id": 11,
    "sender": "Employer",
    "title": "Regarding Project",
    "content": "This message is regarding ..", 
    "created": "2021-11-25"
   }
   ```
 
If message is not found the route through the function `message` in `views.py` returns `{"error": "Message not found."}` with status `404`.
When `delete` button is clicked using `fetch` method `DELETE`is made to `/messages/${messageId}` and the message is deleted and the route through the same function in `views.py` returns {"message": "Message deleted." with status `202`.
Another feature on this template is the *Scroll Back To Top Button*. In the same script, event listener `onscroll` more than `300px` is placed on the window, then the button shows and when is clicked scrolls the `document.body` to the top of the page.

##

- #### Home
  By clicking the first link in the navigation bar, icon **Home**, the user *Developer* opens the portfolio page. Route `/mycv/<str:username>` , where <str:username> is the username of the currently logged user, renders template `capstone/mycv.html`. 
  - first, the user's Image and background image are shown, 
  - then the section of the Developer skills is presented with the Skills `<select>` form, where the user can add programming languages and the skills will be displayed in the same section of the page. Furthermore, the `Skills` section displays the added skills using JavaScript file `capstone/myscript.js`, when the DOM content of the page has been loaded all the elements inside the (`div` with id `skillsSection`) are created like containers styled with classes, for example: 

    ```sass
        .Python {
            @extend %skillIcon;
            background-image: url("python.png");
        }
    ```

    With `fetch` GET method on `/skills` we get the data saved for the skills the user added and are saved into the database and we display it. Another feature is to delete the skill either by clicking on the icon for **delete** or by clicking on the skill container with a help of `fetch` method DELETE on `/skills/${skill_id}`. The `<select>` form for adding the skills is created with React file `skillsForm.js`. In the file choices for the form are saved as global variable called `options` an array of skills `{label: 'Python',value: 'Python'}`. Skills Component renders event to handleChange when skill is chosen and event handlesubmit to submit the form data through `fetch` method POST. `ReactDom` renders the component into the (`div` with id `reactSelect`) in the template.
  
  - *Next showcase* is the developers Proffesional Biography, which uses JavaScript file `capstone/myscript.js` to create and add functionality of the button with event listener `onclick` to show more of the Biography text or to show less. 
   This script is used to add to the same page `scroll buttons` to the top of the page if the user scrolled down more than `300px`, or to take the user to the bottom of the page if the user scrolled less then `300px`.
   
  - *Section* that displays the Projects that the user added. When **more** button on each project is clicked by the user *Employer* it takes the user to the project view page and displays more details in the description. On the other hand if `more` button is clicked by the *Developer* it takes the user to a page to view the project, edit or delete the same. This is achieved with help of JavaScript file `capstone/myscript.js` to add functionality of the button `edit` with event listener `onclick` to show the `edit form` and with `fetch` method GET on  `/projects/${projectid}` to get the data to populate the form and with `feth` method PUT `/projects/${projectid}` to edit the form. Event listener `onclick` on the `delete` button makes `fetch` method DELETE on `/projects/${projectId}` to delete the form. In function
   `projectView` in `views.py` data from edit or delete the project is being saved or deleted in the database. Function returns accordingly `{"message": "Project   Deleted"}` with status `202` or `{"message": "project edited"}` with status `202`.
   
  - *Last*, if the user is logged in as an *Employer* and visits the profile of the developer, the same page will have a `Contact Form` to send to the *Developer*. For this form is used React file `capstone/contactForm.js`. In this file the `<ContactUser/>` Component makes `fetch` GET request through `ComponentDidMount()` for the data of `currentUser` and `profileUser` so that we can use later as hidden fields when sending    the form. the Component renders events like : `handleChange` to toggle between showing and hiding the form `handleUsernameChange`,`handleTitleChange`,`handleContentChange` to handle the data in the form fields and `handleSubmit` to `fetch` method POST  `/messages` to post the form. In function `createMessage` in `views.py` the data for the new messsage is being saved into the database and returns  `{"message": "Message sent."}` with status `201`. `ReactDom` renders the component into the (`div` with id `contactForm1`) in the template.

##

`/developers` route renders template `capstone/developers.html`, while the function `developers` in views.py queries the database for users  *Developer*.
- #### Developers
  this page is available only to users that belong to a group *Employer*, and can be visited by clicking the _Developers_ link in the navigation bar. The employer will be taken to a page where all the Developers are displayed. By clicking on each developer's **more** button the user is taken to the Portfolio page of the Developer.

##

#### Models

*Models used for **capstone** application are:*
- **User** model inherits from `AbstractUser` and has the fields for `username`,`password`,`e-mail` and more already created,  
- **Profile** model has a user `OneToOne` field with User Model, `ImageFields` that upload to `images/` and `TextField` used for the user Biography 
- **Project** model has a user `ForeignKey` field of User Model, `FileField` that uploads to `videos/`, `Charfield` for the title,`TextField` for the description and `DateTimeField`
- **Skill** model has a user ForeignKey field of User Model and `CharField` that has choices set,
- **Message** model fist and second field is `ForeignKey` field of User Model, `CharField` for title, `TextField` for content and `DateTimeField`

This web application is designed to be mobile responsive with help of ***Bootstrap Library***- *flexbox grid system*, and `@media` queries for small, medium and large devices on few classes. 
Used for the styling of this project is used ***Sass*** and ***Bootstrap*** and for testing is used ***django testing*** - TestCase.

 ### Run this application
 
 1. To begin with, download zip and then unzip it. 
2. In the terminal, run `cd` into the `final_project` directory.
3. Then run `python manage.py makemigrations capstone` to make the migrations for the `capstone` app.
4. then, run `python manage.py migrate` to apply migrations to the database.
5. Last, run `python manage.py runserver` and register in the web application.

You can watch the demonstration of this project [here](https://youtu.be/EOLFC70krhE).
     
