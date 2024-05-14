import random
import string

def generate_password(length=12):
    """Generate a strong password."""
    # Define character sets for different types of characters
    uppercase_letters = string.ascii_uppercase
    lowercase_letters = string.ascii_lowercase
    digits = string.digits
    special_characters = string.punctuation

    # Combine all character sets
    all_characters = uppercase_letters + lowercase_letters + digits + special_characters

    # Ensure at least one character from each set
    password = random.choice(uppercase_letters)
    password += random.choice(lowercase_letters)
    password += random.choice(digits)
    password += random.choice(special_characters)

    # Fill the rest of the password length with random characters
    for _ in range(length - 4):
        password += random.choice(all_characters)

    # Shuffle the password to make it harder to predict
    password_list = list(password)
    random.shuffle(password_list)
    password = ''.join(password_list)

    return password

if __name__ == "__main__":
    print(generate_password())
