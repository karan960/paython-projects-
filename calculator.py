def main():
    print("**** This is the basic calculator ****")
    print("*** Menu ***")
    print("*** 1 for Addition      ***")
    print("*** 2 for Subtraction   ***")
    print("*** 3 for Division      ***")
    print("*** 4 for Multiplication ***")

    while True:
        operation = input("Enter choice (1/2/3/4) or 'q' to quit: ")
        
        if operation == 'q':
            print("Exit the calculator. Goodbye!")
            break
        
        if operation in ['1', '2', '3', '4']:
            try:
                print("\n")
                x = float(input("Enter first number: ")) 
                y = float(input("Enter second number: "))

                result = switchcase(int(operation), x, y) 
                print("*******************")
                print(f"Result: {result}**")
                print("*******************\n")
            except ValueError:
                print("Invalid input. Please enter numeric values.") 
        else: 
            print("Invalid choice. Please select a valid operation.")

def add(x, y): 
    return x + y 

def subtract(x, y): 
    return x - y 

def multiply(x, y): 
    return x * y 

def divide(x, y):
    if y == 0: 
        return "Error: Division by zero" 
    return x / y

def switchcase(operation, x, y):
    switcher = {  
        1: add,
        2: subtract,  
        3: divide,
        4: multiply
    }  
    func = switcher.get(operation, lambda x, y: "Invalid operation")
    return func(x, y)  

if __name__ == "__main__":
    main()
