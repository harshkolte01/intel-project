from ortools.sat.python import cp_model
from datetime import datetime, timedelta

def generate_schedule(jobs, machines):
    print(f"Generating schedule with {len(jobs)} jobs and {len(machines)} machines")
    if not jobs or not machines:
        print("No jobs or machines provided")
        return []

    try:
        model = cp_model.CpModel()
        # Calculate horizon (max possible time)
        horizon = sum(int(op["duration"]) for job in jobs for op in job.operations)
        tasks = []
        machine_tasks = {m.id: [] for m in machines}

        # Create variables for each task
        for job in jobs:
            for op_idx, op in enumerate(job.operations):
                machine_id = int(op["machine_id"])
                if machine_id not in machine_tasks:
                    print(f"Invalid machine_id {machine_id} for job {job.job_id}")
                    continue
                duration = int(op["duration"])
                if duration <= 0:
                    print(f"Invalid duration {duration} for job {job.job_id}")
                    continue

                start_var = model.NewIntVar(0, horizon, f'start_{job.job_id}_{op_idx}')
                end_var = model.NewIntVar(0, horizon, f'end_{job.job_id}_{op_idx}')
                interval_var = model.NewIntervalVar(
                    start_var, duration, end_var, f'interval_{job.job_id}_{op_idx}'
                )
                tasks.append((start_var, end_var, interval_var, job.job_id, machine_id))

                # Assign task to machine
                machine_tasks[machine_id].append(interval_var)

                # Precedence: Operation i+1 starts after operation i
                if op_idx > 0:
                    prev_end = tasks[-2][1]
                    model.Add(start_var >= prev_end)

        # Machine exclusivity: No overlapping tasks on the same machine
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
        solver.parameters.max_time_in_seconds = 10.0  # Limit solve time
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
            print(f"Generated schedule with {len(schedule)} tasks, makespan: {solver.Value(makespan)} minutes")
            return schedule
        else:
            print("No feasible schedule found")
            return []
    except Exception as e:
        print(f"Error generating schedule: {e}")
        return []