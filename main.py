import string
import getpass
import secrets
import json
from cryptography.fernet import Fernet

KEY_FILE = "key.key"
try:
    with open(KEY_FILE, "rb") as kf:
        key = kf.read()
except FileNotFoundError:
    key = Fernet.generate_key()
    with open(KEY_FILE, "wb") as kf:
        kf.write(key)

fernet = Fernet(key)

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

    password = ''.join(secrets.choice(characters) for _ in range(length))
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
        entry_name = input("Enter a label for this password (e.g., 'Email', 'GitHub', 'BlackBoard'): ")
        encrypted_password = fernet.encrypt(password.encode()).decode()
        data = {entry_name: encrypted_password}

        try:
            with open("saved_passwords.json", "r") as file:
                passwords = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            passwords = {}

        passwords.update(data)
        with open("saved_passwords.json", "w") as file:
            json.dump(passwords, file, indent=4)

        print("Password saved successfully!\n")
        
def retrieve_password():
    try:
        with open("saved_passwords.json", "r") as file:
            passwords = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        print("No saved passwords found.")
        return

    label = input("Enter the label of the password to retrieve: ")
    encrypted_password = passwords.get(label)
    if encrypted_password:
        decrypted_password = fernet.decrypt(encrypted_password.encode()).decode()
        print(f"Password for '{label}': {decrypted_password}\n")
    else:
        print("No password found with that label.\n")
        
def main():
    while True:
        print("     PASSWORD TOOL     ")
        print("1. Generate a password")
        print("2. Check password strength")
        print("3. Retrieve saved password")
        print("4. Exit")
        choice = input("Choose an option (1/2/3/4): ")

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
            retrieve_password()

        elif choice == '4':
            print("Goodbye 👋")
            break

        else:
            print("Invalid choice, try again.\n")

if __name__ == "__main__":
    main()

