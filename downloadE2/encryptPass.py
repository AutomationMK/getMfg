import os
from cryptography.fernet import Fernet
from getpass import getpass

data_folder = os.path.abspath("assets/password/")
password_binary_filename = "/pass.bin"
password_key_filename = "/pass.key"
user_binary_filename = "/user.bin"
user_key_filename = "/user.key"
url_binary_filename = "/url.bin"
url_key_filename = "/url.key"


def create_user():
    """Generate a user that will be encrypted
    all information will be saved to the data_folder location"""
    # Generate a key and instantiate a Fernet instance
    key = Fernet.generate_key()
    f = Fernet(key)
    # The password you want to encrypt
    user = input("Enter your username: ")
    # Encrypt the password (it must be encoded to bytes)
    encrypted_user = f.encrypt(user.encode())
    # Save the encrypted password to a file
    with open(data_folder + user_binary_filename, "wb") as file:
        file.write(encrypted_user)
    # Optionally, save the key securely as well!
    with open(data_folder + user_key_filename, "wb") as key_file:
        key_file.write(key)


def load_user() -> str:
    """Function to load the user name from the data_folder location"""
    # Load the encryption key (if stored separately)
    with open(data_folder + user_key_filename, "rb") as key_file:
        saved_key = key_file.read()
    # Recreate the Fernet object using the saved key
    f = Fernet(saved_key)
    # Read the encrypted password from file
    with open(data_folder + user_binary_filename, "rb") as file:
        encrypted_user = file.read()
    # Decrypt the password and decode it back to a string
    return f.decrypt(encrypted_user).decode()


def user(folder_location=data_folder):
    """Function to check if a user file exists in data_folder
    if it does not then it prompts the user to create a user name"""
    if os.path.exists(folder_location + user_binary_filename):
        user = load_user()
    else:
        create_user()
        user = load_user()
    return user


def create_password():
    """Generate a password that will be encrypted
    all information will be saved to the data_folder location"""
    # Generate a key and instantiate a Fernet instance
    key = Fernet.generate_key()
    f = Fernet(key)
    # The password you want to encrypt
    password = getpass("Enter a password: ")
    # Encrypt the password (it must be encoded to bytes)
    encrypted_password = f.encrypt(password.encode())
    # Save the encrypted password to a file
    with open(data_folder + password_binary_filename, "wb") as file:
        file.write(encrypted_password)
    # Optionally, save the key securely as well!
    with open(data_folder + password_key_filename, "wb") as key_file:
        key_file.write(key)


def load_password() -> str:
    """Function to load the password from the data_folder location"""
    # Load the encryption key (if stored separately)
    with open(data_folder + password_key_filename, "rb") as key_file:
        saved_key = key_file.read()
    # Recreate the Fernet object using the saved key
    f = Fernet(saved_key)
    # Read the encrypted password from file
    with open(data_folder + password_binary_filename, "rb") as file:
        encrypted_password = file.read()
    # Decrypt the password and decode it back to a string
    return f.decrypt(encrypted_password).decode()


def password(folder_location=data_folder):
    """Function to check if a password file exists in data_folder
    if it does not then it prompts the user to create a password"""
    if os.path.exists(folder_location + password_binary_filename):
        password = load_password()
    else:
        create_password()
        password = load_password()
    return password


def create_url():
    """Generate a url that will be encrypted
    all information will be saved to the data_folder location"""
    # Generate a key and instantiate a Fernet instance
    key = Fernet.generate_key()
    f = Fernet(key)
    # The password you want to encrypt
    url = input("Enter your exact E2 URL: ")
    # Encrypt the password (it must be encoded to bytes)
    encrypted_url = f.encrypt(url.encode())
    # Save the encrypted password to a file
    with open(data_folder + url_binary_filename, "wb") as file:
        file.write(encrypted_url)
    # Optionally, save the key securely as well!
    with open(data_folder + url_key_filename, "wb") as key_file:
        key_file.write(key)


def load_url() -> str:
    """Function to load the url name from the data_folder location"""
    # Load the encryption key (if stored separately)
    with open(data_folder + url_key_filename, "rb") as key_file:
        saved_key = key_file.read()
    # Recreate the Fernet object using the saved key
    f = Fernet(saved_key)
    # Read the encrypted password from file
    with open(data_folder + url_binary_filename, "rb") as file:
        encrypted_url = file.read()
    # Decrypt the password and decode it back to a string
    return f.decrypt(encrypted_url).decode()


def url(folder_location=data_folder):
    """Function to check if a url file exists in data_folder
    if it does not then it prompts the user to enter a url"""
    if os.path.exists(folder_location + url_binary_filename):
        url = load_url()
    else:
        create_url()
        url = load_url()
    return url
