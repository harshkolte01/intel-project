import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Route, Routes, Link } from 'react-router-dom';
import axios from 'axios';
import JobFormComponent from './components/JobFormComponent';
import GanttChartComponent from './components/GanttChartComponent';
import MachineStatusComponent from './components/MachineStatusComponent';
import MachineFormComponent from './components/MachineFormComponent';
import GanttChartPage from './components/GanttChartPage';
import ErrorBoundary from './components/ErrorBoundary';
import './styles_main.css';

function AppMain() {
  const [jobs, setJobs] = useState([]);
  const [machines, setMachines] = useState([]);
  const [schedule, setSchedule] = useState([]);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    try {
      const baseUrl = process.env.NODE_ENV === 'production' ? 'http://server:8000' : 'http://localhost:8000';
      const [jobsRes, machinesRes, scheduleRes] = await Promise.all([
        axios.get(`${baseUrl}/jobs`),
        axios.get(`${baseUrl}/machines`),
        axios.get(`${baseUrl}/schedule`),
      ]);
      setJobs(jobsRes.data || []);
      setMachines(machinesRes.data || []);
      setSchedule(scheduleRes.data || []);
      setError(null);
    } catch (error) {
      console.error('Error fetching data:', error);
      setError('Failed to load data. Please try again.');
    }
  };

  const handleAddJob = async (job) => {
    try {
      const baseUrl = process.env.NODE_ENV === 'production' ? 'http://server:8000' : 'http://localhost:8000';
      await axios.post(`${baseUrl}/jobs`, job);
      fetchData();
    } catch (error) {
      console.error('Error adding job:', error);
      setError('Failed to add job.');
    }
  };

  const handleAddMachine = async (machine) => {
    try {
      const baseUrl = process.env.NODE_ENV === 'production' ? 'http://server:8000' : 'http://localhost:8000';
      await axios.post(`${baseUrl}/machines`, machine);
      fetchData();
    } catch (error) {
      console.error('Error adding machine:', error);
      setError('Failed to add machine.');
    }
  };

  return (
    <Router>
      <Routes>
        <Route
          path="/"
          element={
            <div className="app">
              <h1>Smart Scheduling System</h1>
              {error && <p style={{ color: 'red' }}>{error}</p>}
              <ErrorBoundary>
                <div className="dashboard">
                  <div>
                    <MachineFormComponent onAddMachine={handleAddMachine} />
                    <JobFormComponent onAddJob={handleAddJob} machines={machines} />
                  </div>
                  <div>
                    <Link to="/gantt">View Gantt Chart in New Page</Link>
                    <GanttChartComponent schedule={schedule} machines={machines} />
                    <MachineStatusComponent machines={machines} />
                  </div>
                </div>
              </ErrorBoundary>
            </div>
          }
        />
        <Route path="/gantt" element={<GanttChartPage />} />
      </Routes>
    </Router>
  );
}

export default AppMain;