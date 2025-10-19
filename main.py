import string
import getpass
import random

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
    if len(password) >= 12: strength += 1

    
    if strength == 1:
        remark = "Even 'password' is feeling offended right now. Try something more secure."
    elif strength == 2:
        remark = "This password is like a lock on a diary — just upgrade to a vault."
    elif strength == 3:
        remark = "Not bad! But you can do better, please consider changing it."
    elif strength == 4:
        remark = "This password has good intentions but needs more muscle 💪"
    else:
        remark = "A very strong password — hacker tears detected. 🥲"

    print("\n=== PASSWORD ANALYSIS ===")
    print(f"Lowercase: {lower}, Uppercase: {upper}, Digits: {digit}, Spaces: {space}, Special: {special}")
    print(f"Length: {len(password)}")
    print(f"Strength Score: {strength}/5")
    print(f"💬 {remark}\n")


def main():
    while True:
        print("=== PASSWORD TOOL ===")
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
            use_upper = input("Include uppercase letters? (y/n): ").lower() == 'y'
            use_digits = input("Include digits? (y/n): ").lower() == 'y'
            use_symbols = input("Include symbols? (y/n): ").lower() == 'y'
            password = generate_password(length, use_upper, use_digits, use_symbols)
            print(f"\nGenerated password: {password}\n")

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
