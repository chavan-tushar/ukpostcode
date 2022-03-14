'''
This file will print numbers 1-100.
if the number is multiple of 3 then "Three" will be displayed
if the number is multiple of 5 then "Five" will be displayed.
if the number is multiple of 3 and 5 both then "ThreeFive" will be displayed.
else that particular number will be displayed.
'''

def print_number():
    for num in range(1,101):
        if num % 3 == 0 and num % 5 == 0:
            print("ThreeFive")
        elif num % 5 == 0:
            print("Five")
        elif num % 3 == 0:
            print("Three")
        else:
            print(num)
    print("")

if __name__ == '__main__':
    print_number()