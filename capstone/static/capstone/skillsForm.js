



'use strict';
const csrftoken = Cookies.get('csrftoken');


const options =  [
  {label: 'Skills', value: ''},
  {label: 'Python',value: 'Python'},
  {label:'Django',value:'Django'},
  {label: 'JavaScript',value: 'JavaScript'},
  {label: 'React',value: 'React'},
  {label: 'Vue',value: 'Vue'},
  {label: 'C',value: 'C'},
  {label: 'HTML',value: 'HTML'},
  {label: 'CSS',value: 'CSS'},
  {label: 'SASS',value: 'SASS'}];

class Skills extends React.Component {
  constructor(props) {
    super(props);
    this.state = { 
      skill: "", 
    };
    
  }

  render() {
    const handleChange = (event) => {
      this.setState({skill: event.target.value});
    }

    const handleSubmit = (event) => {
      
      const addSkill = this.state.skill;
      fetch("/skills", {
        method: 'POST',
        mode: 'same-origin',  // Do not send CSRF token to another domain.
        headers: {'X-CSRFToken': csrftoken},
        body: JSON.stringify({
          devSkills: addSkill,
        })
      })
      .then(response => response.json())
      .then(json => {
        console.log(json);
      })
      .catch(error => {
        console.log("error:", error);
      });
      location.reload();
}

    return (
      
        <form onSubmit={handleSubmit}>
        <div className="form-row justify-content-center align-items-center">
        <div className="col-auto my-1">
        <select className="custom-select mr-sm-2" value={this.state.skill} onChange={handleChange} id="id_devSkills">
          {options.map((option) => (
            <option value={option.value}>{option.label}</option>
          ))}
        </select>
        </div>
        <div>
          <a href="#id_devSkills"><input className="add" title="Add Skill" type="submit" value="Add"></input></a>
        </div>
        </div>
        </form>
      
    );
  }
}

if(document.querySelector('#reactSelect')){
  ReactDOM.render(<Skills/>, document.querySelector('#reactSelect'));
}