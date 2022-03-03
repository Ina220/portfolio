
document.addEventListener('DOMContentLoaded', function() {
    console.log("starting");
    const csrftoken = Cookies.get('csrftoken');
    
    // Create button to show more text or show less
    if(document.querySelector("#moreless")) {
        document.querySelectorAll(".moreLess").forEach(p => {
            for(i in p.classList) {
                if(p.classList[i] === "text-truncate-p"){
                   const moreless = document.createElement("button");
                   moreless.className = "btn btn-outline-secondary";
                   moreless.innerHTML = "more";
                   document.querySelector("#moreless").append(moreless);
                   moreless.onclick = () => {
                      
                       if(moreless.innerHTML === "more"){
                        p.classList.remove("text-truncate-p");
                        moreless.innerHTML = "less";
                       } 
                       else {
                        p.classList.add("text-truncate-p");
                        moreless.innerHTML = "more";
                       }
                   }
                }    
            }
        })
    }
    btnTop = document.querySelector("#btnTop");
    mediaBtn = document.querySelector("#mediaBtn");
    // When the user scrolls more then 300px down the document the button shows
    if (btnTop) {
        window.onscroll = () => {

            if (document.body.scrollTop > 300 || document.documentElement.scrollTop > 300) {
                btnTop.style.display = "block";
                if(mediaBtn) {
                    mediaBtn.style.display = "none";
                }
                
            } else {
                btnTop.style.display = "none";
                if(mediaBtn) {
                    mediaBtn.style.display = "block";
                }
            };
            
        }
    }
    
    //When button is clicked scroll up to the top of the document
    if (btnTop) {
        btnTop.onclick = () => {
            document.body.scrollTop = 0;//For Safari
            document.documentElement.scrollTop = 0;//For Chrome, Firefox, IE, Opera
        }
    }
    if (mediaBtn) {
        mediaBtn.onclick = () => {
            const socialMedia = document.querySelector("#socialMedia");
            socialMedia.scrollIntoView();
            
        }
    }
    
    // create elements to display the skills
    // create delete skills
    if (document.querySelector("#skillsSection")) {
        const row = document.createElement("div");
        row.className = "row text-center padding justify-content-center mt-5";
        document.querySelector("#skillsSection").append(row);
        fetch("/skills")
        .then(response => response.json())
        .then(data => {
            console.log(data.usersSkills);
            const allskills = data.usersSkills;
            
            
            allskills.forEach(skill => {
                container = document.createElement("div");
                container.className = "cont";
                container.dataset.section = skill.devSkills;
                container.id = skill.id;
                if(data.currentUser === data.profileUserId){
                container.onclick = () => {
                    deleteSkill(skill.id);
                }
            }
                row.append(container);
                const skillicon = document.createElement("div");
                skillicon.dataset.section = container.dataset.section;
                skillicon.className = "col-12 skill" + " " + container.dataset.section;
                container.append(skillicon);
                if(data.currentUser === data.profileUserId){
                    const delIcon = document.createElement("i");
                    delIcon.className = "far fa-trash-alt delIcon";
                    delIcon.dataset.section = container.dataset.section;
                    container.append(delIcon);
                    if(delIcon.dataset.section === container.dataset.section){
                        delIcon.onclick = () => {    
                            deleteSkill(skill.id);
                        }     
                    };
                }
                    
                // Check if Skills form is on teh selected page
                if (document.querySelector("#id_devSkills")) {
                    // The SelectForm option can not be choosen again after it is added already
                    // hide option
                    selectForm = document.querySelector("#id_devSkills");
                    selectForm.childNodes.forEach(option => {
                        
                        if (option.value === container.dataset.section) {
                           option.style.display = "none";
                        }  
                   })  
                   
                }
            })
        })
        
    }
    
    if(document.querySelector("#editProjectBtn")){
        const editProjectBtn = document.querySelector("#editProjectBtn");
        const projectId = editProjectBtn.dataset.section;
        editProjectBtn.onclick = () => {
            window.scroll({bottom: 0});
            document.querySelector("#projectChange").style.display = "none";
            document.querySelector("#editSection").style.display = "block";
            const scroll = document.getElementById("scroll");
            console.log(scroll);
            
            const editForm = document.getElementById("editForm");
            
            console.log(editForm);
                 edited(projectEdit(`${projectId}`));
        };
        
    }
    // if there is a delete button on click fetch delete projects/projectid
    if(document.querySelector("#delProjectBtn")){
        const delProjectBtn = document.querySelector("#delProjectBtn");
        const projectId = delProjectBtn.dataset.section;
        delProjectBtn.onclick = () => {
            fetch(`/projects/${projectId}`, {
                method: "DELETE",
                mode: 'same-origin',  // Do not send CSRF token to another domain.
                headers: {'X-CSRFToken': csrftoken},
            })
            .then(response => response.json())
            .catch(error => {
                console.log("Error:", error);
            });
        };
        
    }


// submit edited form
function edited() {
    
    const editForm = document.querySelector("#editForm");
    const projectid = editForm.dataset.section; 
    editForm.style.display = "block";
    editForm.onsubmit = () => {
    const title = document.querySelector("#editTitle").value;
    const description = document.querySelector("#editDescription").value;    
    fetch(`/projects/${projectid}`, {
        method: "PUT",
        mode: 'same-origin',  // Do not send CSRF token to another domain.
        headers: {'X-CSRFToken': csrftoken},
        body: JSON.stringify({
            title: title,
            description: description
        })
    })
    .then(response => response.json())
    .then(json => {
        console.log(json)
    })
    .catch(error => {
        console.log('Error:', error);
    });
    fetch(`/projects/${projectid}`)
    .then(response => response.json())
    .then(project => {
        console.log(project);
        document.querySelector("#cardTitle").innerHTML = project.title;
        document.querySelector("#cardText").innerHTML = project.description;
        
    })
    document.querySelector("#projectChange").style.display = "block";
    document.querySelector("#editSection").style.display = "none";
    return false;
    
    }
    
}

// Create One Message View
if(document.querySelector("#messageView")){
    const messageView = document.querySelector("#messageView");
    messageView.style.display = "none";
    const row = document.createElement("div");
    row.className = "row welcome text-center";
    messageView.append(row);
    const back = document.createElement("button");
    back.className = "btn btn-link btn-lg";
    back.style.display = "none";
    back.innerHTML = `<i class="far fa-arrow-alt-circle-left"></i>` + "Messages";
    row.append(back);
    const column = document.createElement("div");
    column.className = "col-12";
    row.append(column);
    const title = document.createElement("h3");
    title.className = "mt-4 title";
    column.append(title);
    const sender = document.createElement("div");
    sender.className = "col-12 title";
    row.append(sender);
    const content = document.createElement("div");
    content.className = "col-12 mt-4";
    row.append(content);
    const lead = document.createElement("p");
    lead.className= "lead";
    content.append(lead);
    const created = document.createElement("p");
    created.className = "text-muted small";
    column.append(created);
    if(document.querySelector("#viewMsg")){
        document.querySelectorAll(".viewMsg").forEach(button => {
        const msgId = button.dataset.section;
        
        button.onclick = () => {

            fetch(`/messages/${msgId}`)
            .then(response => response.json())
            .then(message => {
                title.innerHTML = message.title;
                content.innerHTML = `<p class="lead">${message.content}</p>`;
                created.innerHTML = message.created;
                sender.innerHTML =`<h4><i><small>From</small></i> <mark><strong class="title">${message.sender}</strong></mark><h4>`;

            });
            const allmessages = document.querySelectorAll(".msgContainer");
            console.log(allmessages);
            allmessages.forEach(div => {
                div.style.display = "none"
            })
            messageView.style.display = "block";
            back.style.display = "block";
            back.onclick = () => {
                messageView.style.display = "none";
                back.style.display = "none";
                allmessages.forEach(div => {
                    div.style.display = "block"
                })
            }  
        }
    });
}
if(document.querySelector("#delMsg")) {
    document.querySelectorAll(".delMsg").forEach(button => {
        const messageId = button.dataset.section; 
        button.onclick = () => {
            fetch(`/messages/${messageId}`, {
                method: "DELETE", 
                mode: 'same-origin',  // Do not send CSRF token to another domain.
                headers: {'X-CSRFToken': csrftoken},
            })
            .then(response => response.json())
            .then(json => {
                console.log(json);
            })
            .catch(error => {
                console.log("Error:", error);
            })
            location.reload();
        };
    })
}
}
// Show the section to edit the project and populate the form with existing project content
function projectEdit(project_id) {
    
    fetch(`/projects/${project_id}`)
    .then(response => response.json())
    .then(project => {
        console.log(project);
       
        const title = document.querySelector("#editTitle");
        title.value = project.title;
        
        const description = document.querySelector("#editDescription");
        description.value = project.description;
    
    })
}
// Delete Skill
function deleteSkill(skill_id) {
    fetch(`/skills/${skill_id}`, {
        method: "DELETE",
        mode: 'same-origin',  // Do not send CSRF token to another domain.
        headers: {'X-CSRFToken': csrftoken},
    })
    .then(response => response.json())
    .catch(error => {
        console.log('Error:', error);
    });
    console.log("Deleted");
    window.location.reload();
}  


    
})// DomContentLoaded


