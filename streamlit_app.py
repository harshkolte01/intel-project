import streamlit as st
import pandas as pd
import plotly.figure_factory as ff
import plotly.graph_objects as go
from datetime import datetime, timedelta
import json
import psycopg2
from sqlalchemy import create_engine, text
from ortools.sat.python import cp_model
import uuid
import plotly.colors as pc
import io
import time

# Page configuration
st.set_page_config(
    page_title="Smart Scheduling System",
    page_icon="📊",
    layout="wide"
)

# Database configuration
DATABASE_URL = "postgresql://ashish:ashish@152.53.240.143:5432/scheduling_db"

# Initialize session state
if 'machines' not in st.session_state:
    st.session_state.machines = []
if 'jobs' not in st.session_state:
    st.session_state.jobs = []
if 'schedule' not in st.session_state:
    st.session_state.schedule = []

# Database functions
def get_db_connection():
    """Create database connection"""
    try:
        engine = create_engine(DATABASE_URL)
        return engine
    except Exception as e:
        st.error(f"Database connection error: {e}")
        return None

def init_database():
    """Initialize database tables with loading animation"""
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    try:
        status_text.text("🔄 Connecting to database...")
        progress_bar.progress(20)
        time.sleep(0.5)
        
        engine = get_db_connection()
        if not engine:
            status_text.text("❌ Database connection failed!")
            progress_bar.progress(0)
            return
        
        status_text.text("📋 Creating machines table...")
        progress_bar.progress(40)
        time.sleep(0.5)
        
        with engine.connect() as conn:
            # Create machines table
            conn.execute(text("""
                CREATE TABLE IF NOT EXISTS machines (
                    id SERIAL PRIMARY KEY,
                    name VARCHAR NOT NULL,
                    status VARCHAR DEFAULT 'available',
                    priority INTEGER DEFAULT 1,
                    available_from TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
            """))
            
            status_text.text("📋 Creating jobs table...")
            progress_bar.progress(60)
            time.sleep(0.5)
            
            # Create jobs table
            conn.execute(text("""
                CREATE TABLE IF NOT EXISTS jobs (
                    id SERIAL PRIMARY KEY,
                    job_id VARCHAR UNIQUE NOT NULL,
                    operations JSONB NOT NULL
                );
            """))
            
            status_text.text("💾 Committing changes...")
            progress_bar.progress(80)
            time.sleep(0.5)
            
            conn.commit()
            
            status_text.text("✅ Database initialized successfully!")
            progress_bar.progress(100)
            time.sleep(1)
            
            # Clear the progress indicators
            progress_bar.empty()
            status_text.empty()
            
            st.success("🎉 Database initialized successfully!")
            
    except Exception as e:
        status_text.text("❌ Database initialization failed!")
        progress_bar.progress(0)
        st.error(f"Database initialization error: {e}")

def load_data():
    """Load data from database"""
    engine = get_db_connection()
    if not engine:
        return
    
    try:
        # Load machines
        machines_df = pd.read_sql_query("SELECT * FROM machines", engine)
        st.session_state.machines = machines_df.to_dict('records')
        
        # Load jobs
        jobs_df = pd.read_sql_query("SELECT * FROM jobs", engine)
        st.session_state.jobs = jobs_df.to_dict('records')
        
    except Exception as e:
        st.error(f"Error loading data: {e}")

def save_machine(machine_data):
    """Save machine to database"""
    engine = get_db_connection()
    if not engine:
        return
    
    try:
        with engine.connect() as conn:
            conn.execute(text("""
                INSERT INTO machines (name, status, priority, available_from)
                VALUES (:name, :status, :priority, :available_from)
            """), {
                'name': machine_data['name'],
                'status': machine_data['status'],
                'priority': machine_data['priority'],
                'available_from': datetime.now()
            })
            conn.commit()
            load_data()
            st.success(f"Machine '{machine_data['name']}' saved successfully!")
    except Exception as e:
        st.error(f"Error saving machine: {e}")

def save_job(job_data):
    """Save job to database"""
    engine = get_db_connection()
    if not engine:
        return
    
    try:
        with engine.connect() as conn:
            conn.execute(text("""
                INSERT INTO jobs (job_id, operations)
                VALUES (:job_id, :operations)
            """), {
                'job_id': job_data['job_id'],
                'operations': json.dumps(job_data['operations'])
            })
            conn.commit()
            load_data()
            st.success(f"Job '{job_data['job_id']}' saved successfully!")
    except Exception as e:
        st.error(f"Error saving job: {e}")

def upload_machines_from_csv(uploaded_file):
    """Upload machines from CSV file with loading animation"""
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    try:
        status_text.text("📖 Reading CSV file...")
        progress_bar.progress(20)
        time.sleep(0.3)
        
        df = pd.read_csv(uploaded_file)
        required_columns = ['name', 'status', 'priority']
        
        if not all(col in df.columns for col in required_columns):
            st.error(f"CSV must contain columns: {required_columns}")
            progress_bar.empty()
            status_text.empty()
            return
        
        status_text.text("🔍 Validating data...")
        progress_bar.progress(40)
        time.sleep(0.3)
        
        total_rows = len(df)
        success_count = 0
        
        status_text.text("💾 Uploading machines to database...")
        progress_bar.progress(60)
        
        for idx, row in df.iterrows():
            try:
                machine_data = {
                    'name': row['name'],
                    'status': row['status'].lower(),
                    'priority': int(row['priority'])
                }
                
                # Save to database
                engine = get_db_connection()
                if engine:
                    with engine.connect() as conn:
                        conn.execute(text("""
                            INSERT INTO machines (name, status, priority, available_from)
                            VALUES (:name, :status, :priority, :available_from)
                        """), {
                            'name': machine_data['name'],
                            'status': machine_data['status'],
                            'priority': machine_data['priority'],
                            'available_from': datetime.now()
                        })
                        conn.commit()
                        success_count += 1
                
                # Update progress
                progress = 60 + (idx + 1) / total_rows * 30
                progress_bar.progress(int(progress))
                
            except Exception as e:
                st.warning(f"Error uploading machine '{row['name']}': {e}")
                continue
        
        status_text.text("🔄 Refreshing data...")
        progress_bar.progress(90)
        time.sleep(0.3)
        
        load_data()
        
        status_text.text("✅ Upload completed!")
        progress_bar.progress(100)
        time.sleep(1)
        
        # Clear the progress indicators
        progress_bar.empty()
        status_text.empty()
        
        st.success(f"🎉 Successfully uploaded {success_count} machines!")
        
    except Exception as e:
        status_text.text("❌ Upload failed!")
        progress_bar.progress(0)
        st.error(f"Error uploading machines: {e}")

def upload_jobs_from_csv(uploaded_file):
    """Upload jobs from CSV file with loading animation"""
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    try:
        status_text.text("📖 Reading CSV file...")
        progress_bar.progress(20)
        time.sleep(0.3)
        
        df = pd.read_csv(uploaded_file)
        required_columns = ['job_id', 'operations']
        
        if not all(col in df.columns for col in required_columns):
            st.error(f"CSV must contain columns: {required_columns}")
            progress_bar.empty()
            status_text.empty()
            return
        
        status_text.text("🔍 Validating JSON data...")
        progress_bar.progress(40)
        time.sleep(0.3)
        
        total_rows = len(df)
        success_count = 0
        
        status_text.text("💾 Uploading jobs to database...")
        progress_bar.progress(60)
        
        for idx, row in df.iterrows():
            try:
                # Parse operations from JSON string
                operations = json.loads(row['operations'])
                job_data = {
                    'job_id': row['job_id'],
                    'operations': operations
                }
                
                # Save to database
                engine = get_db_connection()
                if engine:
                    with engine.connect() as conn:
                        conn.execute(text("""
                            INSERT INTO jobs (job_id, operations)
                            VALUES (:job_id, :operations)
                        """), {
                            'job_id': job_data['job_id'],
                            'operations': json.dumps(job_data['operations'])
                        })
                        conn.commit()
                        success_count += 1
                
                # Update progress
                progress = 60 + (idx + 1) / total_rows * 30
                progress_bar.progress(int(progress))
                
            except json.JSONDecodeError:
                st.warning(f"Invalid JSON in operations for job {row['job_id']}")
                continue
            except Exception as e:
                st.warning(f"Error uploading job '{row['job_id']}': {e}")
                continue
        
        status_text.text("🔄 Refreshing data...")
        progress_bar.progress(90)
        time.sleep(0.3)
        
        load_data()
        
        status_text.text("✅ Upload completed!")
        progress_bar.progress(100)
        time.sleep(1)
        
        # Clear the progress indicators
        progress_bar.empty()
        status_text.empty()
        
        st.success(f"🎉 Successfully uploaded {success_count} jobs!")
        
    except Exception as e:
        status_text.text("❌ Upload failed!")
        progress_bar.progress(0)
        st.error(f"Error uploading jobs: {e}")

def create_sample_csv_files():
    """Create sample CSV files for download"""
    
    # Sample machines data
    machines_data = {
        'name': ['Machine A', 'Machine B', 'Machine C', 'Machine D'],
        'status': ['available', 'maintenance', 'available', 'offline'],
        'priority': [1, 2, 3, 1]
    }
    machines_df = pd.DataFrame(machines_data)
    
    # Sample jobs data
    jobs_data = {
        'job_id': ['JOB001', 'JOB002', 'JOB003'],
        'operations': [
            '[{"machine_id": "1", "duration": "30"}, {"machine_id": "2", "duration": "20"}]',
            '[{"machine_id": "2", "duration": "15"}, {"machine_id": "1", "duration": "25"}]',
            '[{"machine_id": "1", "duration": "10"}, {"machine_id": "3", "duration": "45"}]'
        ]
    }
    jobs_df = pd.DataFrame(jobs_data)
    
    return machines_df, jobs_df

# Genetic Algorithm for scheduling
def generate_schedule(jobs, machines):
    if not jobs or not machines:
        return []
    
    try:
        model = cp_model.CpModel()
        # Fix: Check if operations is already a list or needs JSON parsing
        horizon = 0
        for job in jobs:
            operations = job['operations']
            if isinstance(operations, str):
                operations = json.loads(operations)
            horizon += sum(int(op["duration"]) for op in operations)
        
        tasks = []
        machine_tasks = {m['id']: [] for m in machines}
        
        # Create variables for each task
        for job in jobs:
            operations = job['operations']
            if isinstance(operations, str):
                operations = json.loads(operations)
            
            for op_idx, op in enumerate(operations):
                machine_id = int(op["machine_id"])
                if machine_id not in machine_tasks:
                    continue
                duration = int(op["duration"])
                if duration <= 0:
                    continue
                
                start_var = model.NewIntVar(0, horizon, f'start_{job["job_id"]}_{op_idx}')
                end_var = model.NewIntVar(0, horizon, f'end_{job["job_id"]}_{op_idx}')
                interval_var = model.NewIntervalVar(
                    start_var, duration, end_var, f'interval_{job["job_id"]}_{op_idx}'
                )
                tasks.append((start_var, end_var, interval_var, job["job_id"], machine_id))
                
                machine_tasks[machine_id].append(interval_var)
                
                # Precedence: Operation i+1 starts after operation i
                if op_idx > 0:
                    prev_end = tasks[-2][1]
                    model.Add(start_var >= prev_end)
        
        # Machine exclusivity
        for machine_id, intervals in machine_tasks.items():
            if intervals:
                model.AddNoOverlap(intervals)
        
        # Minimize makespan
        makespan = model.NewIntVar(0, horizon, 'makespan')
        for _, end_var, _, _, _ in tasks:
            model.Add(makespan >= end_var)
        model.Minimize(makespan)
        
        # Solve
        solver = cp_model.CpSolver()
        solver.parameters.max_time_in_seconds = 10.0
        status = solver.Solve(model)
        
        if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
            schedule = [
                {
                    "job_id": job_id,
                    "machine_id": str(machine_id),
                    "start_time": (datetime.now() + timedelta(minutes=solver.Value(start))).isoformat(),
                    "end_time": (datetime.now() + timedelta(minutes=solver.Value(end))).isoformat(),
                }
                for start, end, _, job_id, machine_id in tasks
            ]
            return schedule
        else:
            return []
    except Exception as e:
        st.error(f"Error generating schedule: {e}")
        return []

# Initialize database and load data
if st.button("Initialize Database"):
    init_database()

load_data()

st.title("🏭 Smart Scheduling System")

# Database status
engine = get_db_connection()
if engine:
    st.sidebar.success("✅ Database Connected")
else:
    st.sidebar.error("❌ Database Connection Failed")

# Sidebar Navigation Buttons
st.sidebar.markdown("---")
dashboard_clicked = st.sidebar.button("📊 Dashboard")
add_machine_clicked = st.sidebar.button("➕ Add Machine")
add_job_clicked = st.sidebar.button("📋 Add Job")
gantt_clicked = st.sidebar.button("📈 Gantt Chart")
schedule_clicked = st.sidebar.button("📋 Schedule Table")
refresh_clicked = st.sidebar.button("🔄 Refresh Data")
st.sidebar.markdown("---")

if refresh_clicked:
    load_data()
    st.sidebar.success("Data refreshed successfully!")

# Navigation logic
if add_machine_clicked:
    page = "Add Machine"
elif add_job_clicked:
    page = "Add Job"
elif gantt_clicked:
    page = "Gantt Chart"
elif schedule_clicked:
    page = "Schedule Table"
else:
    page = "Dashboard"  # Default page

if page == "Dashboard":
    st.header("📊 Dashboard")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📈 Statistics")
        st.metric("Total Machines", len(st.session_state.machines))
        st.metric("Total Jobs", len(st.session_state.jobs))
        st.metric("Scheduled Tasks", len(st.session_state.schedule))
    
    with col2:
        st.subheader("🔄 Generate Schedule")
        if st.button("Generate New Schedule"):
            st.session_state.schedule = generate_schedule(st.session_state.jobs, st.session_state.machines)
            st.success("Schedule generated successfully!")
    
    # Machine Status Table
    st.subheader("🏗️ Machine Status")
    if st.session_state.machines:
        machines_df = pd.DataFrame(st.session_state.machines)
        st.dataframe(machines_df[['name', 'status', 'priority']], use_container_width=True)
    else:
        st.info("No machines available. Add some machines first!")

elif page == "Add Machine":
    st.header("➕ Add New Machine")
    
    # Create tabs for manual entry and file upload
    tab1, tab2 = st.tabs(["📝 Manual Entry", "📁 Upload CSV"])
    
    with tab1:
        with st.form("machine_form"):
            machine_name = st.text_input("Machine Name", placeholder="Enter machine name")
            status = st.selectbox("Status", ["available", "maintenance", "offline"])
            priority = st.selectbox("Priority", [1, 2, 3], format_func=lambda x: {1: "High", 2: "Medium", 3: "Low"}[x])
            
            submitted = st.form_submit_button("Add Machine")
            if submitted and machine_name:
                machine_data = {
                    'name': machine_name,
                    'status': status,
                    'priority': priority
                }
                save_machine(machine_data)
    
    with tab2:
        st.subheader("📥 Upload Machines from CSV")
        
        # Download sample machines CSV
        machines_df, _ = create_sample_csv_files()
        csv_machines = machines_df.to_csv(index=False)
        st.download_button(
            label="📄 Download Sample Machines CSV",
            data=csv_machines,
            file_name="sample_machines.csv",
            mime="text/csv"
        )
        
        uploaded_machines = st.file_uploader(
            "Choose a machines CSV file",
            type=['csv'],
            key="machines_upload"
        )
        
        if uploaded_machines is not None:
            if st.button("Upload Machines"):
                upload_machines_from_csv(uploaded_machines)

elif page == "Add Job":
    st.header("📋 Add New Job")
    
    # Create tabs for manual entry and file upload
    tab1, tab2 = st.tabs(["📝 Manual Entry", "📁 Upload CSV"])
    
    with tab1:
        with st.form("job_form"):
            job_id = st.text_input("Job ID", placeholder="Enter job ID")
            
            st.subheader("Operations")
            operations = []
            
            # Dynamic operations
            num_operations = st.number_input("Number of Operations", min_value=1, max_value=10, value=1)
            
            for i in range(num_operations):
                st.write(f"Operation {i+1}")
                col1, col2 = st.columns(2)
                with col1:
                    machine_id = st.selectbox(
                        f"Machine for Operation {i+1}",
                        options=[m['id'] for m in st.session_state.machines],
                        format_func=lambda x: f"Machine {x}",
                        key=f"machine_{i}"
                    )
                with col2:
                    duration = st.number_input(
                        f"Duration (minutes) for Operation {i+1}",
                        min_value=1,
                        value=30,
                        key=f"duration_{i}"
                    )
                
                operations.append({
                    "machine_id": str(machine_id),
                    "duration": str(duration)
                })
            
            submitted = st.form_submit_button("Add Job")
            if submitted and job_id and operations:
                job_data = {
                    'job_id': job_id,
                    'operations': operations
                }
                save_job(job_data)
    
    with tab2:
        st.subheader("📥 Upload Jobs from CSV")
        
        # Download sample jobs CSV
        _, jobs_df = create_sample_csv_files()
        csv_jobs = jobs_df.to_csv(index=False)
        st.download_button(
            label="📄 Download Sample Jobs CSV",
            data=csv_jobs,
            file_name="sample_jobs.csv",
            mime="text/csv"
        )
        
        uploaded_jobs = st.file_uploader(
            "Choose a jobs CSV file",
            type=['csv'],
            key="jobs_upload"
        )
        
        if uploaded_jobs is not None:
            if st.button("Upload Jobs"):
                upload_jobs_from_csv(uploaded_jobs)

elif page == "Gantt Chart":
    st.header("📊 Gantt Chart")
    
    if not st.session_state.schedule:
        st.warning("No schedule available. Generate a schedule first!")
    else:
        # Create Gantt chart data
        df = []
        unique_jobs = set()
        
        for task in st.session_state.schedule:
            unique_jobs.add(task['job_id'])
            # Convert ISO string to datetime for Plotly
            start_time = datetime.fromisoformat(task['start_time'].replace('Z', '+00:00'))
            end_time = datetime.fromisoformat(task['end_time'].replace('Z', '+00:00'))
            
            df.append(dict(
                Task=f"Machine {task['machine_id']}",
                Start=start_time,
                Finish=end_time,
                Resource=f"Job {task['job_id']}"
            ))
        
        if df:
            # Generate dynamic colors based on number of unique jobs
            num_jobs = len(unique_jobs)
            colors = pc.qualitative.Set3[:num_jobs] if num_jobs <= 12 else pc.qualitative.Set3 + pc.qualitative.Pastel1 + pc.qualitative.Pastel2
            
            fig = ff.create_gantt(df, 
                                colors=colors,
                                index_col='Resource',
                                show_colorbar=True,
                                group_tasks=True,
                                showgrid_x=True,
                                showgrid_y=True)
            
            fig.update_layout(
                title="Production Schedule Gantt Chart",
                xaxis_title="Time",
                yaxis_title="Machine",
                height=400
            )
            
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No tasks to display in Gantt chart")

elif page == "Schedule Table":
    st.header("📋 Schedule Table")
    
    if not st.session_state.schedule:
        st.warning("No schedule available. Generate a schedule first!")
    else:
        # Create schedule table
        schedule_data = []
        for task in st.session_state.schedule:
            start_time = datetime.fromisoformat(task['start_time'].replace('Z', '+00:00'))
            end_time = datetime.fromisoformat(task['end_time'].replace('Z', '+00:00'))
            duration = (end_time - start_time).total_seconds() / 60
            
            schedule_data.append({
                'Job ID': task['job_id'],
                'Machine': f"Machine {task['machine_id']}",
                'Start Time': start_time.strftime('%Y-%m-%d %H:%M'),
                'End Time': end_time.strftime('%Y-%m-%d %H:%M'),
                'Duration (min)': round(duration, 2)
            })
        
        df = pd.DataFrame(schedule_data)
        st.dataframe(df, use_container_width=True)

# Footer
st.markdown("---")
st.markdown("Smart Scheduling System | PostgreSQL Database") 