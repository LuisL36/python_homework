import traceback

try: 
    with open("diary.txt", "a") as file:
        prompt = "What happened today? "
        while True:
            entry = input(prompt)
            file.write(entry + "/n")
            if entry.lower() == "done for now":
                break
            prompt = "what else? "
except Exception as e: 
    trace_back = traceback.extract_tb(e._traceback__)
    stack_trace = [f'file : {trace[0]} , Line : {trace[1]}, Func.Name : {trace[2]}, Message : {trace[3]}' for trace in trace_back]
    print(f"Exception type: {type(e),__name__}")
    message = str(e)
    if message:
        print(f"Exception message: {message}")    
    print(f"Stack trace: {stack_trace}")
        