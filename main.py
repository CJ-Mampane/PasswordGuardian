import string
import getpass
import random
import json

def generate_password(length=12, use_upper=True, use_digits=True, use_symbols=True):
    characters = string.ascii_lowercase
    if use_upper:
        characters += string.ascii_uppercase
    if use_digits:
        characters += string.digits
    if use_symbols:
        characters += string.punctuation

    if not characters:
        raise ValueError("No character set selected!")

    password = ''.join(random.choice(characters) for _ in range(length))
    return password


def check_password_strength(password):
    strength = 0
    lower = upper = digit = space = special = 0

    for char in password:
        if char in string.ascii_lowercase:
            lower += 1
        elif char in string.ascii_uppercase:
            upper += 1
        elif char in string.digits:
            digit += 1
        elif char.isspace():
            space += 1
        else:
            special += 1

    if lower: strength += 1
    if upper: strength += 1
    if digit: strength += 1
    if special: strength += 1
    if len(password) >= 8:
        strength += 1
    if len(password) >= 12:
        strength += 1  # reward longer passwords

    if strength == 1:
        remark = "Even 'password' is feeling offended right now. Try something more secure."
    elif strength == 2:
        remark = "This password is like a lock on a diary - just upgrade to a vault."
    elif strength == 3:
        remark = "Not bad! But you can do better, please consider changing it."
    elif strength == 4:
        remark = "This password has good intentions but can get more muscle 💪"
    elif strength == 5:
        remark = "Very strong I guess but could be better "
    else:  # strength == 6
        remark = "Diamond-tier password, virtually uncrackable"
        
    print("\n                    PASSWORD ANALYSIS                     ")
    print(f"Lowercase: {lower}, Uppercase: {upper}, Digits: {digit}, Spaces: {space}, Special: {special}")
    print(f"Length: {len(password)}")
    print(f"Strength Score: {strength}/6")
    print(f"{remark}\n")

def save_password(password):
    save = input("Would you like to save this password locally? (y/n): ").lower()
    if save == 'y':
        entry_name = input("Enter a label for this password (e.g., 'Email', 'GitHub'): ")
        data = {entry_name: password}

        try:
            with open("saved_passwords.json", "r") as file:
                passwords = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            passwords = {}

        passwords.update(data)

        with open("saved_passwords.json", "w") as file:
            json.dump(passwords, file, indent=4)

        print("Password saved successfully!\n")
        
        
def main():
    while True:
        print("     PASSWORD TOOL     ")
        print("1. Generate a password")
        print("2. Check password strength")
        print("3. Exit")
        choice = input("Choose an option (1/2/3): ")
            
        if choice == '1':
            try:
                length = int(input("Enter password length: "))
            except ValueError:
                print("Invalid input! Using default length of 12.")
                length = 12

            print("\n(Press 'y' for yes - anything else will be treated as 'no')\n")

            use_uppercase = input("Include uppercase letters? (y/n): ").lower() == 'y'
            use_digits = input("Include digits? (y/n): ").lower() == 'y'
            use_symbols = input("Include symbols? (y/n): ").lower() == 'y'
            
            password = generate_password(length, use_uppercase, use_digits, use_symbols)
            print(f"\nGenerated password: {password}\n")
            
            check = input("Would you like to check the strength of this password? (y/n): ").lower()
            if check == 'y':
                check_password_strength(password)
                
            save_password(password)

        elif choice == '2':
            password = getpass.getpass("Enter your password to check: ")
            check_password_strength(password)

        elif choice == '3':
            print("Goodbye 👋")
            break

        else:
            print("Invalid choice, try again.\n")


if __name__ == "__main__":
    main()

