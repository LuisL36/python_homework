import logging 

logger = logging.getLogger(__name__ + "_paremeter_log")
logger.setLevel(logging.INFO)
logger.addHandler(logging.FileHandler("./decorator.log", "a"))

def logger_decorator(func):
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        logger.info(f"function: {func.__name__}"
                    f"ositional aprameters: { args if args else 'none'}"
                    f"keyword parameters: {kwargs if kwargs else 'none'}"
                    f"return: {result}")
        return result
    return wrapper

@logger_decorator
def greet():
    print("Hello, World!")
    
@logger_decorator
def always_true(*args):
    return True

@logger_decorator
def return_decorator(**kwargs):
    return logger_decorator

if __name__ == "__main__":
    greet()
    always_true(1, 2, 3)
    return_decorator(key="value")