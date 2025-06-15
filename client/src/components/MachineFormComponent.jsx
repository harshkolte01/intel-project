import React, { useState } from 'react';

function MachineFormComponent({ onAddMachine }) {
  const [machineName, setMachineName] = useState('');
  const [status, setStatus] = useState('available');
  const [priority, setPriority] = useState(1);

  const handleSubmit = (e) => {
    e.preventDefault();
    if (machineName.trim()) {
      onAddMachine({ name: machineName, status, priority });
      setMachineName('');
      setStatus('available');
      setPriority(1);
    }
  };

  return (
    <div className="machine-form">
      <h2>Add New Machine</h2>
      <form onSubmit={handleSubmit}>
        <input
          type="text"
          placeholder="Machine Name"
          value={machineName}
          onChange={(e) => setMachineName(e.target.value)}
          required
        />
        <select
          value={status}
          onChange={(e) => setStatus(e.target.value)}
          required
        >
          <option value="available">Available</option>
          <option value="maintenance">Maintenance</option>
          <option value="offline">Offline</option>
        </select>
        <select
          value={priority}
          onChange={(e) => setPriority(Number(e.target.value))}
          required
        >
          <option value={1}>High Priority (1)</option>
          <option value={2}>Medium Priority (2)</option>
          <option value={3}>Low Priority (3)</option>
        </select>
        <button type="submit">Submit Machine</button>
      </form>
    </div>
  );
}

export default MachineFormComponent;