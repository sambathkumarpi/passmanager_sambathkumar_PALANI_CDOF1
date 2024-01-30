import getpass
import hashlib
import json
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

# Save encrypted data to a file
def save_data(filename, data):
    with open(filename, 'wb') as file:
        file.write(data)

# Load encrypted data from a file
def load_data(filename):
    with open(filename, 'rb') as file:
        return file.read()

# Main function to add or retrieve passwords
def main():
    # Print the welcome message
    print("█░█░█ █▀▀ █░░ █▀▀ █▀█ █▀▄▀█ █▀▀   ▀█▀ █▀█   █▀▄▀█ █▄█   █░█ ▄▀█ █░█ █░░ ▀█▀")
    print("▀▄▀▄▀ ██▄ █▄▄ █▄▄ █▄█ █░▀░█ ██▄   ░█░ █▄█   █░▀░█ ░█░   ▀▄▀ █▀█ █▄█ █▄▄ ░█░")
    print()  # Empty line for space
    
    key = generate_key()
    master_password = getpass.getpass("Enter your master password: ")
    hashed_master_password = hash_password(master_password)

    # Check if a data file exists, if not, create an empty dictionary
    try:
        encrypted_data = load_data('passwords.dat')
        decrypted_data = decrypt_data(key, encrypted_data)
        passwords = json.loads(decrypted_data)
    except (FileNotFoundError, json.JSONDecodeError):
        passwords = {}

    # Menu loop
    while True:
        print("\n1. Add Password")
        print("2. Retrieve Password")
        print("3. Exit")
        choice = input("Enter your choice: ")

        if choice == '1':
            website = input("Enter the website: ")
            username = input("Enter the username: ")
            password = getpass.getpass("Enter the password: ")

            # Encrypt and store the password
            passwords[website] = {
                'username': username,
                'password': encrypt_data(key, password)
            }
            print("Password added successfully!")

        elif choice == '2':
            website = input("Enter the website: ")
            if website in passwords:
                username = passwords[website]['username']
                decrypted_password = decrypt_data(key, passwords[website]['password'])
                print(f"\nUsername: {username}")
                print(f"Password: {decrypted_password}")
            else:
                print("Password not found!")

        elif choice == '3':
            # Save the encrypted data and exit
            encrypted_data = encrypt_data(key, json.dumps(passwords))
            save_data('passwords.dat', encrypted_data)
            print("Password manager closed.")
            break

        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
