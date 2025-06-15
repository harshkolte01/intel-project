import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import axios from 'axios';
import GanttChartComponent from './GanttChartComponent';
import ScheduleTable from './ScheduleTable';

function GanttChartPage() {
  const [schedule, setSchedule] = useState([]);
  const [machines, setMachines] = useState([]);
  const [filteredSchedule, setFilteredSchedule] = useState([]);
  const [error, setError] = useState(null);
  const [statusFilter, setStatusFilter] = useState('All');
  const [priorityFilter, setPriorityFilter] = useState('All');

  useEffect(() => {
    const fetchData = async () => {
      try {
        const baseUrl = process.env.NODE_ENV === 'production' ? 'http://server:8000' : 'http://localhost:8000';
        const [scheduleRes, machinesRes] = await Promise.all([
          axios.get(`${baseUrl}/schedule`),
          axios.get(`${baseUrl}/machines`),
        ]);
        setSchedule(scheduleRes.data || []);
        setFilteredSchedule(scheduleRes.data || []);
        setMachines(machinesRes.data || []);
        setError(null);
      } catch (error) {
        console.error('Error fetching data:', error);
        setError('Failed to load chart data.');
      }
    };
    fetchData();
  }, []);

  useEffect(() => {
    let filtered = schedule;
    if (statusFilter !== 'All') {
      filtered = filtered.filter(task => {
        const machine = machines.find(m => m.id.toString() === task.machine_id);
        return machine && machine.status === statusFilter.toLowerCase();
      });
    }
    if (priorityFilter !== 'All') {
      filtered = filtered.filter(task => {
        const machine = machines.find(m => m.id.toString() === task.machine_id);
        return machine && machine.priority === Number(priorityFilter);
      });
    }
    setFilteredSchedule(filtered);
  }, [statusFilter, priorityFilter, schedule, machines]);

  return (
    <div className="app">
      <h1>Gantt Chart View</h1>
      {error && <p className="error">{error}</p>}
      <div className="filter-controls">
        <label>
          Filter by Status:
          <select value={statusFilter} onChange={(e) => setStatusFilter(e.target.value)}>
            <option value="All">All</option>
            <option value="Available">Available</option>
            <option value="Maintenance">Maintenance</option>
            <option value="Offline">Offline</option>
          </select>
        </label>
        <label>
          Filter by Priority:
          <select value={priorityFilter} onChange={(e) => setPriorityFilter(e.target.value)}>
            <option value="All">All</option>
            <option value="1">High (1)</option>
            <option value="2">Medium (2)</option>
            <option value="3">Low (3)</option>
          </select>
        </label>
      </div>
      <Link to="/" className="back-link">Back to Dashboard</Link>
      <div className="chart-table-container">
        <GanttChartComponent schedule={filteredSchedule} machines={machines} />
        <ScheduleTable schedule={filteredSchedule} machines={machines} />
      </div>
    </div>
  );
}

export default GanttChartPage;