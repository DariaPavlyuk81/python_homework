

import pandas as pd

df = pd.read_csv("../csv/employees.csv")

# Using a list comprehension, create a list of the employee names, first_name + space + last_name. 
full_names = [row['first_name'] + " " + row['last_name'] for index, row in df.iterrows()]
print("All employee names:")
print(full_names)

# list should include only those names that contain the letter "e". 
names_with_e = [name for name in full_names if 'e' in name.lower()]
print("\nNames containing the letter 'e':")
print(names_with_e)
