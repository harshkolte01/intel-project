import pandas as pd
import json
from datetime import datetime

# Sample machines data
machines_data = {
    'name': [
        'CNC Machine 1', 'CNC Machine 2', 'Welding Station 1', 'Assembly Line A',
        'Assembly Line B', 'Quality Control Station', 'Packaging Machine 1',
        'Packaging Machine 2', 'Drilling Machine', 'Cutting Machine',
        'Painting Booth', 'Testing Station'
    ],
    'status': [
        'available', 'available', 'maintenance', 'available',
        'offline', 'available', 'available', 'available',
        'maintenance', 'available', 'available', 'available'
    ],
    'priority': [1, 1, 2, 3, 2, 1, 3, 3, 2, 1, 2, 1]
}

# Sample jobs data with realistic operations
jobs_data = {
    'job_id': [
        'PRODUCT_A_001', 'PRODUCT_B_002', 'PRODUCT_C_003', 'PRODUCT_D_004',
        'PRODUCT_E_005', 'PRODUCT_F_006', 'PRODUCT_G_007', 'PRODUCT_H_008',
        'PRODUCT_I_009', 'PRODUCT_J_010'
    ],
    'operations': [
        '[{"machine_id": "1", "duration": "45"}, {"machine_id": "3", "duration": "30"}, {"machine_id": "4", "duration": "60"}, {"machine_id": "6", "duration": "15"}, {"machine_id": "7", "duration": "20"}]',
        '[{"machine_id": "2", "duration": "40"}, {"machine_id": "10", "duration": "25"}, {"machine_id": "5", "duration": "50"}, {"machine_id": "6", "duration": "15"}, {"machine_id": "8", "duration": "18"}]',
        '[{"machine_id": "1", "duration": "35"}, {"machine_id": "9", "duration": "20"}, {"machine_id": "11", "duration": "30"}, {"machine_id": "12", "duration": "10"}]',
        '[{"machine_id": "2", "duration": "50"}, {"machine_id": "3", "duration": "35"}, {"machine_id": "4", "duration": "45"}, {"machine_id": "6", "duration": "20"}, {"machine_id": "7", "duration": "25"}]',
        '[{"machine_id": "10", "duration": "30"}, {"machine_id": "11", "duration": "25"}, {"machine_id": "12", "duration": "15"}]',
        '[{"machine_id": "1", "duration": "55"}, {"machine_id": "9", "duration": "30"}, {"machine_id": "4", "duration": "40"}, {"machine_id": "6", "duration": "20"}, {"machine_id": "8", "duration": "22"}]',
        '[{"machine_id": "2", "duration": "40"}, {"machine_id": "3", "duration": "25"}, {"machine_id": "5", "duration": "35"}, {"machine_id": "6", "duration": "15"}]',
        '[{"machine_id": "1", "duration": "30"}, {"machine_id": "10", "duration": "20"}, {"machine_id": "11", "duration": "15"}, {"machine_id": "12", "duration": "10"}, {"machine_id": "7", "duration": "18"}]',
        '[{"machine_id": "2", "duration": "45"}, {"machine_id": "9", "duration": "25"}, {"machine_id": "4", "duration": "50"}, {"machine_id": "6", "duration": "20"}]',
        '[{"machine_id": "1", "duration": "35"}, {"machine_id": "3", "duration": "30"}, {"machine_id": "5", "duration": "40"}, {"machine_id": "6", "duration": "15"}, {"machine_id": "8", "duration": "20"}]'
    ]
}

# Create detailed operations breakdown
detailed_operations = []
for job in jobs_data['job_id']:
    job_ops = json.loads(jobs_data['operations'][jobs_data['job_id'].index(job)])
    for i, op in enumerate(job_ops):
        detailed_operations.append({
            'job_id': job,
            'operation_number': i + 1,
            'machine_id': op['machine_id'],
            'machine_name': machines_data['name'][int(op['machine_id']) - 1],
            'duration_minutes': int(op['duration']),
            'estimated_cost': int(op['duration']) * 10,  # $10 per minute
            'priority': 'High' if int(op['duration']) > 40 else 'Medium' if int(op['duration']) > 20 else 'Low'
        })

# Create machine utilization data
machine_utilization = []
for i, machine in enumerate(machines_data['name']):
    machine_utilization.append({
        'machine_id': i + 1,
        'machine_name': machine,
        'status': machines_data['status'][i],
        'priority': machines_data['priority'][i],
        'total_operations': sum(1 for op in detailed_operations if int(op['machine_id']) == i + 1),
        'total_duration': sum(op['duration_minutes'] for op in detailed_operations if int(op['machine_id']) == i + 1),
        'utilization_rate': round(sum(op['duration_minutes'] for op in detailed_operations if int(op['machine_id']) == i + 1) / 480 * 100, 2)  # 8-hour day
    })

# Create DataFrames
machines_df = pd.DataFrame(machines_data)
jobs_df = pd.DataFrame(jobs_data)
operations_df = pd.DataFrame(detailed_operations)
utilization_df = pd.DataFrame(machine_utilization)

# Create Excel file with multiple sheets
with pd.ExcelWriter('sample_scheduling_data.xlsx', engine='openpyxl') as writer:
    machines_df.to_excel(writer, sheet_name='Machines', index=False)
    jobs_df.to_excel(writer, sheet_name='Jobs', index=False)
    operations_df.to_excel(writer, sheet_name='Detailed_Operations', index=False)
    utilization_df.to_excel(writer, sheet_name='Machine_Utilization', index=False)
    
    # Add summary sheet
    summary_data = {
        'Metric': [
            'Total Machines',
            'Available Machines',
            'Maintenance Machines',
            'Offline Machines',
            'Total Jobs',
            'Total Operations',
            'Average Operations per Job',
            'Total Estimated Duration (hours)',
            'Average Job Duration (minutes)'
        ],
        'Value': [
            len(machines_data['name']),
            sum(1 for status in machines_data['status'] if status == 'available'),
            sum(1 for status in machines_data['status'] if status == 'maintenance'),
            sum(1 for status in machines_data['status'] if status == 'offline'),
            len(jobs_data['job_id']),
            len(detailed_operations),
            round(len(detailed_operations) / len(jobs_data['job_id']), 2),
            round(sum(op['duration_minutes'] for op in detailed_operations) / 60, 2),
            round(sum(op['duration_minutes'] for op in detailed_operations) / len(jobs_data['job_id']), 2)
        ]
    }
    summary_df = pd.DataFrame(summary_data)
    summary_df.to_excel(writer, sheet_name='Summary', index=False)

print("✅ Excel file 'sample_scheduling_data.xlsx' created successfully!")
print("📊 Contains 5 sheets:")
print("   - Machines: Machine information")
print("   - Jobs: Job definitions with operations")
print("   - Detailed_Operations: Breakdown of each operation")
print("   - Machine_Utilization: Machine usage statistics")
print("   - Summary: Overall system statistics") 