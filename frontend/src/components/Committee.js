import React, {Component} from 'react';
import '../css/Committee.css';
import List from './Header1';

const title = "Komiteen";

const list = [
  {
    'id': 1,
    'name': 'Industrikomiteen',
    'description': 'Studentenes bindeledd til arbeidslivet.',
    'image': '/indkom.jpg',
  },
];

class Committee extends Component {
  constructor(props) {
    super(props);
    this.state = {list};
  };

  render() {
    return [
      <div className="Committee-width">
        <List title={title}/>
        <div className="Committee-wrapper">
          {this.state.list.map(item => (
              <div className="Committee" key={item.id}>
                <img className="Committee-image" src={item.image}></img>
                <h2>{item.name}</h2>
                <p>{item.description}</p>
              </div>
          ))}
        </div>
      </div>
    ];
  }
}

export default Committee;