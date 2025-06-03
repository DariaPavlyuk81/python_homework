#Task 1: Writing and Testing a Decorator


import logging
from functools import wraps

# One-time setup for the logger
logger = logging.getLogger(__name__ + "_parameter_log")
logger.setLevel(logging.INFO)
logger.addHandler(logging.FileHandler("./decorator.log", "a"))

def logger_decorator(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        # Prepare parameter info
        pos_params = list(args) if args else "none"
        kw_params = kwargs if kwargs else "none"
        
        
        result = func(*args, **kwargs)

        
        logger.info(f"function: {func.__name__}")
        logger.info(f"  positional parameters: {pos_params}")
        logger.info(f"  keyword parameters: {kw_params}")
        logger.info(f"  return: {result}")
        logger.info("-" * 40)

        return result
    return wrapper

# Declare a function that takes no parameters and returns nothing. 
@logger_decorator
def say_hello():
    print("Hello, World!")

# Declare a function that takes a variable number of positional arguments
@logger_decorator
def accepts_positional(*args):
    return True

# Keyword arguments
@logger_decorator
def accepts_keywords(**kwargs):
    return logger_decorator

# call each of these three functions,
if __name__ == "__main__":
    say_hello()
    accepts_positional(10, 20, 30)
    accepts_keywords(name="Alice", age=30)
