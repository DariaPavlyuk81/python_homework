

def type_converter(type_of_output):
    def decorator(func):
        def wrapper(*args, **kwargs):
            x = func(*args, **kwargs)
            return type_of_output(x)
        return wrapper
    return decorator

# Write a function return_int() that takes no arguments and returns the integer value 5. 
@type_converter(str)
def return_int():
    return 5

# Write a function return_string() that takes no arguments and returns the string value "not a number".
@type_converter(int)
def return_string():
    return "not a number"


if __name__ == "__main__":
    y = return_int()
    print(type(y).__name__) 

    try:
        y = return_string()
        print("shouldn't get here!")
    except ValueError:
        print("can't convert that string to an integer!")  
