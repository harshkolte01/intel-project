import React from 'react';
import { Chart } from 'react-chartjs-2';
import 'chart.js/auto';
import { Chart as ChartJS, TimeScale, LinearScale, CategoryScale, BarElement, Title, Tooltip, Legend } from 'chart.js';
import 'chartjs-adapter-date-fns';
import zoomPlugin from 'chartjs-plugin-zoom';

// Register required components
ChartJS.register(TimeScale, LinearScale, CategoryScale, BarElement, Title, Tooltip, Legend, zoomPlugin);

function GanttChartComponent({ schedule, machines }) {
  console.log('Schedule Data:', schedule);
  console.log('Machines Data:', machines);

  if (!schedule || !schedule.length || !machines || !machines.length) {
    return <div>No schedule data available</div>;
  }

  // Extract unique machine IDs from filtered schedule
  const machineIds = [...new Set(schedule.map(task => task.machine_id))];

  const data = {
    datasets: schedule.reduce((acc, task, index) => {
      const dataset = acc.find(ds => ds.label === `Job ${task.job_id}`);
      if (dataset) {
        dataset.data.push({
          x: new Date(task.start_time),
          y: task.machine_id,
          duration: (new Date(task.end_time) - new Date(task.start_time)) / 1000 / 60,
        });
      } else {
        acc.push({
          label: `Job ${task.job_id}`,
          data: [{
            x: new Date(task.start_time),
            y: task.machine_id,
            duration: (new Date(task.end_time) - new Date(task.start_time)) / 1000 / 60,
          }],
          backgroundColor: `hsl(${index * 60}, 70%, 50%)`,
          barThickness: Math.max(10, 40 / machineIds.length), // Dynamic thickness
        });
      }
      return acc;
    }, []),
  };

  console.log('Chart Data:', data);

  const options = {
    indexAxis: 'y',
    scales: {
      x: {
        type: 'time',
        time: {
          unit: 'minute',
          displayFormats: {
            minute: 'HH:mm',
          },
        },
        title: {
          display: true,
          text: 'Time',
        },
        min: new Date(Math.min(...schedule.map(task => new Date(task.start_time)))).toISOString(),
        max: new Date(Math.max(...schedule.map(task => new Date(task.end_time)))).toISOString(),
        ticks: {
          autoSkip: true,
          maxTicksLimit: 10,
        },
      },
      y: {
        type: 'category',
        labels: machineIds, // Use machine numbers (IDs) only
        title: {
          display: true,
          text: 'Machine',
        },
      },
    },
    plugins: {
      legend: {
        display: true,
        position: 'top',
      },
      tooltip: {
        callbacks: {
          label: (context) => {
            const dataPoint = context.dataset.data[context.dataIndex];
            return `Job ${context.dataset.label}: ${dataPoint.duration} minutes`;
          },
        },
      },
      zoom: {
        pan: {
          enabled: true,
          mode: 'x',
        },
        zoom: {
          wheel: { enabled: true },
          pinch: { enabled: true },
          mode: 'x',
        },
        limits: {
          x: { min: 'original', max: 'original' },
        },
      },
    },
    elements: {
      bar: {
        borderWidth: 1,
        borderColor: '#000',
      },
    },
    responsive: true,
    maintainAspectRatio: false,
  };

  return (
    <div className="gantt-chart" style={{ height: '400px' }}>
      <h2>Gantt Chart</h2>
      <Chart type="bar" data={data} options={options} />
    </div>
  );
}

export default GanttChartComponent;