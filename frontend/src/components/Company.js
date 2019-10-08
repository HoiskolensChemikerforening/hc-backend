import React, {Component} from 'react';
import '../css/Company.css';
import List from './Header1';

const title = "Bedrift";

class Company extends Component {
  state = {
    companies: []
  };

  async componentDidMount() {
    try {
      const res = await fetch('http://127.0.0.1:8000/bedrift_api/bedrift/');
      const companies = await res.json();
      this.setState({
        companies
      });
    } catch (e) {
      console.log(e);
    }
  }

  render() {
    return [
      <div className="Company-list">
        <List title={title}/>
        <div className="Company-wrapper">
          {this.state.companies.map(company => (
              <div className="Company" key={company.id}>
                <div className="Company-logo-wrapper">
                  <img src={company.logo} className="Company-logo"></img>
                </div>
                <h2>{company.name}</h2>
                <span>{company.description}</span>
              </div>
          ))}
        </div>
        <button className="Button-black">Alle bedrifter</button>
      </div>
    ];
  }
}

export default Company;
