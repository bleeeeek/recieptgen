import requests
import json
from datetime import datetime
import pandas as pd
from zk import ZK, const
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# ZKTeco Device Configuration
DEVICE_IP = os.getenv('DEVICE_IP')
DEVICE_PORT = int(os.getenv('DEVICE_PORT', 4370))

# Employee ID to filter (as a string)
TARGET_EMPLOYEE_ID = '70'  

def connect_to_device():
    """Connect to ZKTeco device"""
    conn = None
    zk_obj = ZK(DEVICE_IP, port=DEVICE_PORT, timeout=5)
    try:
        conn = zk_obj.connect()
        print("Connection to device successful")
        return conn
    except Exception as e:
        print(f"Error connecting to device: {e}")
        return None

def get_attendance_logs():
    """Get attendance logs from ZKTeco device"""
    conn = connect_to_device()
    if conn:
        try:
            print("Getting attendance logs...")
            attendance = conn.get_attendance()
            print(f"Retrieved {len(attendance)} attendance records")
            
            # Print punch types to understand what values are available
            punch_types = set()
            for record in attendance[:100]:  # Check first 100 records
                if hasattr(record, 'punch'):
                    punch_types.add(record.punch)
            
            print(f"Punch types found in data: {punch_types}")
            
            return attendance
        except Exception as e:
            print(f"Error getting attendance: {e}")
        finally:
            conn.disconnect()
    return []

def get_available_employee_ids(attendance_data):
    """Get a list of all employee IDs that have attendance records"""
    employee_ids = set()
    for record in attendance_data:
        employee_ids.add(str(record.user_id))
    
    return sorted(list(employee_ids))

def filter_employee_data(attendance_data, employee_id):
    """Filter attendance data for a specific employee"""
    filtered_data = []
    
    for record in attendance_data:
        if str(record.user_id) == employee_id:
            # Determine punch type (in or out)
            punch_type = "Unknown"
            if hasattr(record, 'punch'):
                if record.punch == 0:
                    punch_type = "Punch In"
                elif record.punch == 1:
                    punch_type = "Punch Out"
                else:
                    punch_type = f"Other ({record.punch})"
            
            filtered_data.append({
                'Employee ID': record.user_id,
                'Timestamp': record.timestamp,
                'Date': record.timestamp.date(),
                'Time': record.timestamp.time(),
                'Status': record.status,
                'Punch Code': record.punch if hasattr(record, 'punch') else None,
                'Punch Type': punch_type
            })
    
    return filtered_data

def organize_punch_data(filtered_data):
    """Organize punch data into daily records with in/out times"""
    daily_records = {}
    
    for record in filtered_data:
        date_str = str(record['Date'])
        
        if date_str not in daily_records:
            daily_records[date_str] = {
                'Date': record['Date'],
                'Employee ID': record['Employee ID'],
                'First Punch': record['Timestamp'],
                'First Punch Type': record['Punch Type'],
                'Last Punch': record['Timestamp'],
                'Last Punch Type': record['Punch Type']
            }
        else:
            # Update first punch if this is earlier
            if record['Timestamp'] < daily_records[date_str]['First Punch']:
                daily_records[date_str]['First Punch'] = record['Timestamp']
                daily_records[date_str]['First Punch Type'] = record['Punch Type']
            
            # Update last punch if this is later
            if record['Timestamp'] > daily_records[date_str]['Last Punch']:
                daily_records[date_str]['Last Punch'] = record['Timestamp']
                daily_records[date_str]['Last Punch Type'] = record['Punch Type']
    
    # Convert to list of records
    organized_data = list(daily_records.values())
    
    # Add duration if we have both in and out punches
    for record in organized_data:
        if record['First Punch'] != record['Last Punch']:
            duration = record['Last Punch'] - record['First Punch']
            record['Duration (hours)'] = round(duration.total_seconds() / 3600, 2)
        else:
            record['Duration (hours)'] = None
    
    return organized_data

def save_to_csv(data, filename=None, organize=True):
    """Save data to CSV file"""
    if not data:
        print(f"No data found for employee {TARGET_EMPLOYEE_ID}")
        return False
    
    # Create DataFrame
    df = pd.DataFrame(data)
    
    # Sort by timestamp
    if 'Timestamp' in df.columns:
        df.sort_values(by='Timestamp', ascending=False, inplace=True)
    elif 'Date' in df.columns:
        df.sort_values(by='Date', ascending=False, inplace=True)
    
    # Save detailed punch records
    if filename is None:
        filename = f"employee_{TARGET_EMPLOYEE_ID}_attendance.csv"
    
    df.to_csv(filename, index=False)
    print(f"Data saved to {filename}")
    
    # If organize is True, also save organized daily records
    if organize and 'Timestamp' in df.columns:
        organized_data = organize_punch_data(data)
        if organized_data:
            organized_filename = f"employee_{TARGET_EMPLOYEE_ID}_daily_summary.csv"
            organized_df = pd.DataFrame(organized_data)
            organized_df.sort_values(by='Date', ascending=False, inplace=True)
            organized_df.to_csv(organized_filename, index=False)
            print(f"Daily summary saved to {organized_filename}")
    
    return True

def main():
    # Get attendance logs from device
    print(f"Starting data extraction for employee {TARGET_EMPLOYEE_ID}...")
    attendance_logs = get_attendance_logs()
    
    if attendance_logs:
        # Get list of all employee IDs
        employee_ids = get_available_employee_ids(attendance_logs)
        print(f"Available employee IDs: {employee_ids}")
        
        # Check if target employee ID exists
        if TARGET_EMPLOYEE_ID not in employee_ids:
            print(f"Warning: Employee ID {TARGET_EMPLOYEE_ID} not found in attendance records.")
            print("Please choose from one of the available employee IDs listed above.")
            return
        
        # Filter for target employee
        filtered_data = filter_employee_data(attendance_logs, TARGET_EMPLOYEE_ID)
        
        # Save to CSV
        if filtered_data:
            save_to_csv(filtered_data)
            print(f"Successfully extracted {len(filtered_data)} records for employee {TARGET_EMPLOYEE_ID}")
        else:
            print(f"No records found for employee {TARGET_EMPLOYEE_ID}")
    else:
        print("No attendance data retrieved from device")

if __name__ == "__main__":
    main() 