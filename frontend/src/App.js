import React from 'react';
import './App.css';

export default class Table extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      data: [
        { id: 1, sensortype: 'pressure', reading: 20.5, timestamp: 1583286436.841013 },
        { id: 2, sensortype: 'radio', reading: 50.5, timestamp: 1583286445.841013 },
        { id: 3, sensortype: 'peizo', reading: 100, timestamp: 1583286448.841013 },
        { id: 4, sensortype: 'temperature', reading: 300, timestamp: 1583286452.841013 },
      ],
    };
  }
  
  componentWillMount() {
    fetchData(this.props.sensorid).then(
      (response) => {
        this.setState({
          data: response.data,
        });
      }
    );
  }

  getTabularData() {
    return this.state.data.map((row) => {
      const {id, sensortype, reading, timestamp} = row;
      return (
        <tr key={id}>
          <td>{id}</td>
          <td>{sensortype}</td>
          <td>{reading}</td>
          <td>{timestamp}</td>
        </tr>
      );
    });
  }

  getHeader() {
    const keys = Object.keys(this.state.data[0]);
    return keys.map((key, index) => {
      return <th key={index}>{key.toUpperCase()}</th>
    })
  }

  render() {
    return (
      <div>
        <h1 id="title">SensorData Table</h1>
        <table id="sensordata">
          {this.getHeader()}
          {this.getTabularData()}
        </table>
      </div>
    );
  }
}

const fetchData = (sensorid) => {
  return new Promise((resolve, reject) => {
    const url = `http://localhost:5000/api/v1/sensordata/${sensorid}`;
    const request = new XMLHttpRequest();
    // Never do this.....
    request.setRequestHeader('Authorization', `Basic: ${atob('sjaffer:password')}`);
    request.open('GET', url);
    request.onload = () => {
      (request.status === 200
        ? resolve(JSON.parse(request.response))
        : reject(Error(request.statusText))
      )
    };
    request.onerror = (err) => reject(err);
    request.send();
  });
}