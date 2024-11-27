# Imports and Setup
import tkinter as tk  # Import tkinter for GUI functionality
from tkinter import messagebox  # Import messagebox for displaying pop-up messages
from datetime import datetime  # Import datetime for recording expense dates
import json  # Import JSON for storing and loading user and expense data
import os  # Import OS for directory and file operations
import hashlib  # Import hashlib for password hashing




# Directory and File Setup
USER_FILES_DIR = "user_expenses"  # Directory where user expense files are stored
USER_CREDENTIALS_FILE = "users.json"  # File to store usernames and hashed passwords
os.makedirs(USER_FILES_DIR, exist_ok=True)  # Create the user files directory if it doesn't exist

if not os.path.exists(USER_CREDENTIALS_FILE):  # Check if the credentials file exists
    with open(USER_CREDENTIALS_FILE, "w") as file:  # If not, create an empty JSON file
        json.dump({}, file)




# Utility Functions
def hash_password(password):  # Function to hash a password using SHA-256
    return hashlib.sha256(password.encode()).hexdigest()  # Return the hashed password

def get_user_file(username):  # Function to get the file path for a specific user's expense data
    return os.path.join(USER_FILES_DIR, f"{username}.json")  # Return the file path as "<directory>/<username>.json"

def load_user_data(username):  # Function to load a user's expense data
    global expenses_data  # Use a global variable to store the loaded data
    user_file = get_user_file(username)  # Get the file path for the user's data
    try:
        with open(user_file, "r") as file:  # Try to open the user's expense file
            expenses_data = json.load(file)  # Load the JSON data into the global variable
    except (FileNotFoundError, json.JSONDecodeError):  # If the file doesn't exist or is corrupted
        expenses_data = []  # Initialize an empty list for expenses

def save_user_data(username):  # Function to save a user's expense data
    user_file = get_user_file(username)  # Get the file path for the user's data
    with open(user_file, "w") as file:  # Open the file for writing
        json.dump(expenses_data, file)  # Save the global expense data to the file in JSON format

def load_user_credentials():  # Function to load all user credentials
    with open(USER_CREDENTIALS_FILE, "r") as file:  # Open the credentials file for reading
        return json.load(file)  # Load and return the credentials as a dictionary

def save_user_credentials(credentials):  # Function to save all user credentials
    with open(USER_CREDENTIALS_FILE, "w") as file:  # Open the credentials file for writing
        json.dump(credentials, file)  # Save the credentials dictionary in JSON format




# Login Window Setup
root = tk.Tk()  # Create the main Tkinter window
root.title("BudgetApp Login")  # Set the title of the window
root.geometry("1920x1080")  # Set the dimensions of the window
font_settings = ("Helvetica", 14)  # Define a consistent font style for the GUI elements

label_username = tk.Label(root, text="Username:", bg="white", font=font_settings)  # Label for username input
label_username.pack(pady=5)  # Add vertical padding around the label
entry_username = tk.Entry(root, font=font_settings)  # Text entry box for the username
entry_username.pack(pady=5)  # Add vertical padding around the entry box

label_password = tk.Label(root, text="Password:", bg="white", font=font_settings)  # Label for password input
label_password.pack(pady=5)  # Add vertical padding around the label
entry_password = tk.Entry(root, show="*", font=font_settings)  # Password entry box (masked with asterisks)
entry_password.pack(pady=5)  # Add vertical padding around the entry box

login_button = tk.Button(root, text="Login", font=font_settings)  # Button to initiate the login process
login_button.pack(pady=20)  # Add vertical padding around the button




# Login and User Management
def login():  # Function to handle login or registration
    username = entry_username.get().strip().upper()  # Convert username to uppercase
    password = entry_password.get().strip()  # Get and strip leading/trailing whitespace from the password

    if username and password:  # Check if both username and password are provided
        credentials = load_user_credentials()  # Load the user credentials

        if username in credentials:  # Check if the username exists
            if credentials[username] == hash_password(password):  # Validate the password
                load_user_data(username)  # Load the user's expense data
                open_budget_tracker(username)  # Open the budget tracker interface
            else:
                messagebox.showerror("Login Failed", "Invalid password.")  # Show an error for incorrect password
        else:  # If the username does not exist
            if messagebox.askyesno("Register New User", f"User '{username}' does not exist. Register as a new user?"):
                credentials[username] = hash_password(password)  # Register the new user with a hashed password
                save_user_credentials(credentials)  # Save the updated credentials
                expenses_data = []  # Initialize an empty expense list for the new user
                save_user_data(username)  # Save the empty expense data for the new user
                open_budget_tracker(username)  # Open the budget tracker interface
    else:
        messagebox.showerror("Login Failed", "Please enter both username and password.")  # Show an error for missing input




# Budget Tracker Interface
def open_budget_tracker(username):  # Function to display the budget tracker interface
    new_window = tk.Toplevel(root)  # Create a new Tkinter window
    new_window.title(f"BudgetApp - {username}")  # Set the title of the new window
    new_window.geometry("1920x1080")  # Set the dimensions of the new window

    welcome_label = tk.Label(new_window, text=f"Welcome, {username}!", font=("Helvetica", 18), bg="white")  # Welcome message
    welcome_label.pack(pady=20)  # Add vertical padding around the welcome message

    budget_frame = tk.Frame(new_window, bg="white")  # Create a frame for budget tracker elements
    budget_frame.pack(pady=20)  # Add vertical padding around the frame

    label_category = tk.Label(budget_frame, text="Expense Category:", font=font_settings, bg="white")  # Label for category
    label_category.grid(row=0, column=0, padx=10, pady=5, sticky="w")  # Place the label in the grid layout
    entry_category = tk.Entry(budget_frame, font=font_settings)  # Text entry box for category
    entry_category.grid(row=0, column=1, padx=10, pady=5)  # Place the entry box in the grid layout

    label_amount = tk.Label(budget_frame, text="Amount Spent:", font=font_settings, bg="white")  # Label for amount
    label_amount.grid(row=1, column=0, padx=10, pady=5, sticky="w")  # Place the label in the grid layout
    entry_amount = tk.Entry(budget_frame, font=font_settings)  # Text entry box for amount
    entry_amount.grid(row=1, column=1, padx=10, pady=5)  # Place the entry box in the grid layout




    # Expense Management
    def add_expense():  # Function to add a new expense
        try:
            category = entry_category.get().strip().upper()  # Convert category to uppercase
            amount = float(entry_amount.get())  # Convert the entered amount to a float
            date = datetime.now().strftime("%Y-%m-%d at %I:%M %p")  # Get the current date and time
            expense_id = len(expenses_data) + 1  # Assign a unique ID to the expense

            expenses_data.append({"id": expense_id, "category": category, "amount": amount, "date": date})  # Add the expense
            entry_category.delete(0, tk.END)  # Clear the category entry field
            entry_amount.delete(0, tk.END)  # Clear the amount entry field
            entry_category.focus_set()  # Set focus back to the category field
            display_expenses()  # Refresh the displayed expenses
            save_user_data(username)  # Save the updated expense data
        except ValueError:  # Handle invalid amount input
            messagebox.showerror("Invalid Input", "Please enter a valid number for the amount.")
            

    def delete_expense(expense_id):  # Function to delete an expense by its ID
        global expenses_data
        expenses_data = [exp for exp in expenses_data if exp["id"] != expense_id]  # Remove the expense with the matching ID
        display_expenses()  # Refresh the displayed expenses
        save_user_data(username)  # Save the updated expense data

    def clear_all_expenses():  # Function to clear all expenses
        if messagebox.askyesno("Clear All Expenses", "Are you sure you want to clear all expense history?"):
            global expenses_data
            expenses_data = []  # Clear the expense list
            display_expenses()  # Refresh the displayed expenses
            save_user_data(username)  # Save the cleared expense data




    # Calculate and Display Total Expenses
    def view_total_expenses():  # Function to calculate and display total expenses by category
        total_expenses = {}  # Dictionary to store totals by category

        # Calculate totals by summing up amounts for each category
        for expense in expenses_data:
            category = expense["category"]
            amount = expense["amount"]
            if category in total_expenses:
                total_expenses[category] += amount
            else:
                total_expenses[category] = amount

        # Format the total expenses for display
        total_message = "\n".join([f"{category}: ${total:.2f}" for category, total in total_expenses.items()])
        
        # Show the total expenses in a message box
        messagebox.showinfo("Total Expenses", total_message if total_message else "No expenses to display.")




    # Display Expenses
    def display_expenses():  # Function to display the current expenses
        for widget in expenses_frame.winfo_children():  # Remove all existing widgets in the expense frame
            widget.destroy()

        for i, expense in enumerate(expenses_data):  # Iterate through the expenses
            expense_label = tk.Label(
                expenses_frame,
                text=f"{expense['category']}: ${expense['amount']:.2f} on {expense['date']}",
                font=font_settings,
                bg="white"
            )  # Create a label for each expense
            expense_label.grid(row=i, column=0, padx=10, pady=2, sticky="w")  # Place the label in the grid layout

            delete_button = tk.Button(
                expenses_frame,
                text="X",
                command=lambda id=expense["id"]: delete_expense(id),
                font=font_settings,
                bg="red",
                fg="white"
            )  # Create a delete button for each expense
            delete_button.grid(row=i, column=1, padx=10, pady=2)  # Place the button in the grid layout

    add_expense_button = tk.Button(budget_frame, text="Add Expense", command=add_expense, font=font_settings)  # Button to add an expense
    add_expense_button.grid(row=2, column=0, columnspan=2, pady=10)  # Place the button in the grid layout

    clear_all_expenses_button = tk.Button(
        budget_frame,
        text="Clear All Expenses",
        command=clear_all_expenses,
        font=font_settings,
        bg="red",
        fg="white"
    )  # Button to clear all expenses
    clear_all_expenses_button.grid(row=3, column=0, columnspan=2, pady=10)  # Place the button in the grid layout




    # Add "View Total Expenses" button
    view_total_expenses_button = tk.Button(
        budget_frame,
        text="View Total Expenses",
        command=view_total_expenses,
        font=font_settings
    )  # Button to view total expenses
    view_total_expenses_button.grid(row=4, column=0, columnspan=2, pady=10)  # Place the button in the grid layout

    expenses_frame = tk.Frame(new_window, bg="white")  # Create a frame for displaying expenses
    expenses_frame.pack(pady=20)  # Add vertical padding around the frame

    display_expenses()  # Display the current expenses

    root.withdraw()  # Hide the main login window




# Key Bindings
def enter_key(event):  # Function to trigger login on Enter key press
    login_button.invoke()

root.bind('<Return>', enter_key)  # Bind the Enter key to the `enter_key` function
login_button.config(command=login)  # Set the login button to call the `login` function



# main loop
root.mainloop()  # Start the Tkinter event loop
