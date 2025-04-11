"""
This is the script of the main logic codes which including the enter, exit, view available parking spaces
and the query of parking record functions. Also, it includes the functions to read/write the csv file.
This script will wait for the call from the cmdUI or GUI script, then process with the input from those scripts and
return a result to them for displaying to the user.
"""

import time                     # import the time module for recording the entry and exit time
import csv                      # import the csv module for reading/writing the csv file
import random                   # import the random module for allocating the parking space
from datetime import datetime   # import the datetime module for converting the seconds to a timestamp


# Construct a class of the car park so that all the temporary memories are stored in the class
class Carpark:

    def __init__(self, cap=10):
        """
        Initiate the class with all the settings of the car park, such as:
        - self.cap: the capacity of the car park
        - self.avail_space: a set of all the available parking slots
        - self.file: the file name for storing all the record

        Then, read from the record and store the record into the temporary memories:
        - self.record: a list storing all rows of data from the record
        - self.ticket_list: a dictionary of all the ticket numbers issued with the ticket number as the key
                            and the details of parking as the value
        - self.parked_car: a dictionary of all parked cars with the plate number as the key
                           and the latest ticket number as the value
        - self.parking_car: a dictionary of all parking cars with plate numbers as the key
                           and the current ticket number as the value
        - self.avail_space: discard the occupied slots from the set of the available parking slots
        - self.avail_no: the amount of available parking space
        - self.ticket: the BST for storing the ticket numbers and the parking records
        """
        self.cap = cap
        self.avail_space = set(range(1, self.cap + 1))
        self.file = "Record.csv"
        self.record = read_file(self.file)
        self.ticket_list, self.parked_car, self.parking_car, occupied_space = sort_data(self.record)
        for space in occupied_space:
            self.avail_space.discard(int(space))
        self.avail_no = len(self.avail_space)
        lt = [x for x in self.ticket_list.keys()]
        if lt:
            self.ticket = self.bst(lt, self.ticket_list)
        else:
            self.ticket = Ticket()

    def bst(self, lt, dt):
        # Optimize the BST when doing the first reading from the record
        lt.sort()
        mid = len(lt) // 2
        ticket, plt, space, entry_time, exit_time, fee, index = dt[lt[mid]]
        pass_list = [ticket, plt, space, entry_time, exit_time, fee, index]
        root = Ticket(pass_list)
        if lt[:mid]:
            root.left = self.bst(lt[:mid], dt)
        if lt[mid+1:]:
            root.right = self.bst(lt[mid + 1:], dt)
        return root

    def avail_check(self, stage="enter"):
        # Check the availability of the car park for entering and exiting functions
        display = "We would like to have your plate number for the processing.\n"
        display += "(The format should be as \"AB12 CDE\".)\n\n"
        display += "Please enter the plate number: "

        if stage == "enter" and self.avail_no > 0:
            return True, display
        elif stage == "exit" and self.avail_no != self.cap:
            return True, display
        else:
            if stage == "enter":
                return False, "Sorry, the car park is full now."
            elif stage == "exit":
                return False, "Sorry, there is no car parked in the car park."
            else:
                return False, "Sorry, please restart the program."

    def plt_check(self, plate_no=None, stage=None):
        """
        Check the format of the vehicle registration number:
        - the entry must be 8 characters long
        - the 1st, 2nd, 6th, 7th, 8th character must be alphabet
        - the 3rd, 4th character must be digital number
        - the 5th character must be a space
        In this program, the verification of customisable or forbidden plate numbers was not implemented.
        """
        if len(plate_no) != 8:
            display = "Sorry, the inputted plate number is not correct.\nPlease retry."
            return False, display

        else:
            str1, age, space, str2 = plate_no[:2], plate_no[2:4], plate_no[4], plate_no[5:]
            if str1.isalpha() and age.isdigit() and space.isspace() and str2.isalpha():
                if stage == "enter" and plate_no in self.parking_car:
                    display = "Sorry, the car is already parked in the car park.\nPlease retry."
                    return False, display
                elif stage == "exit" and plate_no not in self.parking_car:
                    display = "Sorry, we cannot find the car in our car park.\nPlease retry."
                    return False, display
                else:
                    return True, None
            else:
                display = "Sorry, the inputted plate number is not correct.\nPlease retry."
                return False, display

    def enter(self, plate_no):
        """
        Process the entering:
        - issuing the ticket number
        - allocating the parking space
        - recording the entry time
        - update the record to the temporary memory and save to the csv file
        """
        if plate_no in self.parked_car:
            ticket = int(self.parked_car[plate_no][3:6], 16)
            ticket = (format(datetime.now().year, "03x").upper() + format(ticket + 1, "03x").upper()
                      + plate_no[:4] + plate_no[5:])
        else:
            ticket = format(datetime.now().year, "03x").upper() + format(1, "03x") + plate_no[:4] + plate_no[5:]
        plt = plate_no
        space = random.choice(list(self.avail_space))
        entry_time = datetime.fromtimestamp(int(time.time()))
        index = len(self.record)
        update = [ticket, plt, space, entry_time, 'Parking...', 'Parking...']
        self.update(1, update, index)
        display = "Here is the detail of the parking:\n\n"
        display += "Ticket Number: %s\n" % ticket
        display += "Vehicle Registration Number: %s\n" % plt
        display += "Allocated Parking Space: %s\n" % space
        display += "Entry Time: %s\n\n" % entry_time
        display += "Remaining Parking %s: %d" % ("Spaces" if self.avail_no > 1 else "Space", self.avail_no)
        return display

    def exit(self, plate_no):
        """
        Process the exiting:
        - retrieving the parking record
        - recording the exit time
        - calculating the parking fee
        - update the record to the temporary memory and save to the csv file
        """
        ticket_no = self.parking_car[plate_no]
        ticket, plt, space, entry_time, exit_time, fee, index = self.ticket.get_info(ticket_no)
        exit_time = datetime.fromtimestamp(int(time.time()))
        difference = (datetime.strptime(str(exit_time), "%Y-%m-%d %H:%M:%S").timestamp() -
                      datetime.strptime(str(entry_time), "%Y-%m-%d %H:%M:%S").timestamp())
        fee = round(difference / 3600 * 2, 2)
        update = [ticket, plt, space, entry_time, exit_time, fee]
        self.update(2, update, index)
        display = "Thank you for choosing our car park.\n\n"
        display += "Here is the detail of the parking:\n"
        display += "Ticket Number: %s\n" % ticket
        display += "Vehicle Registration Number: %s\n" % plt
        display += "Allocated Parking Space: %s\n" % space
        display += "Entry Time: %s\n" % entry_time
        display += "Exit Time: %s\n" % exit_time
        display += "Parking Fee: £ %.2f  (£ 2.00 per hour)\n\n" % fee
        display += "Remaining Parking %s: %d" % ("Spaces" if self.avail_no > 1 else "Space", self.avail_no)
        return display

    def view(self):
        # Check the number of available parking spaces
        if self.avail_no > 0:
            display = ("There %s %d available parking %s now.\n\n" %
                       ("are" if self.avail_no > 1 else "is", self.avail_no,
                        "spaces" if self.avail_no > 1 else "space"))
            display += "The available parking %s\n\n" % "spaces are:" if self.avail_no > 1 else "space is:"
            lt = [int(no) for no in self.avail_space]
            for x in sorted(lt)[:-1]:
                display += "%s, " % str(x)
            display += "%s" % sorted(self.avail_space)[-1]
        else:
            display = "Sorry, there is no available parking space in the car park now."
        return display

    def query(self):
        # Ask for a ticket number for record query
        display = "Please enter the ticket number for the record query: "
        return display

    def search(self, ticket):
        # Return the parking record
        if self.ticket.find(ticket) is not None:
            ticket, plt, space, entry_time, exit_time, fee, index = self.ticket.get_info(ticket)
            display = "Here is the record of the parking:\n\n"
            display += "Ticket Number: %s\n" % ticket
            display += "Vehicle Registration Number: %s\n" % plt
            display += "Allocated Parking Space: %s\n" % space
            display += "Entry Time: %s\n" % entry_time
            display += "Exit Time: %s\n" % exit_time
            display += "Parking Fee: %s%s  %s" % ("£ " if fee != "Parking..." else "", fee,
                                                  "(£ 2.00 per hour)" if fee != "Parking..." else "")
            return True, display
        else:
            display = "Sorry, we cannot find the ticket in our record. Please retry."
            return False, display

    def update(self, stage=0, update=None, index=0):
        # Function to update the temporary memory of all the parking records
        if update is not None:
            ticket, plt, space, entry_time, exit_time, fee = update
            if stage == 1:
                self.record.append(update[:])
                self.avail_space.discard(space)
                self.avail_no = len(self.avail_space)
                update.append(index)
                self.ticket.insert(update)
                self.parked_car[plt] = ticket
                self.parking_car[plt] = ticket
            elif stage == 2:
                self.record[index] = update[:]
                self.avail_space.add(space)
                self.avail_no = len(self.avail_space)
                update.append(index)
                self.ticket.update(update)
                self.parking_car.pop(plt)
            self.ticket_list[ticket] = ticket, plt, space, entry_time, exit_time, fee, index
            self.save()

    def get_parking_car(self):
        # Return a list of parking car (for exit function in cmdUI and GUI)
        lt = sorted(self.parking_car.keys())
        lt.reverse()
        return lt

    def get_ticket(self):
        # Return a list of tickets issued (for query function in GUI)
        return self.ticket_list.keys()

    def save(self):
        # Call the function to update the CSV file
        write_file(self.file, self.record)


# Construct a class for the ticket numbers for building the BST
class Ticket:
    # Initiate the root and set all the related information
    def __init__(self, lt=None):
        if lt is None:
            ticket, reg_no, space, entry_time, exit_time, fee, index = None, None, None, None, None, None, None
        else:
            ticket, reg_no, space, entry_time, exit_time, fee, index = lt
        self.ticket = ticket
        self.reg_no = reg_no
        self.space = space
        self.entry = entry_time
        self.exit = exit_time
        self.fee = fee
        self.index = index
        self.left = None
        self.right = None

    # Insert a new ticket to the BST, and save the parking record to the node
    def insert(self, lt):
        ticket, reg_no, space, entry_time, exit_time, fee, index = lt
        if self.ticket:
            if ticket < self.ticket:
                if self.left is None:
                    self.left = Ticket(lt)
                else:
                    self.left.insert(lt)
            elif ticket > self.ticket:
                if self.right is None:
                    self.right = Ticket(lt)
                else:
                    self.right.insert(lt)
        else:
            self.ticket = ticket
            self.reg_no = reg_no
            self.space = space
            self.entry = entry_time
            self.exit = exit_time
            self.fee = fee
            self.index = index

    # Find the requested ticket's node in the BST
    def find(self, ticket):
        if ticket < self.ticket:
            if self.left is None:
                return None
            return self.left.find(ticket)
        elif ticket > self.ticket:
            if self.right is None:
                return None
            return self.right.find(ticket)
        else:
            return self

    # Update the information of the ticket's node after the car exited the car park
    def update(self, lt):
        ticket, reg_no, space, entry_time, exit_time, fee, index = lt
        car = self.find(ticket)
        car.ticket = ticket
        car.reg_no = reg_no
        car.space = space
        car.entry = entry_time
        car.exit = exit_time
        car.fee = fee
        car.index = index

    # Return the information of the ticket number
    def get_info(self, ticket):
        car = self.find(ticket)
        output = [car.ticket, car.reg_no, car.space, car.entry, car.exit, car.fee, car.index]
        return output


def read_file(file):
    # Read the CSV file
    if check_file(file):
        with open(file, "r") as f:
            lines = [row for row in csv.reader(f)]
        return lines


def check_file(file):
    # Check if the presence of the CSV file
    try:
        file = open(file, "r")
        file.close()
        return True

    except FileNotFoundError:
        print("Parking history can not be found in the directory.\nCreating a new one...\n")
        content = [["Parking History"], ["Ticket No.", "Vehicle Registration No.", "Parking Space", "Entry Time",
                                         "Exit Time", "Parking Fee (£)"]]
        create_file(file, content)
        return True

    except BaseException as e:
        print("\nError Type:", type(e).__name__, "\n")
        return False


def create_file(file, content):
    # Create a CSV file if there was no CSV file in the directory
    with open(file, "w", newline="") as f:
        csv.writer(f).writerows(content)


def write_file(file, content):
    # Write the parking record to the CSV file
    try:
        with open(file, "w", newline="") as f:
            csv.writer(f).writerows(content)
    except BaseException as e:
        print("\nError Type:", type(e).__name__)
        exit()


def sort_data(lt):
    """
    Sort the data from reading of the CSV file
    to optimise the initiation of the Class Carpark and the creation of the BST
    """
    record = lt[2:]
    if not record:
        return {}, {}, {}, set()
    ticket = {}
    parked_car = {}
    parking_car = {}
    occupied_space = set()
    count = 2
    for array in record:
        ticket[array[0]] = array[0], array[1], array[2], array[3], array[4], array[5], count
        parked_car[array[1]] = array[0]
        if array[4] == "Parking...":
            parking_car[array[1]] = array[0]
            occupied_space.add(array[2])
        count += 1
    return ticket, parked_car, parking_car, occupied_space
