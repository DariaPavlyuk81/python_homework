import csv
import os
import custom_module
from datetime import datetime



#task2
employees = {}

def read_employees():
    try:
        dic = {
            "fields":[],
            "rows":[]
        }
        #open CSV file
        with open('python_homework/csv/employees.csv', mode='r') as file:
            reader = csv.reader(file)

            #read the first row as a header
            dic["fields"] = next(reader)

            #adding all the other raws
            for row in reader:
                dic["rows"].append(row)
        #return dictionary       
        return dic
    
    #catch exception
    except Exception as e:
        print(f"An exception occurred: {type(e).__name__}: {str(e)}")
        raise

employees = read_employees()

print(employees)


#task3
def column_index(column_name):
    try:
        return employees["fields"].index(column_name)
    except ValueError:
        raise ValueError(f"Column '{column_name}' not found in employees['fields']")
    
#call the column-index function
employee_id_column = column_index("employee_id")

#task4
def first_name(row_number):
    try:
        #column index that you want of the 'first_name' column
        first_name_column = column_index("first_name")

        #retrieve the row based on the row_number 
        row = employees["rows"][row_number]

        #get the value of the 'first_name' from the row
        return row[first_name_column]
    except IndexError:
        #if the row number is invalid
        raise ValueError(f"Row number {row_number} is out of range. ")
    except Exception as e:
        #if unexpected errors
        raise ValueError(f"An errror occured: {type(e).__name__}: {str(e)}")
    
    #task5
def employee_find(employee_id):
    #inner function
    def employee_match(row):
        return int(row[employee_id_column]) == employee_id
    
    #filter to find matching rows
    matches = list(filter(employee_match, employees["rows"]))

    #return the list of matches
    return matches

#task6
def employee_find_2(employee_id):
    matches = list(filter(lambda row : int(row[employee_id_column]) == employee_id ,employees ["rows"]))
    return matches

#task7
def sort_by_last_name():
    #find the index of the 'last_name' column
    last_name_column = column_index("last_name")

    #sort employees["rows"] in place using the 'last name' column
    employees["rows"].sort(key=lambda row: row[last_name_column])
    
    return employees["rows"]

#task#8
def employee_dict(row):
    #using zip()to pair column headers with values from the row
    employee_data = dict(zip(employees["fields"],row))

    #remove the 'employee_id'key from the dictionary
    if "employee_id" in employee_data:
        del employee_data["employee_id"]

    #return the resulting dict for the employee
    return employee_data

#task9
def all_employees_dict():
    #create an empty dictionary
    employees_dict = {}
    #loop through each row 
    for row in employees["rows"]:
        employee_id = row[employee_id_column]
        employees_dict[employee_id] = employee_dict(row)

    #return the resulting dictionary
    return employees_dict

#task10
def get_this_value():
    return os.getenv("THISVALUE")

print('Value of THISVALUE:', get_this_value())

#task11
def set_that_secret(new_secret):
    custom_module.set_secret(new_secret)  

set_that_secret("open, sesame!")
print(custom_module.secret)
    

#task12
def read_csv_file(file_path):
    try:
        with open(file_path, mode='r') as file:
            reader = csv.reader(file)
            fields = next(reader)
            rows = [tuple(row)for row in reader]
            return {"fields": fields, "rows": rows}
    except Exception as e:
        raise ValueError(f"Error reading file {file_path}: {e}")
    
def read_minutes():
    minutes1 = read_csv_file('python_homework/csv/minutes1.csv')   
    minutes2 = read_csv_file('python_homework/csv/minutes2.csv')
    return minutes1, minutes2
minutes1, minutes2 = read_minutes()

print("Minutes 1:", minutes1)
print("Minutes 2:", minutes2)

#task13
def create_minutes_set():
    set1 = set(minutes1["rows"])
    set2 = set(minutes2["rows"])
#combine both sets
    combined_set = set1.union(set2)
#return the resultin set
    return combined_set
#global varieable to store the result
minutes_set = create_minutes_set()

print("Minutes Set:", minutes_set)

#task14
def create_minutes_list():
    #convert minutes_set to a list
    minutes_list = list(minutes_set)

    #use map() to convert each element of the list
    converted_list = list(map(lambda x: (x[0], datetime.strptime(x[1],"%B %d, %Y")),minutes_list))

    return converted_list

minutes_list = create_minutes_list()
print("Minutes List (converted to datetime):", minutes_list)

#task15
def write_sorted_list():
    minutes_list.sort(key= lambda x: x[1])
    minutes_list1 = list(map(lambda row: (row[0], datetime.strftime(row[1], "%B %-d, %Y")), minutes_list))
    with open ("./minutes.csv", "w") as file:
        writer = csv.writer(file)
        writer.writerow(minutes1["fields"])
        for row in minutes_list1:
            writer.writerow(row)
    return minutes_list1

write_sorted_list()
    