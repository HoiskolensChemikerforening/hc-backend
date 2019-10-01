import React from 'react';
import '../css/Navbar.css';

function Navbar() {
  return (
    <div className="Navbar">
      <div className="Logo">
        <div className="Logo-overlayed">
          <h1 className="Logo-text"><span>&nbsp;Høiskolens&nbsp;</span></h1>
          <div className="overlay">
          </div>
        </div>
        <div className="Logo-overlayed">
          <h1 className="Logo-text"><span>&nbsp;Chemikerforening&nbsp;</span></h1>
          <div className="overlay">
          </div>
        </div>
      </div>
    </div>
  );
}

const navbar = <Navbar/>;

export default navbar