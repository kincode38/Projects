#python weight converter

weight = float(input("Enter your weigth: "))
unit = input("Kilograms or pounds? (K/L): ")

if unit == "K":
    weight = weight * 2.205
    unit = "LBS."
    print(f"your weight is {round(weight, 1)} {unit}") 
elif unit == "L":
    weight = weight / 2.205
    unit = "KGS."
    print(f"your weight is {round(weight, 1)} {unit}") 
else:
    print(f"{unit} is not valid") 

  
    