import React from 'react';

function MachineStatusComponent({ machines }) {
  return (
    <div className="machine-status">
      <h2>Machine Status</h2>
      {machines && machines.length ? (
        <table className="status-table">
          <thead>
            <tr>
              <th>Name</th>
              <th>Status</th>
              <th>Priority</th>
              <th>Availability</th>
            </tr>
          </thead>
          <tbody>
            {machines.map((machine) => (
              <tr key={machine.id}>
                <td>{machine.name}</td>
                <td>{machine.status}</td>
                <td>{machine.priority}</td>
                <td>{new Date(machine.available_from).toLocaleString()}</td>
              </tr>
            ))}
          </tbody>
        </table>
      ) : (
        <p>No machines available.</p>
      )}
    </div>
  );
}

export default MachineStatusComponent;