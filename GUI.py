"""
This is the script of the graphical user interface (GUI). It basically provides an interface for the user
to interact with. After receiving the input from the user, it will call the functions in the Carpark script and
display the result from the script.
"""

import tkinter as tk  # Import the tkinter module for building the GUI
import Carpark as Cp  # Import the Carpark module for all the processing functions


# Construct the GUI class
class GUI:

    def __init__(self):
        # Initiate the class with all the settings:
        self.root = tk.Tk()             # Set the root window
        self.car_park = Cp.Carpark()    # Initiate the class Carpark in the Carpark script
        self.sec = 2000                 # The delay time after displaying error messages
        self.retry = None               # A variable for indicating a faulty input from the user
        self.click = 0                  # A variable the store the number of user clicking the entry box
        # The root window of the GUI
        self.root.title("Car Park Simulator")
        self.root.geometry("1060x600")
        # The title on the top of root window
        self.title = tk.Label(self.root, text="Car Park Simulator", font=('Arial', 20))
        self.title.pack(padx=10, pady=20)
        # 5 rows x 3 columns frame on the root window
        self.frame = tk.Frame(self.root)
        self.frame.rowconfigure(0, weight=1)
        self.frame.rowconfigure(1, weight=1)
        self.frame.rowconfigure(2, weight=1)
        self.frame.rowconfigure(3, weight=1)
        self.frame.rowconfigure(4, weight=1)
        self.frame.columnconfigure(0, weight=1)
        self.frame.columnconfigure(1, weight=60)
        self.frame.columnconfigure(2, weight=60)
        self.frame.pack(padx=10, pady=30, expand=True, fill='both')
        # The 5 buttons for the 5 main functions of this car park simulator
        self.btn1 = tk.Button(self.frame, text="Enter the car park", font=('Arial', 18), width=23,
                              command=lambda: self.btn_click(self.btn1))
        self.btn1.grid(row=0, column=0, padx=10, pady=10)
        self.btn2 = tk.Button(self.frame, text="Exit the car park", font=('Arial', 18), width=23,
                              command=lambda: self.btn_click(self.btn2))
        self.btn2.grid(row=1, column=0, padx=10, pady=10)
        self.btn3 = tk.Button(self.frame, text="View available parking space", font=('Arial', 18), width=23,
                              command=lambda: self.btn_click(self.btn3))
        self.btn3.grid(row=2, column=0, padx=10, pady=10)
        self.btn4 = tk.Button(self.frame, text="Check parking record", font=('Arial', 18), width=23,
                              command=lambda: self.btn_click(self.btn4))
        self.btn4.grid(row=3, column=0, padx=10, pady=10)
        self.btn5 = tk.Button(self.frame, text="Quit", font=('Arial', 18), width=23,
                              command=lambda: self.btn_click(self.btn5))
        self.btn5.grid(row=4, column=0, padx=10, pady=10)
        # The area for displaying content for the functions (enter, exit, view available spaces, record query)
        self.win = tk.Label(self.frame, bg='light grey', width=80, height=50)
        self.win.grid(row=0, column=1, rowspan=5, columnspan=2, padx=5, sticky='nsew')
        # The initiation of all the components used in the script
        self.text = tk.Label(self.frame)
        self.entry = tk.Entry(self.frame)
        self.ent_btn = tk.Button(self.frame)
        self.cnl_btn = tk.Button(self.frame)
        self.bk_btn = tk.Button(self.frame)
        self.listbox = tk.Listbox(self.frame)
        self.scroll = tk.Scrollbar(self.frame)
        self.home()  # Create the components on menu page of the GUI

    def create_text(self, r):
        # Create the textbox for displaying messages
        self.text = tk.Label(self.frame, bg='light grey', font=('Arial', 18), text="")
        self.text.grid(row=r, column=1, rowspan=3, columnspan=2, padx=10, pady=10, sticky='nsew')

    def create_entry(self, stage=None):
        # Create the entry box for user to entering plate/ticket number
        self.entry = tk.Entry(self.frame, width=16, font=('Arial', 24))
        if stage == "enter" or stage == "exit":
            self.entry.insert(0, 'AB12 CDE')
        elif stage == "query":
            self.entry.insert(0, '7E7001AB12CDE')
        self.entry.grid(row=2, column=1, rowspan=1, columnspan=2, padx=10, pady=10)
        self.entry.bind("<FocusIn>", self.clear_entry)
        self.click = 0

    def clear_entry(self, event=None):
        # Clear the content of the entry box when the user click on it
        if self.click == 0:
            self.entry.delete(0, tk.END)
        self.click = 1

    def create_ent_btn(self, stage=None):
        # Create an enter button
        self.ent_btn = tk.Button(self.frame, text="Enter", font=('Arial', 18), width=20,
                                 command=lambda: self.ent_btn_click(stage))
        self.ent_btn.grid(row=3, column=1, rowspan=1, padx=50, pady=10)
        if stage == "enter":
            self.ent_btn.grid_configure(columnspan=2, sticky='s')
        elif stage == "exit":
            self.ent_btn.grid_configure(column=2, sticky='se')
        elif stage == "query":
            self.ent_btn.grid_configure(column=2, sticky='se')

    def create_cnl_btn(self, stage=None):
        # Create a cancel button
        self.cnl_btn = tk.Button(self.frame, text="Cancel", font=('Arial', 18), width=20,
                                 command=lambda: self.btn_click())
        self.cnl_btn.grid(row=4, column=1, rowspan=1, padx=50, pady=10, sticky='n')
        if stage == "enter":
            self.cnl_btn.grid_configure(columnspan=2, sticky='n')
        elif stage == "exit":
            self.cnl_btn.grid_configure(column=2, sticky='ne')
        elif stage == "query":
            self.cnl_btn.grid_configure(column=2, sticky='ne')

    def create_bk_btn(self):
        # Create a back to menu page button
        self.bk_btn = tk.Button(self.frame, text="Back", font=('Arial', 18), width=10,
                                command=lambda: self.btn_click())
        self.bk_btn.grid(row=4, column=1, rowspan=1, columnspan=2, padx=10, pady=10, sticky='n')

    def create_lb(self, stage=None):
        # Create a listbox in the exit/record query page
        self.listbox = tk.Listbox(self.frame, font=('Arial', 14), width=30, height=8)
        self.listbox.grid(row=3, column=1, rowspan=2, padx=10, pady=10, sticky='nsew')
        self.scroll = tk.Scrollbar(self.frame, command=self.listbox.yview, orient=tk.VERTICAL)
        self.scroll.grid(row=3, column=1, rowspan=2, pady=10, sticky='nse')
        self.listbox.config(yscrollcommand=self.scroll.set)
        if stage == "exit":
            lt = self.car_park.get_parking_car()
        elif stage == "query":
            lt = self.car_park.get_ticket()
        else:
            lt = []
        for item in lt:
            self.listbox.insert(0, item)
        self.listbox.bind('<ButtonRelease-1>', self.get_item)

    def get_item(self, event=None):
        # Get selected text in the listbox and display in entry box
        index = self.listbox.curselection()[0]
        sel_text = self.listbox.get(index)
        self.click = 0
        self.clear_entry()
        self.entry.insert(0, sel_text)

    def btn_click(self, button=None):
        # Function after the main function buttons being clicked
        self.clear()
        if self.retry == "enter":
            button = self.btn1
        elif self.retry == "exit":
            button = self.btn2
        elif self.retry == "query":
            button = self.btn4
        self.retry = None
        buttons = {self.btn1, self.btn2, self.btn3, self.btn4, self.btn5}
        if button:
            button.config(bg='dark grey')
            for btn in buttons:
                btn.config(state="disabled")
        else:
            for btn in buttons:
                btn.config(state="normal", bg='SystemButtonFace')
        if button == self.btn1:
            self.enter_exit("enter")
        elif button == self.btn2:
            self.enter_exit("exit")
        elif button == self.btn3:
            self.view()
        elif button == self.btn4:
            self.query()
        elif button == self.btn5:
            self.quit()
        else:
            self.home()

    def home(self):
        # The components on the menu page
        self.create_text(1)
        self.text.config(text="Welcome to the car park!\n"
                              "Please select the corresponding action button.")
        self.text.grid(row=1, column=1, rowspan=2, padx=10, pady=10, sticky='nsew')

    def enter_exit(self, stage="enter"):
        # The components on the enter/exit page
        self.create_text(0)
        check, display = self.car_park.avail_check(stage)
        self.text.config(text=display)
        if check is False:
            self.root.after(self.sec, self.btn_click)
        else:
            self.create_entry(stage)
            self.create_ent_btn(stage)
            self.create_cnl_btn(stage)
            if stage == "exit":
                self.create_lb(stage)

    def view(self):
        # The components on the viewing available parking space page
        display = self.car_park.view()
        self.create_text(0)
        self.create_bk_btn()
        self.text.config(text=display)

    def query(self):
        # The components on the record query page
        stage = "query"
        self.create_text(0)
        display = self.car_park.query()
        self.create_entry(stage)
        self.create_lb(stage)
        self.create_ent_btn(stage)
        self.create_cnl_btn(stage)
        self.text.config(text=display)

    def quit(self):
        # The components on the quiting page
        self.create_text(1)
        self.text.config(text="We hope to see you soon again.\nHave a nice day. Goodbye!")
        self.root.after(self.sec, self.root.destroy)

    def clear(self):
        # Clear the area for the next main function
        self.text.destroy()
        self.entry.destroy()
        self.ent_btn.destroy()
        self.cnl_btn.destroy()
        self.bk_btn.destroy()
        self.listbox.destroy()
        self.scroll.destroy()

    def ent_btn_click(self, stage=None):
        # Process the input from the user and display accordingly
        plt_no = self.entry.get().upper()
        if stage == "enter":
            check, display = self.car_park.plt_check(plt_no, stage)
        elif stage == "exit":
            check, display = self.car_park.plt_check(plt_no, stage)
        elif stage == "query":
            check, display = self.car_park.search(plt_no)
        else:
            check, display = None, None
        self.clear()
        self.create_text(0)
        if check is False:
            self.text.config(text=display)
            self.retry = stage
            self.root.after(self.sec, self.btn_click)
        else:
            if stage == "enter":
                display = self.car_park.enter(plt_no)
                self.create_bk_btn()
                self.text.grid_configure(rowspan=3)
            elif stage == "exit":
                display = self.car_park.exit(plt_no)
                self.create_bk_btn()
                self.text.grid_configure(rowspan=4)
            elif stage == "query":
                self.create_bk_btn()
                self.text.grid_configure(rowspan=3)
            self.text.config(text=display)


window = GUI()  # Initiate the class GUI

# The main loop of the program and react when an error arise
try:
    window.root.mainloop()
except BaseException as e:
    print("\nError Type:", type(e).__name__)
    window.btn_click(window.btn5)
