'''
This is the main file for this project.
There are two parts of this project.

1.  To print number 1-100. If the number is multiples of three print “Three” instead of the number
    and for the multiples of five print “Five”.
    For numbers which are multiples of both three and five print “ThreeFive”

2.  Validating and Formatting post codes for UK.

User can enter 1 or 2 to run above mentioned programs.
User can also select 3 to terminate the program.

'''

import printNumbers as pn
import ukpostcodes as up


def display_message(message_type):
    message = ""
    if message_type == 'normal':
        message = "This coding challenge has 2 tasks\n" \
                   "1. Print number 1 to 100\n" \
                   "2. Validating and formatting UK post codes\n" \
                   "3. To Exit\n\n" \
                   "Please enter 1, 2 or 3 to proceed : "
    elif message_type == 'error':
        message = "\nPlease select correct option"
    return message


def infoMessage():
    while True:
        try:
            user_selection = int(input(display_message('normal')))

        except ValueError:
            print(display_message('error'))
            continue

        else:
            valid_user_selection = [1, 2, 3]
            if user_selection not in valid_user_selection:
                print("Please select correct option")
                continue
            if user_selection == 3:
                print("Thank you!")
                break

            #if user select 1 then print_number() from
            pn.print_number() if user_selection == 1 else up.validate_postcode()


if __name__ == '__main__':
    infoMessage()
