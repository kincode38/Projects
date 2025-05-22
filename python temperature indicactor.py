#python temperature indicactor

temp = float(input("Enter the temperature: "))
unit = input("Is this the temperature Celcius or Fahrenheit (C/F):  ")

if unit == "C":
    temp = round((9 * temp) / 5 + 32, 1)
    print(f"The temperature in fahrenheit {temp}F")
elif unit == "F":
    temp = round((temp - 32) * 5 / 9, 1)
    print(f"The temperature in Celcius {temp}C")
else:
    print(f"{unit} unit of measurement is not valid")