import React from 'react';
import '../css/Header1.css';

function List(props) {
  return (
    <div className="List">
      <h1>{props.title}</h1>
    </div>
  );
}

export default List;
