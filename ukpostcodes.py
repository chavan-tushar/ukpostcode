'''
This file has functions to validate and format Post codes of UK.
More information about the post codes can be found at https://en.wikipedia.org/wiki/Postcodes_in_the_United_Kingdom#Formatting
User has 2 options, they can either enter the post code to validate or they can enter 'exit' to return to main execution.
Once user enters post code, the script will first check if it falls under a normal post code or a special cases.
if the post code is in normal format (Please refer to wiki site), then additional checks are performed to validate its authenticity.
if the post code is in special format (Please refer to wiki site), then it will be checked in specialCases.py file if it is mentioned there.
appropriate message will be displayed on the screen.
'''

import re
import specialCases as sc

area = district = sector = unit = postcode = outward = inward = formatted_postcode = ""
mode = "test"

# Purpose of this function is to display messages.
# In case of error more information will be provided.
def display_message(message_type, *error):
    message = ""
    if message_type == "normal":
        message = "Please enter Post Code to validate or type 'exit' to end this loop : "
    elif message_type == "error":
        message = f"Invalid Post Code {error[0]}.\nPlease check your response!"
    elif message_type == "exit":
        message = "Thank you!"
    elif message_type == "success":
        message = f"Entered Post Code '{formatted_postcode}', can be a valid one."
    elif message_type == "confirmSuccess":
        message = f"Entered Post Code '{formatted_postcode}', is a valid one."
    elif message_type == 'blank':
        message = "Please provide Post Code."

    return message


# Purpose of this function is to find particular element el in list l.
# used binary search algorithm.
def findElementInList(el,l):
    l.sort()
    start = 0
    end = len(l) -1
    to_return = False
    while start <= end and not to_return:
        mid = (start + end) // 2
        if l[mid] == el:
            to_return = True
        else:
            if el < l[mid]:
                end = mid - 1
            else:
                start = mid + 1
    return to_return


# Purpose of this function is to divide the entered post code and assign values to area, district, sector, unit
def getDetails(p):
    global area, district, sector, unit, postcode, outward, inward
    postcode = postcode.upper()
    postcode_without_space = postcode.replace(" ", "")
    # In post code, Last 3 characters will in inward and everything else will be outward.
    outward = postcode_without_space[:len(postcode_without_space) - 3]
    inward = postcode_without_space[len(postcode_without_space) - 3:]

    # disctrict will always start with number. Anything before that will be area.
    district_start_pos = 0
    for pos, char in enumerate(outward):
        if char.isdigit():
            district_start_pos = pos
            break

    area = outward[0:district_start_pos]
    district = outward[district_start_pos:]
    sector = inward[0]
    unit = inward[1:]
    #return area, district, sector, unit, postcode, outward, inward


# in case of normal postcode this function will format any post code to '{area}{district} {sector}{unit}'
# in case of special postcode this function will simply convert post code to uppercase.
def format_postcodes(p, type_of_postcode):
    global formatted_postcode, area, district, sector, unit
    if type_of_postcode == 'normal':
        #area, district, sector, unit, *other = getDetails(p)
        #getDetails(p)
        formatted_postcode = f"{area}{district} {sector}{unit}"
    else:
        formatted_postcode = p.upper()


# The purpose of this function is to validate the post code.
def validate_postcode(*p):
    global area, district, sector, unit, postcode, outward, inward, formatted_postcode

    while True:
        try:
            formatted_postcode = ""
            if mode == "live":
                postcode = input(display_message('normal'))
            else:
                postcode = p[0]

        except ValueError:
            print(display_message('error'))

        else:
            if postcode.strip().lower() == 'exit':
                print(display_message('exit'))
                break

            elif postcode.strip() == "":
                print(display_message("blank"))
                continue
            else:
                #area, district, sector, unit, postcode, outward, inward = getDetails(postcode)
                getDetails(postcode)

                #Normal Postcodes
                if (re.fullmatch(r"^[A-Z]{1,2}[0-9][A-Z0-9]? ?[0-9][A-Z]{2}$", postcode)):
                    format_postcodes(postcode, "normal")

                    # Areas with only single-digit districts: BR, FY, HA, HD, HG, HR, HS, HX, JE, LD, SM, SR, WC, WN, ZE (although WC is always subdivided by a further letter, e.g. WC1A)
                    if findElementInList(area, ['BR', 'FY', 'HA', 'HD', 'HG', 'HR', 'HS', 'HX', 'JE', 'LD', 'SM', 'SR', 'WN', 'ZE']) and len(district) > 1:
                        print(display_message("error", f"{area} should have only 1 digit for District "))
                        if mode == 'test':
                            return False
                    # Areas with only double-digit districts: AB, LL, SO
                    elif findElementInList(area, ['AB', 'LL', 'SO']) and (not len(district) == 2 or re.search(r'[A-Z]+', district)):
                        print(display_message("error", "'AB', 'LL', 'SO' areas should have only double-digit district"))
                        if mode == 'test':
                            return False
                    # Areas with a district '0' (zero): BL, BS, CM, CR, FY, HA, PR, SL, SS
                    elif not findElementInList(area, ['BL', 'BS', 'CM', 'CR', 'FY', 'HA', 'PR', 'SL', 'SS']) and district == "0":
                        print(display_message("error", "Only 'BL', 'BS', 'CM', 'CR', 'FY', 'HA', 'PR', 'SL', 'SS' areas can have district 0"))
                        if mode == 'test':
                            return False
                    # BS is the only area to have both a district 0 and a district 10
                    elif findElementInList(area, ['BL', 'CM', 'CR', 'FY', 'HA', 'PR', 'SL', 'SS']) and district == "10":
                        print(display_message("error", "BS is the only area that can have both a district 0 and a district 10"))
                        if mode == 'test':
                            return False
                    # The only letters to appear in the third position are A, B, C, D, E, F, G, H, J, K, P, S, T, U and W when the structure starts with A9A.
                    elif re.match(r'^[A-Z0-9]{2}[A-Z]',postcode) and not findElementInList(postcode[2], list("ABCDEFGHJKPSTUW")): #postcode[2] not in "ABCDEFGHJKPSTUW":
                        print(display_message("error", "The only letters to appear in the third position are A, B, C, D, E, F, G, H, J, K, P, S, T, U and W when the structure starts with A9A"))
                        if mode == 'test':
                            return False
                    # The only letters to appear in the fourth position are A, B, E, H, M, N, P, R, V, W, X and Y when the structure starts with AA9A.
                    elif re.match(r'^[A-Z]{2}[0-9]{1}[A-Z]{1}',postcode) and not findElementInList(postcode[3], list("ABEHMNPRVWXY")): # postcode[3] not in "ABEHMNPRVWXY":
                    # elif re.match(r'^[A-Z]{2}[0-9][A-Z]',postcode) and not re.match(r'^[A-Z]{2}[0-9]{1}[A-Z]{1}[ABEHMNPRVWXY]{1}', postcode):
                        print(display_message("error", "The only letters to appear in the fourth position are A, B, E, H, M, N, P, R, V, W, X and Y when the structure starts with AA9A"))
                        if mode == 'test':
                            return False
                    # The letters Q, V and X are not used in the first position.
                    elif re.match(r'^Q|V|X',area):
                        print(display_message("error", "Postcode cannot start with Q, V, or X"))
                        if mode == 'test':
                            return False
                    # The letters I, J and Z are not used in the second position.
                    elif re.match(r'^.[IJZ]{1}',area):
                        print(display_message("error", "Second character of postcode cannot be I, J, or Z"))
                        if mode == 'test':
                            return False
                    # The final two letters do not use C, I, K, M, O or V, so as not to resemble digits or each other when hand-written.
                    elif set(postcode[-2:]).intersection(set(list("CIKMOV"))):
                        print(display_message("error", "Final two letters can not use C, I, K, M, O or V, so as not to resemble digits or each other when hand-written."))
                        if mode == 'test':
                            return False
                    # Postcode sectors are one of ten digits: 0 to 9, with 0 only used once 9 has been used in a post town, save for Croydon and Newport
                    elif sector == "0" and not re.match(r'[0-9][A-Z]',district):
                        print(display_message("error", "Post code can have sector 0 only if 0-9 has been used in a post town."))
                        if mode == 'test':
                            return False
                    # Central London single-digit districts have been further divided by inserting a letter after the digit and before the space.
                    elif district[-1].isalpha():

                        # only these districts can have a character at the end.
                        # district E1 can have only W as last character.
                        # district N1 can have only C or P as last character.
                        # district NW1 can have only W as last character.
                        # district SE1 can have only P as last character.
                        if not findElementInList(outward[:-1], ['EC1','EC2','EC3','EC4','SW1','W1','WC1','WC2','E1','N1','NW1','SE1']):
                            print(display_message("error", "Only 'EC1-EC4','SW1','W1','WC1','WC2','E1','N1','NW1','SE1' areas can have a letter after digit for district"))
                            if mode == 'test':
                                return False
                        elif outward[:-1] == "E1" and not outward[-1] == "W":
                            print(display_message("error", "Only possible outward for E1 is E1W"))
                            if mode == 'test':
                                return False
                        elif outward[:-1] == "N1" and not outward[-1] in 'CP':
                            print(display_message("error", "Only possible outward for N1 are N1C or N1P"))
                            if mode == 'test':
                                return False
                        elif outward[:-1] == "NW1" and not outward[-1] == 'W':
                            print(display_message("error", "Only possible outward for NW1 is NW1W"))
                            if mode == 'test':
                                return False
                        elif outward[:-1] == "SE1" and not outward[-1] == 'P':
                            print(display_message("error", "Only possible outward for SE1 is SE1P"))
                            if mode == 'test':
                                return False
                        else:
                            print(display_message('success'))
                            if mode == 'test':
                                return True
                    else:
                        print(display_message('success'))
                        if mode == 'test':
                            return True

                #Special Postcodes
                elif re.fullmatch(r"^(([A-Z]{1,2}[0-9][A-Z0-9]?|ASCN|STHL|TDCU|BBND|[BFS]IQQ|PCRN|TKCA) ?[0-9][A-Z]{2}|BFPO ?[0-9]{1,4}|(KY[0-9]|MSR|VG|AI)[ -]?[0-9]{4}|[A-Z]{2} ?[0-9]{2}|GE ?CX|GIR ?0A{2}|SAN ?TA1)$", postcode):
                    format_postcodes(postcode, "special")

                    # importing all special cases post codes from specialCases.py and storing it in special_cases.
                    special_cases = sc.special_postcodes()

                    # if entered post code is a part of special cases then success message will be displayed.
                    if findElementInList(postcode, special_cases):
                        print(display_message("confirmSuccess"))
                        if mode == 'test':
                            return True
                    else:
                        print(display_message("error", f"Provided Postcode '{formatted_postcode}' is invalid.\n If the provided post code falls under special category, then make sure to include space as well, if applicable."))
                        if mode == 'test':
                            return False
                else:
                    print(display_message('error', f"'{postcode}' Please Enter Valid Post code"))
                    if mode == 'test':
                        return False

if __name__ == '__main__':
    validate_postcode()