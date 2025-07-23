import csv
import traceback
import os
import custom_module
from datetime import datetime


def read_employees():
    try:
        data = {}
        rows = []
        with open("../csv/employees.csv", "r") as f: 
            reader = csv.reader(f)
            for i, row in enumerate(reader):
                if i == 0:
                    data["fields"] = row
                else:
                    rows.append(row)
        data["rows"] = rows
        return data
    except Exception as e:
        trace_back = traceback.extract_tb(e.__traceback__)
        stack_trace = [f'file : {trace[0]} , Line : {trace[1]}, Func.Name : {trace[2]}, Message : {trace[3]}' for trace in trace_back]
        print(f"Exception type: {type(e).__name__}")
        message = str(e)
        if message:
            print(f"Exception message: {message}") 
        print(f"stack trace: {stack_trace}")
        
employees = read_employees()
print(employees) 

def column_index(header_name):
    return employees["fields"].index(header_name)

employee_id_column = column_index("employee_id")

def first_name(row_number):
    first_name_col = column_index("first_name")
    return employees["rows"][row_number][first_name_col]

def employee_find(employee_id):
    def employee_match(row):
        return int(row[employee_id_column]) == employee_id
    matches = list(filter(employee_match, employees["rows"]))
    return matches

def employee_find_2(employee_id):
    matches = list(filter(lambda row: int(row[employee_id_column]) == employee_id, employees["rows"]))
    return matches

def sort_by_last_name():
    last_name_col = column_index("last_name")
    employees["rows"].sort(key=lambda row: row[last_name_col])
    return employees["rows"]

def employee_dict(row):
    result = {}
    for i, field in enumerate(employees["fields"]):
        if field != "employee_id":
            result[field] = row[i]
    return result

def all_employees_dict():
    result = {}
    for row in employees["rows"]:
        emp_id = (row[employee_id_column])
        result[emp_id] = employee_dict(row)
    return result

def get_this_value():
    return os.getenv("THISVALUE")

def set_that_secret(new_secret):
    custom_module.set_secret(new_secret)
    
def read_csv_to_dict(filepath):
    try:
        data = {}
        rows = []
        with open(filepath, "r") as f:
            reader = csv.reader(f)
            for i, row in enumerate(reader):
                if i == 0:
                    data["fields"] = row
                else:
                    rows.append(tuple(row)) 
        data["rows"] = rows
        return data
    except Exception as e: 
        trace_back = traceback.extract_tb(e.__traceback__)
        stack_trace = [f'file : {trace[0]} , Line : {trace[1]}, Func.Name : {trace[2]}, Message : {trace[3]}' for trace in trace_back]
        pass

def read_minutes():
    minutes1 = read_csv_to_dict("../csv/minutes1.csv")
    minutes2 = read_csv_to_dict("../csv/minutes2.csv")
    return minutes1, minutes2

minutes1, minutes2 = read_minutes()
print(minutes1)
print(minutes2)

def create_minutes_set(): 
    m1, m2, = read_minutes()
    minutes_combined = m1["rows"] + m2["rows"]
    return set(minutes_combined)

minutes_set = create_minutes_set()
def create_minutes_list(): 
    temp_list = list(minutes_set)
    converted = map(lambda x: (x[0], datetime.strptime(x[1], "%B %d, %Y")), temp_list)
    return list(converted)

minutes_list = create_minutes_list()

def write_sorted_list():
    sorted_list = sorted(minutes_list, key=lambda x: x[1])
    
    final_data = list(map(lambda x: (x[0], x[1].strftime("%B %d, %Y")), sorted_list))
    
    with open("./minutes.csv", "w", newline="") as f: 
        writer = csv.writer(f)
        writer.writerow(minutes1["fields"])
        writer.writerows(final_data)
    
    return final_data
