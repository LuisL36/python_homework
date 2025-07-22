# Write your code here.
def hello():
    return "Hello!"

def greet(name):
    return f"Hello, {name}!"

def calc(a, b, op="multiply"):
    try: 
        match op:
            case "add":
                return a + b
            case "subtract":
                return a - b
            case "multiply":
                return a * b
            case "divide":
                return a / b 
            case "modulo":
                return a % b
            case "int_divide":
                return a // b 
            case "power":
                return a ** b
            case _:
                return None
    except ZeroDivisionError:
        return "You can't divide by 0!"
    except TypeError: 
        return "You can't multiply those values!"

def data_type_conversion(value, dtype):
    try: 
        if dtype == "int":
            return int(value)
        elif dtype == "float":
            return float(value)
        elif dtype == "str":
            return str(value)
    except (ValueError, TypeError):
        return f"You can't convert {value} into a {dtype}."

def grade(*args):
    try:
        avg = sum(args) / len(args)
        if avg >= 90:
            return "A"
        elif avg >= 80:
            return "B"
        elif avg >= 70:
            return "C"
        elif avg >= 60:
            return "D"
        else:
            return "F"
    except:
        return "Invalid data was provided."
    
def repeat(string, count):
    result = ""
    for _ in range(count):
        result += string
    return result

def student_scores(mode, **kwargs):
    if mode == "best":
        return max(kwargs, key=kwargs.get)
    elif mode == "mean":
        return sum(kwargs.values()) / len(kwargs)
    
def titleize(text):
    little_words = {"a", "on", "the", "of", "and", "is", "in"}
    words = text.split()
    result = []
    
    for i, word in enumerate(words): 
        if i == 0 or i == len(words) - 1:
            result.append(word.capitalize())
        elif word in little_words:
            result.append(word)
        else: 
            result.append(word.capitalize())
            
    return " ".join(result)
            
def hangman(secret, guess):
    result = ""
    for letter in secret:
        if letter in guess:
            result += letter
        else:
            result += "_"
    return result

def pig_latin(sentence):
    vowels = "aeiou"
    words = sentence.split()
    result = []
    
    for word in words:
        if word.startswith("qu"):
            result.append(word[2:] + "quay")
        elif word[0] in vowels:
            result.append(word + "ay")
        else:
            i = 0
            while i < len(word) and word[i] not in vowels:
                if word[i:i+2] == "qu":
                    i += 2
                    break
                i += 1
            result.append(word[i:] + word[:i] + "ay")
            
    return " ".join(result)