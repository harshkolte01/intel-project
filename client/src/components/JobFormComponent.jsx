import React, { useState } from 'react';

function JobFormComponent({ onAddJob, machines }) {
  const [jobId, setJobId] = useState('');
  const [operations, setOperations] = useState([{ machine_id: '', duration: '' }]);

  const handleSubmit = (e) => {
    e.preventDefault();
    onAddJob({ job_id: jobId, operations });
    setJobId('');
    setOperations([{ machine_id: '', duration: '' }]);
  };

  const addOperation = () => {
    setOperations([...operations, { machine_id: '', duration: '' }]);
  };

  return (
    <div className="job-form">
      <h2>Add New Job</h2>
      <form onSubmit={handleSubmit}>
        <input
          type="text"
          placeholder="Job ID"
          value={jobId}
          onChange={(e) => setJobId(e.target.value)}
          required
        />
        {operations.map((op, index) => (
          <div key={index} className="operation">
            <select
              value={op.machine_id}
              onChange={(e) => {
                const newOps = [...operations];
                newOps[index].machine_id = e.target.value;
                setOperations(newOps);
              }}
              required
            >
              <option value="">Select Machine</option>
              {machines.map((m) => (
                <option key={m.id} value={m.id}>{m.name}</option>
              ))}
            </select>
            <input
              type="number"
              placeholder="Duration (min)"
              value={op.duration}
              onChange={(e) => {
                const newOps = [...operations];
                newOps[index].duration = e.target.value;
                setOperations(newOps);
              }}
              required
            />
          </div>
        ))}
        <button type="button" onClick={addOperation}>Add Operation</button>
        <button type="submit">Submit Job</button>
      </form>
    </div>
  );
}

export default JobFormComponent;