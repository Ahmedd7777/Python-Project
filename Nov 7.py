# Import tkinter module for GUI elements
import tkinter as tk
# Import messagebox for showing message dialogs in tkinter
from tkinter import messagebox
# Import Image and ImageTk from PIL for handling images
from PIL import Image, ImageTk
# Import sqlite3 for database operations
import sqlite3
# Import datetime for working with dates and times
from datetime import datetime

# Create the main application window (the login window)
root = tk.Tk()
root.title("BudgetApp Login")  # Set the title of the window
root.geometry("1920x1080")  # Set the window size

# Load and resize the background image to fit the window dimensions
image_path = r"C:\Desktop\Classes\Python 1\Python Project 1\5.jpg"  # Define the image path
image = Image.open(image_path)  # Open the image file
image = image.resize((1920, 1080), Image.LANCZOS)  # Resize the image to window dimensions
background_image = ImageTk.PhotoImage(image)  # Convert image to PhotoImage for tkinter

# Create a label with the background image for the main window
background_label = tk.Label(root, image=background_image)  # Label with the background image
background_label.place(x=0, y=0, relwidth=1, relheight=1)  # Position label to cover entire window

# Define a larger font size for labels and entries
font_settings = ("Helvetica", 14)  # Font settings for consistency

# Create and place the username label and entry field
label_username = tk.Label(root, text="Username:", bg="white", font=font_settings)  # Label for "Username"
label_username.pack(pady=5)  # Place with padding
entry_username = tk.Entry(root, font=font_settings)  # Entry for username input
entry_username.pack(pady=5)  # Place with padding

# Create and place the password label and entry field
label_password = tk.Label(root, text="Password:", bg="white", font=font_settings)  # Label for "Password"
label_password.pack(pady=5)  # Place with padding
entry_password = tk.Entry(root, show="*", font=font_settings)  # Entry for password input with hidden characters
entry_password.pack(pady=5)  # Place with padding

# Connect to SQLite database (or create it if it doesn't exist)
conn = sqlite3.connect("budget_tracker.db")  # Connect to the database file
cursor = conn.cursor()  # Create a cursor for database operations

# Create a table for expenses if it doesn't exist
cursor.execute('''
    CREATE TABLE IF NOT EXISTS expenses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT,
        category TEXT,
        amount REAL,
        date TEXT
    )
''')
conn.commit()  # Save the changes to the database

# Define the login function to check credentials and open a new window if login is successful
def login():
    username = entry_username.get()  # Get entered username
    password = entry_password.get()  # Get entered password

    # Check if both username and password fields are empty for demonstration purposes
    if username == "" and password == "":
        new_window = tk.Toplevel(root)  # Create a new window on successful login
        new_window.title("BudgetApp")  # Set title of new window
        new_window.geometry("1920x1080")  # Set window size

        # Set the same background image in the new window
        background_label_new = tk.Label(new_window, image=background_image)  # Label with background image
        background_label_new.place(x=0, y=0, relwidth=1, relheight=1)  # Position label to cover entire window

        # Add a welcome message with a larger font
        welcome_label = tk.Label(new_window, text="Welcome to the Budget Tracker", font=("Helvetica", 18), bg="white")
        welcome_label.pack(pady=20)  # Place with padding

        # Create the budget tracker section
        budget_frame = tk.Frame(new_window, bg="white")  # Frame for budget entry widgets
        budget_frame.pack(pady=20)  # Place with padding

        # Create and place labels and entry fields for expense tracking
        label_category = tk.Label(budget_frame, text="Expense Category:", font=font_settings, bg="white")  # Label for category
        label_category.grid(row=0, column=0, padx=10, pady=5, sticky="w")  # Position in grid
        entry_category = tk.Entry(budget_frame, font=font_settings)  # Entry for category input
        entry_category.grid(row=0, column=1, padx=10, pady=5)  # Position in grid

        label_amount = tk.Label(budget_frame, text="Amount Spent:", font=font_settings, bg="white")  # Label for amount
        label_amount.grid(row=1, column=0, padx=10, pady=5, sticky="w")  # Position in grid
        entry_amount = tk.Entry(budget_frame, font=font_settings)  # Entry for amount input
        entry_amount.grid(row=1, column=1, padx=10, pady=5)  # Position in grid

        # Function to add expense to the database
        def add_expense():
            try:
                category = entry_category.get()  # Get entered category
                amount = float(entry_amount.get())  # Get entered amount as float
                date = datetime.now().strftime("%Y-%m-%d at %I:%M %p")  # Format current date and time

                # Insert the new expense into the database
                cursor.execute("INSERT INTO expenses (username, category, amount, date) VALUES (?, ?, ?, ?)",
                               (username, category, amount, date))
                conn.commit()  # Save the changes to the database

                # Clear the entry fields
                entry_category.delete(0, tk.END)  # Clear category entry field
                entry_amount.delete(0, tk.END)  # Clear amount entry field
                entry_category.focus_set()  # Focus back to category entry

                # Update the display of expenses
                display_expenses()
            except ValueError:
                messagebox.showerror("Invalid Input", "Please enter a valid number for the amount.")  # Show error if invalid input

        # Bind the Enter key to the add_expense function
        new_window.bind('<Return>', lambda event: add_expense())  # Bind Enter key to trigger add_expense

        # Function to delete an expense from the database
        def delete_expense(expense_id):
            cursor.execute("DELETE FROM expenses WHERE id = ?", (expense_id,))  # Delete expense by ID
            conn.commit()  # Save changes
            display_expenses()  # Update display of expenses

        # Function to clear all expenses from the database
        def clear_all_expenses():
            if messagebox.askyesno("Clear All Expenses", "Are you sure you want to clear all expense history?"):
                cursor.execute("DELETE FROM expenses WHERE username = ?", (username,))  # Clear expenses for the user
                conn.commit()  # Save changes
                display_expenses()  # Update display of expenses

        # Function to display all expenses for the user
        def display_expenses():
            for widget in expenses_frame.winfo_children():
                widget.destroy()  # Clear existing widgets in expenses_frame

            cursor.execute("SELECT id, category, amount, date FROM expenses WHERE username = ?", (username,))
            expenses = cursor.fetchall()  # Fetch all expenses for the user

            for i, (expense_id, category, amount, date) in enumerate(expenses):
                expense_label = tk.Label(expenses_frame, text=f"{category}: ${amount:.2f} on {date}", font=font_settings, bg="white")
                expense_label.grid(row=i, column=0, padx=10, pady=2, sticky="w")  # Display each expense

                delete_button = tk.Button(expenses_frame, text="X", command=lambda id=expense_id: delete_expense(id), font=font_settings, bg="red", fg="white")
                delete_button.grid(row=i, column=1, padx=10, pady=2)  # Button to delete specific expense

        # Function to view total expenses by category
        def view_total_expenses():
            total_expenses_window = tk.Toplevel(new_window)  # Create new window for total expenses
            total_expenses_window.title("Total Expenses")  # Set window title
            total_expenses_window.geometry("400x400")  # Set window size

            cursor.execute("SELECT category, SUM(amount) FROM expenses WHERE username = ? GROUP BY category", (username,))
            total_expenses = cursor.fetchall()  # Get total expenses grouped by category

            for i, (category, total) in enumerate(total_expenses):
                total_label = tk.Label(total_expenses_window, text=f"{category}: ${total:.2f}", font=font_settings, bg="white")
                total_label.pack(pady=5)  # Display each category's total expense

        # Create and place the add expense button
        add_expense_button = tk.Button(budget_frame, text="Add Expense", command=add_expense, font=font_settings)
        add_expense_button.grid(row=2, column=0, columnspan=2, pady=10)  # Button to add expense

        # Create and place the view total expenses button
        view_total_expenses_button = tk.Button(budget_frame, text="View Total Expenses", command=view_total_expenses, font=font_settings)
        view_total_expenses_button.grid(row=3, column=0, columnspan=2, pady=10)  # Button to view total expenses

        # Create and place the clear all expenses button
        clear_all_expenses_button = tk.Button(budget_frame, text="Clear All Expenses", command=clear_all_expenses, font=font_settings, bg="red", fg="white")
        clear_all_expenses_button.grid(row=4, column=0, columnspan=2, pady=10)  # Button to clear all expenses

        # Frame to display expenses
        expenses_frame = tk.Frame(new_window, bg="white")  # Frame to show expenses
        expenses_frame.pack(pady=20)  # Place with padding

        # Display expenses initially
        display_expenses()  # Show expenses when new window opens

        # Hide the main login window
        root.withdraw()  # Close login window after successful login
    else:
        messagebox.showerror("Login Failed", "Invalid username or password.")  # Show error on login failure

# Create and place the login button with larger font
login_button = tk.Button(root, text="Login", command=login, font=font_settings)
login_button.pack(pady=20)  # Place login button

# Bind the Enter key to invoke the login button
def enter_key(event):
    login_button.invoke()  # Trigger login button with Enter key

root.bind('<Return>', enter_key)  # Bind Enter key to the enter_key function

# Run the main event loop
root.mainloop()  # Start the tkinter event loop to display the window
