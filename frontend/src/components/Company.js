import React, { Component } from 'react';
import '../css/Company.css';
import List from './Header1';


class Company extends Component {
  state = {
    companies: []
  };

  async componentDidMount() {
    try {
      const res = await fetch('http://127.0.0.1:8000/bedrift_api/');
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
      List("Bedrift"),
      <div className="Company-wrapper">
        {this.state.companies.map(item => (
            <div className="Company" key={item.id}>
              <h2>{item.name}</h2>
              <span>{item.description}</span>
            </div>
        ))}
      </div>
    ];
  }
}

export default Company;
