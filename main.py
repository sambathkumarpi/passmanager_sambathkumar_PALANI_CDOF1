import getpass
import hashlib
import json
import random
import string
from datetime import datetime, timedelta
from cryptography.fernet import Fernet

# Generate a key for encryption
def generate_key():
    return Fernet.generate_key()

# Encrypt data using Fernet symmetric encryption
def encrypt_data(key, data):
    cipher = Fernet(key)
    return cipher.encrypt(data.encode())

# Decrypt data using Fernet symmetric encryption
def decrypt_data(key, encrypted_data):
    cipher = Fernet(key)
    return cipher.decrypt(encrypted_data).decode()

# Hash the master password using SHA-256
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Save encrypted data to a JSON file
def save_data(filename, data):
    with open(filename, 'w') as file:
        json.dump(data, file, default=lambda x: x.decode() if isinstance(x, bytes) else x)

# Load encrypted data from a JSON file
def load_data(filename):
    try:
        with open(filename, 'r') as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

# Check password strength
def check_password_strength(password):
    # Define criteria for password strength
    length_requirement = 8
    has_uppercase = any(char.isupper() for char in password)
    has_lowercase = any(char.islower() for char in password)
    has_digit = any(char.isdigit() for char in password)
    has_special = any(char in string.punctuation for char in password)

    # Check if password meets the criteria
    if len(password) < length_requirement or not has_uppercase or not has_lowercase or not has_digit or not has_special:
        return False
    return True

# Generate a strong password
def generate_strong_password():
    length = 12
    characters = string.ascii_letters + string.digits + string.punctuation
    return ''.join(random.choice(characters) for i in range(length))

# Main function to add or retrieve passwords
def main():
    print("Welcome to Your Password Manager")
    print("---------------------------------")

    key = generate_key()
    master_password = getpass.getpass("Enter your master password: ")
    hashed_master_password = hash_password(master_password)

    # Check if a data file exists, if not, create an empty dictionary
    try:
        passwords = load_data('passwords.json')
    except FileNotFoundError:
        passwords = {}

    # Menu loop
    while True:
        print("\n1. Add Password")
        print("2. Retrieve Password")
        print("3. Generate Strong Password")
        print("4. Exit")
        choice = input("Enter your choice: ")

        if choice == '1':
            website = input("Enter the website: ")
            username = input("Enter the username: ")

            print("Password should contain at least 8 characters, including uppercase and lowercase letters, numbers, and special characters.")

            while True:
                password = getpass.getpass("Enter the password: ")

                if not check_password_strength(password):
                    print("Password does not meet the strength criteria. Please try again.")
                    continue

                break

            # Encrypt and store the password
            encrypted_password = encrypt_data(key, password)
            passwords[website] = {
                'username': username,
                'password': encrypted_password,
                'created_at': datetime.now().isoformat(),
                'expiry_date': (datetime.now() + timedelta(days=90)).isoformat()  # Password expires after 90 days
            }
            print("Password added successfully!")

        elif choice == '2':
            website = input("Enter the website: ")
            if website in passwords:
                username = passwords[website]['username']
                decrypted_password = decrypt_data(key, passwords[website]['password'])
                print(f"\nWebsite: {website}")
                print(f"Username: {username}")
                print(f"Password: {decrypted_password}")
                
                # Check if password is expired
                expiry_date = datetime.fromisoformat(passwords[website]['expiry_date'])
                if expiry_date < datetime.now():
                    print("Warning: Password has expired! Consider changing it.")
            else:
                print("Password not found!")

        elif choice == '3':
            new_password = generate_strong_password()
            print(f"Generated Strong Password: {new_password}")

        elif choice == '4':
            # Save the encrypted data and exit
            save_data('passwords.json', passwords)
            print("Password manager closed.")
            break

        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
