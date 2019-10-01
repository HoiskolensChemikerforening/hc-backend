import React, { Component } from 'react';
import '../css/Committee.css';
import List from './Header1';

const list = [
  {
    'id': 1,
    'name': 'Industrikomiteen',
    'description': 'Studentenes bindeledd til arbeidslivet.'
  },
  {
    'id': 2,
    'name': 'pHaestkomiteen',
    'description': 'Fester hele natta.'
  },
  {
    'id': 3,
    'name': 'Kjellerstyret',
    'description': 'Aka vaskehjelp :P'
  }
];

class Committee extends Component {
  constructor(props) {
      super(props);
      this.state = { list };
    };

  render() {
    return [
      List("Komité"),
      <div className="Committee-wrapper">
        {this.state.list.map(item => (
            <div className="Committee" key={item.id}>
              <h2>{item.name}</h2>
              <p>{item.description}</p>
            </div>
        ))}
      </div>
    ];
  }
}

export default Committee;