"""
This is the script of the text-based program (cmdUI). It basically provides a text-based interface for the user
to interact with. After receiving the input from the user, it will call the functions in the Carpark script and
display the result from the script.
"""

import Carpark as Cp    # Import the Carpark module for all the processing functions
import time             # Import the time module for having a delay in between displays

car_park = Cp.Carpark()  # Initiate the class Carpark in the Carpark script
page_break = "\n--------------------------------------------------------------------"  # Set the page break line
delay_time = 2  # Set the delay time in between displays (in seconds)


def menu():
    # The menu page for obtaining the desired action from the user
    try:
        display = "Main Menu:\n"
        display += "1. Enter the car park.\n"
        display += "2. Exit the car park.\n"
        display += "3. View available parking spaces.\n"
        display += "4. Query parking record by ticket number.\n"
        display += "5. Quit.\n\n"
        display += "Please enter a number (1-5) to proceed: "
        action = int(input(display))
        if action not in range(1, 6):
            raise ValueError

    except ValueError:
        print(page_break)
        print('Sorry, the inputted value is not correct. Please retry.')
        delay(delay_time)
        return 0

    except BaseException as BE:
        print("\n", page_break)
        print("Error: %s" % type(BE).__name__)
        delay(delay_time)
        return 5

    else:
        return action


def enter_exit(state="enter"):
    """
    The functions for entering or exiting the car park:
    1. Do a car park availability check
    2. Request a vehicle registration number and verify the format
    3. Process the entering/exiting and return the record of parking
    """
    check, display = car_park.avail_check(state)
    if check is False:
        print(display)
        delay(delay_time)
        return 0
    else:
        display = display[:59] + "\nTo go back to the previous page, enter \"0\".\n" + display[59:]
        plate_no = input(display).upper()
    if plate_no == "0":
        return 0
    check, display = car_park.plt_check(plate_no, state)
    print(page_break)
    if check is False:
        print(display)
        delay(delay_time)
        return 1
    else:
        display = car_park.enter(plate_no)
        print(display)
        delay(delay_time)
        return 0


def view():
    # The page for checking the numbers of available parking spaces
    display = car_park.view()
    print(display)
    delay(delay_time)
    return 0


def query():
    # The page for checking the parking record with the ticket number
    display = car_park.query()
    display = display[:51] + "\nor enter \"0\" to go back to the previous page" + display[51:]
    data = input(display).upper()
    if data == "0":
        return 0
    check, display = car_park.search(data)
    print(page_break)
    print(display)
    delay(delay_time)
    if check is False:
        return 4
    else:
        return 0


def quit_program():
    # Function for quiting the program
    car_park.save()
    return 6


def delay(sec):
    # Function for delaying the program
    time.sleep(sec)


# The main loop of the program and react when an error arise
try:
    stage = 0
    print(page_break, "\nWelcome to the car park!")
    delay(delay_time)
    while stage in range(0, 6):
        print(page_break)
        if stage == 0:
            stage = menu()
        elif stage == 1:
            stage = enter_exit("enter")
        elif stage == 2:
            stage = enter_exit("exit")
        elif stage == 3:
            stage = view()
        elif stage == 4:
            stage = query()
        elif stage == 5:
            stage = quit_program()


except BaseException as e:
    print(page_break)
    print("Error: %s" % type(e).__name__)
    print(page_break)
    delay(delay_time)
    quit()

finally:
    print("Have a nice day, Bye!")
    print(page_break)
