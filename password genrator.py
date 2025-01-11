
import random
import string
import tkinter as tk
from tkinter import messagebox

# password generation function
def generate_password():
    """Generate a random password based on user input."""
    try:
        # Get the password length from the user
        length = int(length_entry.get())
        
        #  the password length is at least 4
        if length < 4:
            messagebox.showerror("Error", "Password length should be at least 4 characters.")
            return

        # Character sets for password generation
        lower = string.ascii_lowercase
        upper = string.ascii_uppercase
        digits = string.digits
        symbols = string.punctuation

        
        all_characters = lower + upper + digits + symbols

        password = (
            random.choice(lower) +
            random.choice(upper) +
            random.choice(digits) +
            random.choice(symbols)
        )

        # Add random character to meet the desired length
        password += ''.join(random.choices(all_characters, k=length - 4))

        # Shuffle the password for randomness
        password = ''.join(random.sample(password, len(password)))

        # Display the generated password
        password_entry.delete(0, tk.END)  
        password_entry.insert(0, password)  

    except ValueError:
        
        messagebox.showerror("Error", "Please enter a valid number for the password length.")

# Create the main  window
root = tk.Tk()
root.title("Password Generator") 


tk.Label(root, text="Password Length:").grid(row=0, column=0, padx=10, pady=10)  
length_entry = tk.Entry(root)  
length_entry.grid(row=0, column=1, padx=10, pady=10)


generate_button = tk.Button(root, text="Generate Password", command=generate_password)
generate_button.grid(row=1, column=0, columnspan=2, pady=10)


tk.Label(root, text="Generated Password:").grid(row=2, column=0, padx=10, pady=10)  
password_entry = tk.Entry(root, width=30)  
password_entry.grid(row=2, column=1, padx=10, pady=10)


root.mainloop()
