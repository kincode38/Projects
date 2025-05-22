#python calculator 

operator = input("Choose your operator (+ - * /): ")
num1 = float(input("Enter your number:  "))
num2 = float(input("Enter your number:  "))

if operator == "+":
    result = num1 + num2
    print(round(result, 3))
elif operator == "-":
    result = num1 - num2
    print(round(result, 3)) 
elif operator == "*":
    result = num1 *num2
    print(round(result, 3))
elif operator == "/":
    result = num1 / num2
    print(round(result, 3))   
else:
    print(f"{operator} is NOT found")    
try:
    print("1/0")
except ZeroDivisionError:
    print("You can't divide by zero!")