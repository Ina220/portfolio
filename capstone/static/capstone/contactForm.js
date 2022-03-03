

const csrftoken = Cookies.get('csrftoken');

'use strict';


class ContactUser extends React.Component {
    constructor(props) {
        super(props);

        this.state = {
            currentUser: "",
            profileUser: "",
            username: "",
            title: "",
            content: "",
            
            showContactForm: false,
        }
    }  
    
    componentDidMount() {
        fetch('/developerProfile')
        .then(response => response.json())
        .then(data => this.setState({ 
            currentUser: data.currentUser,
            profileUser: data.profileUser
        }));
        
        
    }

    render() {

        const handleChange = (event) => {
            // the initial state of false is set to true
            this.setState({ showContactForm: !this.state.showContactForm });
        };

        const handleUsernameChange = (event) => {
            this.setState({username:event.target.value});
        };

        const handleTitleChange = (event) => {
            this.setState({title:event.target.value});
        };
        const handleContentChange = (event) => {
            this.setState({content:event.target.value});
        };


        const handleSubmit = (event) => {
            // fetch post with content value
            event.preventDefault();
            
            fetch('/messages', {
                
                method: 'POST',
                mode: 'same-origin',  // Do not send CSRF token to another domain.
                headers: {'X-CSRFToken': csrftoken},
                body: JSON.stringify({
                    currentUser: this.state.currentUser,
                    profileUser: this.state.profileUser,
                    sender: this.state.username,
                    title: this.state.title,
                    content: this.state.content, 
                }),
            })
            .then(response => response.json())
            .then(json => {
                // print json
                console.log(json);
            })
            .catch(error => {
                console.log('Error:', error);
            });
           
            location.reload();
        };
    
    // the initial state of the button is " "
    // toggle "hide" and "show" form
    const buttonToggle = this.state.showContactForm;
    return(
        <div>
            <button onClick={handleChange} className="circle">{buttonToggle?'X':<i class="fas fa-pen-alt"></i>}</button>
               
                {
                    // Conditional rendering
                    // after clicking the button, if the state is "True" show the Form, otherwise hide it
                    buttonToggle && (
                        <div className="row justify-content-center">
                        <div className="col-sm-12 col-md-8">
                        <form onSubmit={handleSubmit} accept-charset="utf-8">
                            <input type="hidden" value={this.state.currentUser}/>
                            <input type="hidden" value={this.state.profileUser}/>
                            <input type="text" value={this.state.username} onChange={handleUsernameChange} className="form-control" autofocus placeholder="Your Name" required/>
                            <input type="text" value={this.state.title} onChange={handleTitleChange} className="form-control" autofocus placeholder="message Title" required/>
                            <textarea value={this.state.content} onChange={handleContentChange} className="form-control" rows="7" placeholder="Your Message..." required/>
                            <button type="submit" title="Send" className="plane"><i class="fas fa-paper-plane"></i></button>
                        </form>
                        </div>
                        </div>
                    )
                }
        </div>
    );
   
}

};
if (document.querySelector("#contactForm1")) {
    ReactDOM.render(<ContactUser/>, document.querySelector("#contactForm1"));
};



