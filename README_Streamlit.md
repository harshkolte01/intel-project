# Smart Scheduling System - Streamlit Version

This is a Streamlit-based version of the Smart Scheduling System that combines both frontend and backend functionality into a single deployable application.

## Features

- **Dashboard**: Overview of machines, jobs, and scheduling statistics
- **Machine Management**: Add and manage production machines with status and priority
- **Job Management**: Create jobs with multiple operations and durations
- **Gantt Chart**: Visual representation of the production schedule
- **Schedule Table**: Detailed view of scheduled tasks
- **Genetic Algorithm**: Optimized scheduling using Google OR-Tools

## Installation

1. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the application:**
   ```bash
   streamlit run streamlit_app.py
   ```

## Deployment on Streamlit Cloud

1. **Push your code to GitHub:**
   ```bash
   git add .
   git commit -m "Add Streamlit version"
   git push origin main
   ```

2. **Deploy on Streamlit Cloud:**
   - Go to [share.streamlit.io](https://share.streamlit.io)
   - Connect your GitHub account
   - Select your repository
   - Set the main file path to: `streamlit_app.py`
   - Click "Deploy"

## Local Development

1. **Clone the repository:**
   ```bash
   git clone <your-repo-url>
   cd intel-project
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application:**
   ```bash
   streamlit run streamlit_app.py
   ```

4. **Open your browser:**
   Navigate to `http://localhost:8501`

## Usage

1. **Add Machines**: Go to "Add Machine" page and create production machines
2. **Add Jobs**: Go to "Add Job" page and create jobs with operations
3. **Generate Schedule**: Go to Dashboard and click "Generate New Schedule"
4. **View Results**: Check the Gantt Chart and Schedule Table pages

## Database

The application uses SQLite for data storage. The database file (`scheduling.db`) will be created automatically when you first run the application.

## Key Differences from Original

- **Single Application**: Combines React frontend and FastAPI backend into one Streamlit app
- **SQLite Database**: Uses SQLite instead of PostgreSQL for simplicity
- **Plotly Gantt Charts**: Uses Plotly for interactive Gantt charts
- **Streamlit UI**: Modern, responsive interface with sidebar navigation
- **Session State**: Maintains data across page navigation

## Requirements

- Python 3.8+
- Streamlit
- Pandas
- Plotly
- OR-Tools (Google's optimization library)

## Troubleshooting

- **Port already in use**: Change the port with `streamlit run streamlit_app.py --server.port 8502`
- **Database issues**: Delete `scheduling.db` to reset the database
- **Dependency issues**: Update pip and reinstall requirements

## License

This project is part of the Intel Project for smart manufacturing scheduling. 