import traceback

def write_to_diary():
    try:
        with open('diary.txt', 'a') as file:
            while True:
                if file.tell() == 0:
                    prompt = "What happened today? "
                else:
                    prompt = "What else? "

                user_input = input(prompt)

# done for now
                if user_input.lower() == "done for now":
                    file.write("done for now\n")
                    break

                #user input
                file.write(user_input + "\n")

    except Exception as e:
        trace_back = traceback.extract_tb(e.__traceback__)
    stack_trace = list() 
    for trace in trace_back:
        stack_trace.append(f'File : {trace[0]} , Line : {trace[1]}, Func.name : {trace[2]}, Message : {trace[3]}')
    print(f"Esception type: {type(e).__name__}")
    message = str(e)
    if message:
        print(f"Esception message: {message}")
    print(f"Stack trace: {stack_trace}")

if __name__ == "__main__":
    write_to_diary()