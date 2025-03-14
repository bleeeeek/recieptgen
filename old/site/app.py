from flask import Flask, render_template, jsonify, request
from datetime import datetime, timedelta
import pandas as pd
import threading
import time
import os
from zk import ZK, const
from dotenv import load_dotenv
import statistics

app = Flask(__name__)

# Load environment variables
load_dotenv()

# ZKTeco Device Configuration
DEVICE_IP = os.getenv('DEVICE_IP')
DEVICE_PORT = int(os.getenv('DEVICE_PORT', 4370))

# Global variable to store attendance data
attendance_data = {}
last_update = None

def get_status_emoji(duration_hours):
    if duration_hours is None:
        return "❓"  # Unknown/No checkout
    elif duration_hours < 6:
        return "😢"  # Sad - worked less
    elif duration_hours > 10:
        return "😫"  # Tired - worked too much
    elif 7.5 <= duration_hours <= 8.5:
        return "😊"  # Happy - perfect duration
    else:
        return "😐"  # Normal - acceptable duration

def get_overall_status(avg_duration):
    """Get overall status emoji based on average duration"""
    return get_status_emoji(avg_duration)

def fetch_attendance():
    """Connect to device and fetch attendance data"""
    global attendance_data, last_update
    
    while True:
        try:
            zk = ZK(DEVICE_IP, port=DEVICE_PORT, timeout=5)
            conn = zk.connect()
            
            if conn:
                # Get attendance
                records = conn.get_attendance()
                today = datetime.now().date()
                
                # Process records
                processed_data = {}
                for record in records:
                    date_str = record.timestamp.strftime('%Y-%m-%d')
                    # Skip future dates
                    if datetime.strptime(date_str, '%Y-%m-%d').date() > today:
                        continue
                        
                    emp_id = str(record.user_id)
                    
                    if date_str not in processed_data:
                        processed_data[date_str] = {}
                    
                    if emp_id not in processed_data[date_str]:
                        processed_data[date_str][emp_id] = []
                    
                    processed_data[date_str][emp_id].append({
                        'timestamp': record.timestamp,
                        'status': record.status,
                        'punch': record.punch if hasattr(record, 'punch') else None
                    })
                
                # Sort and process each employee's records for each date
                final_data = {}
                for date_str in processed_data:
                    final_data[date_str] = {}
                    for emp_id, records in processed_data[date_str].items():
                        records = sorted(records, key=lambda x: x['timestamp'])
                        if records:
                            latest = records[-1]
                            first = records[0]
                            duration = None
                            if len(records) > 1:
                                duration = (latest['timestamp'] - first['timestamp']).total_seconds() / 3600
                            
                            final_data[date_str][emp_id] = {
                                'employee_id': emp_id,
                                'date': datetime.strptime(date_str, '%Y-%m-%d').date(),
                                'first_punch': first['timestamp'],
                                'last_punch': latest['timestamp'],
                                'duration_hours': round(duration, 2) if duration else None,
                                'status_emoji': get_status_emoji(duration),
                                'total_punches': len(records)
                            }
                
                attendance_data = final_data
                last_update = datetime.now()
                conn.disconnect()
                
            time.sleep(60)  # Update every minute
            
        except Exception as e:
            print(f"Error fetching attendance: {e}")
            time.sleep(30)  # Wait 30 seconds before retrying

def get_available_dates():
    """Get list of available dates in the attendance data"""
    today = datetime.now().date()
    # Get unique dates and filter out future dates
    dates = sorted(set(attendance_data.keys()), reverse=True)
    dates = [date for date in dates if datetime.strptime(date, '%Y-%m-%d').date() <= today]
    
    # Move today's date to the top if it exists
    today_str = today.strftime('%Y-%m-%d')
    if today_str in dates:
        dates.remove(today_str)
        dates.insert(0, today_str)
    
    return dates

def get_available_employees():
    """Get list of unique employee IDs"""
    employees = set()
    for date_data in attendance_data.values():
        employees.update(date_data.keys())
    return sorted(list(employees))

@app.route('/')
def index():
    selected_date = request.args.get('date', None)
    selected_employee = request.args.get('employee', 'all')
    dates = get_available_dates()
    employees = get_available_employees()
    
    # If an employee is selected, force date to 'all'
    if selected_employee != 'all':
        selected_date = 'all'
    
    if selected_date == 'all':
        # Flatten the data for all dates
        flattened_data = []
        for date_str in dates:
            for emp_id, record in attendance_data[date_str].items():
                if selected_employee == 'all' or emp_id == selected_employee:
                    flattened_data.append(record)
        display_data = flattened_data
    elif selected_date and selected_date in attendance_data:
        # Convert dict to list for the selected date
        display_data = [
            record for emp_id, record in attendance_data[selected_date].items()
            if selected_employee == 'all' or emp_id == selected_employee
        ]
    elif dates:
        # Default to most recent date
        display_data = [
            record for emp_id, record in attendance_data[dates[0]].items()
            if selected_employee == 'all' or emp_id == selected_employee
        ]
        selected_date = dates[0]
    else:
        display_data = []
        selected_date = None
    
    # Sort the data and remove the first row
    sorted_data = sorted(display_data, key=lambda x: (x['date'], x['first_punch']), reverse=True)
    if sorted_data:
        sorted_data = sorted_data[1:]  # Remove the first row
    
    return render_template('index.html', 
                         attendance=sorted_data,
                         dates=dates,
                         employees=employees,
                         selected_date=selected_date,
                         selected_employee=selected_employee,
                         last_update=last_update)

@app.route('/api/analytics/<employee_id>')
def get_employee_analytics(employee_id):
    """Get analytics data for a specific employee"""
    employee_data = []
    dates = []
    durations = []
    punches = []
    
    # Collect all records for the employee
    for date_str in sorted(attendance_data.keys()):
        if employee_id in attendance_data[date_str]:
            record = attendance_data[date_str][employee_id]
            employee_data.append(record)
            dates.append(date_str)
            durations.append(record['duration_hours'] if record['duration_hours'] else 0)
            punches.append(record['total_punches'])
    
    # Calculate analytics
    avg_duration = statistics.mean(durations) if durations else 0
    avg_punches = statistics.mean(punches) if punches else 0
    
    return jsonify({
        'dates': dates,
        'durations': durations,
        'punches': punches,
        'average_duration': avg_duration,
        'average_punches': avg_punches,
        'overall_status': get_overall_status(avg_duration),
        'total_days': len(dates)
    })

@app.route('/api/attendance')
def get_attendance():
    return jsonify({
        'attendance': attendance_data,
        'last_update': last_update.isoformat() if last_update else None
    })

if __name__ == '__main__':
    # Start the background thread for fetching attendance
    fetch_thread = threading.Thread(target=fetch_attendance, daemon=True)
    fetch_thread.start()
    
    # Run the Flask app
    app.run(debug=True, port=5000) 