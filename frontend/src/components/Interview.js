import React, {Component} from 'react';
import '../css/Interview.css';
import List from './Header1';

const title = "Intervju";

const list = [
  {
    'id': 1,
    'name': 'Per Olsen',
    'bedrift': 'NTNU',
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
      <div className="Interview-width">
        <List title={title}/>
        <div className="Committee-wrapper">
          {this.state.list.map(interview => (
              <div className="Interview" key={interview.id}>
                <h3>{interview.name} – {interview.bedrift}</h3>
              </div>
          ))}
        </div>
      </div>
    ];
  }
}

export default Committee;