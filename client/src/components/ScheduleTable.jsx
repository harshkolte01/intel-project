import React, { useMemo } from 'react';
import { useTable, useFilters } from 'react-table';

function ScheduleTable({ schedule, machines }) {
  const data = useMemo(
    () =>
      schedule.map(task => ({
        job_id: task.job_id,
        machine_name: machines.find(m => m.id.toString() === task.machine_id)?.name || task.machine_id,
        start_time: new Date(task.start_time).toLocaleString(),
        end_time: new Date(task.end_time).toLocaleString(),
        duration: ((new Date(task.end_time) - new Date(task.start_time)) / 1000 / 60).toFixed(2),
      })),
    [schedule, machines]
  );

  const columns = useMemo(
    () => [
      {
        Header: 'Job ID',
        accessor: 'job_id',
        Filter: ({ column }) => SelectFilter({ column, options: [...new Set(schedule.map(task => task.job_id))].sort() }),
        filter: 'equals',
      },
      {
        Header: 'Machine',
        accessor: 'machine_name',
        Filter: ({ column }) => SelectFilter({ column, options: [...new Set(machines.map(m => m.name))].sort() }),
        filter: 'equals',
      },
      {
        Header: 'Start Time',
        accessor: 'start_time',
        Filter: ({ column }) => SelectFilter({ column, options: [...new Set(data.map(row => row.start_time))].sort() }),
        filter: 'equals',
      },
      {
        Header: 'End Time',
        accessor: 'end_time',
        Filter: ({ column }) => SelectFilter({ column, options: [...new Set(data.map(row => row.end_time))].sort() }),
        filter: 'equals',
      },
      {
        Header: 'Duration (min)',
        accessor: 'duration',
        Filter: ({ column }) => SelectFilter({ column, options: [...new Set(data.map(row => row.duration))].sort((a, b) => a - b) }),
        filter: 'equals',
      },
    ],
    [schedule, machines, data]
  );

  const {
    getTableProps,
    getTableBodyProps,
    headerGroups,
    rows,
    prepareRow,
  } = useTable({ columns, data }, useFilters);

  return (
    <div className="schedule-table">
      <h2>Schedule Table</h2>
      <table {...getTableProps()}>
        <thead>
          {headerGroups.map(headerGroup => (
            <tr {...headerGroup.getHeaderGroupProps()}>
              {headerGroup.headers.map(column => (
                <th {...column.getHeaderProps()}>
                  {column.render('Header')}
                  <div>{column.canFilter ? column.render('Filter') : null}</div>
                </th>
              ))}
            </tr>
          ))}
        </thead>
        <tbody {...getTableBodyProps()}>
          {rows.map(row => {
            prepareRow(row);
            return (
              <tr {...row.getRowProps()}>
                {row.cells.map(cell => (
                  <td {...cell.getCellProps()}>{cell.render('Cell')}</td>
                ))}
              </tr>
            );
          })}
        </tbody>
      </table>
    </div>
  );
}

// Dropdown filter component
function SelectFilter({ column: { filterValue, setFilter }, options }) {
  return (
    <select
      value={filterValue || ''}
      onChange={e => setFilter(e.target.value || undefined)}
      className="table-filter-select"
    >
      <option value="">All</option>
      {options.map(option => (
        <option key={option} value={option}>{option}</option>
      ))}
    </select>
  );
}

export default ScheduleTable;