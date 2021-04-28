import React from 'react'
import { Navbar, Nav, NavDropdown} from 'react-bootstrap';
import {Typography} from '@material-ui/core';
import 'bootstrap/dist/css/bootstrap.min.css';
import './navigationbar.css';

class NavigationBar extends React.Component {

  render() {
    return (
      <Navbar fixed="top" collapseOnSelect expand="lg" bg="dark" variant="dark">
        <Navbar.Brand href='/'>
          <img alt='Cheffu' className='app-logo'
          src= {require("../../images/cheffu-logo-white.png")} />
        </Navbar.Brand>
        <Navbar.Brand href='/about'><Typography variant='body1'>About</Typography></Navbar.Brand>
      </Navbar>

    )
  }
}

export default NavigationBar;