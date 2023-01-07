i = 0
keep_going = True
while keep_going:
    if i == 4:
        print(f"Abbruch bei i = {i}")
        keep_going = False
        break
        
    i += 1
    print(f"in Schleife: {i}")

print(f"nach Schleife: {i}")