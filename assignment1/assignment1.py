# Write your code here.
# assignment1.py
#task1
def hello():
    return "Hello!"

print ("hello: ",hello())

#task2
def greet(name):
    return f"Hello, {name}!"


#task3
def calc(a, b, operation="multiply"):
    try:
        match operation:
            case "add":
                return a + b
            
            case "divide":
                if b == 0:
                    return "You can't divide by 0!"
                return a / b
            case "multiply":
                return a * b
            case "subtract":
                return a - b
            case "modulo":
                return a % b
            case "int_divide":
                if b == 0:
                    return "You can't divide by 0!"
                return a // b
                
            case "power":
                return a ** b
            case _:
                return "Invalid operation"
    except TypeError:
        return "You can't multiply those values!"
    
    
#task4

def data_type_conversion(value, type_name):
        try:
            match type_name:
                case "int":
                    return int(value)
                case "float":
                    return float(value)
                case "str":
                    return str(value)
                case _:
                    return "Invalid type name"
        except ValueError:
                return f"You can't convert {value} into a {type_name}."
                
#task5
        
def grade(*args):
        try:
            #convert each argument to float to handle non-numeric inputs
            grades = [float(grade) for grade in args]
            avg = sum(grades) / len(grades)#calculate the average
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
        except ValueError:
            return "Invalid data was provided."
        
#task6
        
def repeat(value, count):
    result = ""     
    for _ in range(count):
        result += value 
    return result

#task7
def student_scores(option, **kwargs):
    if option == "mean":
        #calculate the average score of all students
        total_score = sum(kwargs.values()) #sum of all students' scores
        count = len(kwargs) #Number of students
        return total_score / count  #Return the average score
    
    elif option == "best":
        #students with the highest score
        best_student = max(kwargs,key=kwargs.get)
        return best_student
    
    else:
        return "Invalid option"
                
#task8
def titleize(text):
    #list of little words that should remain lowercase
    little_words = {"a","on","an","the","of","and","is","in"} 

    #split the input string into words   
    words = text.split()

    #Iterate through the words and titleize accordingly
    for i, word in enumerate(words):
        #first and last word always capitalize
        if i == 0 or i == len(words) - 1:
            words[i] = word.capitalize()
        #if the word is not a little word,capitalize it
        elif word.lower() not in little_words:
            words[i] = word.capitalize()
        #if it is a little word, leave lower case
        else:
            words[i] = word.lower()
        
        #join the words back into a single string and return
    return " ".join(words)


    
#task9
def hangman(word, guessed_letters):
    result = []

    #iterate through each letter in the word
    for letter in word:
        #if the letter is in guessed_letters, append it to result
        if letter in guessed_letters:
            result.append(letter)
        else:
        #if not, append an underscore
            result.append('_')
    #join the list into a string and return it
    return ''.join(result)

#task10
def pig_latin(s):
    vowels = "aeiouAEIOU"
    out_string = ""
    start_string = ""
    rest_string = ""
    for ch in s:
        if (ch == " "):
            if(rest_string):
                if len(out_string) > 0:
                    out_string += " "
                out_string += rest_string + start_string + "ay"
                rest_string = ""
                start_string = ""
        elif len(rest_string) > 0:
            rest_string += ch
        elif (ch == "u" or ch == "U") and len(start_string) > 0 and \
                (start_string[-1] == "q" or start_string[-1] == "Q"):
                start_string += ch
        elif ch in vowels:
            rest_string += ch
        else:
            start_string += ch

    if rest_string:
        if len(out_string) > 0:
            out_string += " "
        out_string += rest_string + start_string + "ay"

    return out_string
                