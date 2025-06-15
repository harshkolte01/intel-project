# Smart Scheduling System for Small Machine Shops

A web-based application designed to optimize job-shop scheduling for small and medium enterprises (SMEs) in industrial clusters like Rajkot and Dongguan. The system uses AI-based scheduling (Google OR-Tools) to improve machine utilization by approximately 10%, reduce job delays, and handle dynamic workloads with an intuitive interface.

## Table of Contents
- [Overview](#overview)
- [Features](#features)
- [Screenshots](#screenshots)
- [Prerequisites](#prerequisites)
- [Setup](#setup)
  - [Using Docker](#using-docker)
  - [Local Development](#local-development)
- [Usage](#usage)
  - [Adding Machines and Jobs](#adding-machines-and-jobs)
  - [Viewing the Schedule](#viewing-the-schedule)
  - [Filtering Data](#filtering-data)
- [Project Structure](#project-structure)
- [Dependencies](#dependencies)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [License](#license)

## Overview

The Smart Scheduling System addresses inefficient job scheduling in SMEs by providing an AI-driven solution to allocate tasks to machines, minimizing idle time and makespan. Built with a React frontend, FastAPI backend, and PostgreSQL database, it offers a user-friendly interface for shop floor workers and managers to manage jobs and machines, visualize schedules via a Gantt chart, and filter data in a table format.

**Project Details**:
- **Organisation**: General
- **Problem Category**: General problem
- **Description**: Inefficient job scheduling affects SME productivity. This system optimizes task allocation, targeting a ~10% machine utilization increase in industrial clusters.
- **Group ID**: G00091

## Features

- **AI-Based Scheduling**: Uses Google OR-Tools to generate conflict-free schedules, ensuring no overlapping tasks on machines and sequential job operations.
- **Job and Machine Management**: Add, view, and manage jobs (with multiple operations) and machines (with status and priority) via intuitive forms.
- **Gantt Chart Visualization**: Dynamic, zoomable Gantt chart displaying job schedules, auto-scaled to fit the time range.
- **Schedule Table**: Filterable table on the Gantt chart page with dropdowns for Job ID, Machine, Start Time, End Time, and Duration.
- **Machine Status Table**: Displays machine details (Name, Status, Priority, Availability) in a tabular format.
- **Filtering**: Filter schedules by machine status (All, Available, Maintenance, Offline) and priority (All, High, Medium, Low) on the Gantt chart page.
- **Responsive UI**: Modern, mobile-friendly design with a blue/gray/white theme, shadows, and hover effects.
- **Separate Chart Page**: Dedicated `/gantt` page for focused schedule visualization and filtering.
- **Docker Support**: Easy deployment with Docker Compose.

## Screenshots

Below are screenshots showcasing the application’s interface:

![Dashboard](images/img1.png)
*Dashboard with machine/job forms, Gantt chart, and machine status table.*

![Gantt Chart Page](images/img2.png)
*Gantt chart page with schedule table and status/priority filters.*

![Filtered Schedule](images/img3.png)
*Filtered schedule showing specific jobs in the Gantt chart and table.*

## Prerequisites

- **Docker** and **Docker Compose** (for containerized deployment)
- **Node.js** v18+ (for local frontend development)
- **Python** 3.9+ (for local backend development)
- **PostgreSQL** (for local database, if not using Docker)
- Git (to clone the repository)

## Setup

### Using Docker

1. **Clone the Repository**:
   ```bash
   git clone <repository-url>
   cd smart-scheduling-system
   ```

2. **Start the Application**:
   ```bash
   docker-compose up --build
   ```

3. **Access the Application**:
   - **Frontend**: `http://localhost:3000`
   - **Backend API Docs**: `http://localhost:8000/docs`

### Local Development

#### Backend
1. Navigate to the server directory:
   ```bash
   cd server
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements_list.txt
   ```

4. Set up PostgreSQL:
   - Create a database named `scheduling_db`.
   - Update `server/app/database_config.py` with your database credentials:
     ```python
     SQLALCHEMY_DATABASE_URL = "postgresql://user:password@localhost:5432/scheduling_db"
     ```

5. Run the backend:
   ```bash
   uvicorn app.main_app:app --reload
   ```

#### Frontend
1. Navigate to the client directory:
   ```bash
   cd client
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Start the frontend:
   ```bash
   npm start
   ```

#### Database
- Ensure PostgreSQL is running and `scheduling_db` is created.
- The backend automatically initializes tables and sample data (2 machines, 3 jobs) on startup.

## Usage

### Adding Machines and Jobs
1. **Add a Machine**:
   - On the dashboard (`/`), use the “Add New Machine” form.
   - Enter a name (e.g., `Machine3`), select status (Available, Maintenance, Offline), and priority (High: 1, Medium: 2, Low: 3).
   - Click “Submit Machine” to add it to the database.

2. **Add a Job**:
   - Use the “Add New Job” form.
   - Enter a Job ID (e.g., `JOB004`), select a machine (e.g., Machine1), and specify duration (e.g., 40 minutes).
   - Click “Add Operation” for additional operations (sequential tasks).
   - Click “Submit Job” to schedule it.

### Viewing the Schedule
- **Dashboard (`/`)**:
  - View the Gantt chart showing all job operations (e.g., JOB001, JOB002, JOB003).
  - Check the machine status table for details (Name, Status, Priority, Availability).
  - Click “View Gantt Chart in New Page” to go to `/gantt`.

- **Gantt Chart Page (`/gantt`)**:
  - Displays a Gantt chart and a schedule table side-by-side.
  - Gantt chart: Zoom (scroll wheel) and pan (click-drag) to explore.
  - Schedule table: Shows Job ID, Machine, Start Time, End Time, Duration with dropdown filters.

### Filtering Data
- **Status/Priority Filters** (on `/gantt`):
  - Select “Available” to show jobs on available machines (e.g., Machine1).
  - Select “High (1)” to show jobs on priority 1 machines.
  - Combine filters (e.g., “Available” + “High (1)”).

- **Schedule Table Filters** (on `/gantt`):
  - Use dropdowns to filter:
    - Job ID: Select “JOB001” to show its tasks.
    - Machine: Select “Machine1” to show tasks on Machine1.
    - Duration: Select “30.00” to show 30-minute tasks.
  - Filters sync with the Gantt chart.

## Project Structure

```
smart-scheduling-system/
├── client/
│   ├── public/
│   │   ├── index.html
│   ├── src/
│   │   ├── components/
│   │   │   ├── GanttChartComponent.jsx
│   │   │   ├── GanttChartPage.jsx
│   │   │   ├── JobFormComponent.jsx
│   │   │   ├── MachineFormComponent.jsx
│   │   │   ├── MachineStatusComponent.jsx
│   │   │   ├── ScheduleTable.jsx
│   │   ├── AppMain.jsx
│   │   ├── index.js
│   │   ├── styles_main.css
│   ├── package.json
├── server/
│   ├── app/
│   │   ├── models/
│   │   │   ├── job_model.py
│   │   │   ├── machine_model.py
│   │   ├── routers/
│   │   │   ├── jobs_router.py
│   │   │   ├── machines_router.py
│   │   │   ├── schedule_router.py
│   │   ├── utils/
│   │   │   ├── genetic_algo.py
│   │   ├── database_config.py
│   │   ├── main_app.py
│   ├── requirements_list.txt
├── images/
│   ├── img1.png
│   ├── img2.png
│   ├── img3.png
├── docker_compose_config.yml
├── README_guide.md
```

## Dependencies

### Backend
- Python 3.9+
- FastAPI==0.115.0
- Uvicorn==0.30.6
- SQLAlchemy==2.0.35
- Psycopg2-binary==2.9.9
- Python-dateutil==2.9.0
- OR-Tools==9.10.4067

### Frontend
- Node.js v18+
- React==18.2.0
- Axios==1.7.2
- React-chartjs-2==5.2.0
- Chart.js==4.4.3
- Date-fns==2.30.0
- Chartjs-adapter-date-fns==3.0.0
- React-router-dom==6.23.1
- Chartjs-plugin-zoom==2.0.1
- React-table==7.8.0

## Troubleshooting

- **Blank Page**:
  - Check browser console (F12 → Console) for errors.
  - Verify backend is running (`http://localhost:8000/docs`).
  - Ensure `machines` and `jobs` tables have data:
    ```bash
    docker exec -it <db-container-name> psql -U user -d scheduling_db
    SELECT * FROM machines;
    SELECT * FROM jobs;
    ```

- **No Schedule Data**:
  - Check server logs for scheduler errors:
    ```bash
    docker-compose logs server
    ```
  - Test `/schedule` endpoint:
    ```bash
    curl http://localhost:8000/schedule
    ```

- **Styling Issues**:
  - Clear browser cache.
  - Confirm `styles_main.css` is loaded (check DevTools → Network).

- **Dependency Errors**:
  - Reinstall dependencies:
    ```bash
    cd server && pip install -r requirements_list.txt
    cd client && npm install
    ```

## Contributing

Contributions are welcome! To contribute:
1. Fork the repository.
2. Create a feature branch (`git checkout -b feature/new-feature`).
3. Commit changes (`git commit -m "Add new feature"`).
4. Push to the branch (`git push origin feature/new-feature`).
5. Open a pull request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.