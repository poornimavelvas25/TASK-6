import secrets
import string
import math
import re

# Common weak passwords list
COMMON_PASSWORDS = [
    "123456", "password", "123456789", "admin",
    "qwerty", "abc123", "111111", "123123"
]

# ---- PASSWORD GENERATOR ----
def generate_password(length, use_upper, use_numbers, use_symbols):
    characters = string.ascii_lowercase
    
    if use_upper:
        characters += string.ascii_uppercase
    if use_numbers:
        characters += string.digits
    if use_symbols:
        characters += string.punctuation

    password = ''.join(secrets.choice(characters) for _ in range(length))
    return password, len(characters)


# ---- STRENGTH CHECKER ----
def check_strength(password):
    score = 0
    feedback = []

    if len(password) >= 12:
        score += 1
    else:
        feedback.append("Increase length to at least 12 characters.")

    if re.search(r"[A-Z]", password):
        score += 1
    else:
        feedback.append("Add uppercase letters.")

    if re.search(r"[0-9]", password):
        score += 1
    else:
        feedback.append("Include numbers.")

    if re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        score += 1
    else:
        feedback.append("Include special symbols.")

    if password not in COMMON_PASSWORDS:
        score += 1
    else:
        feedback.append("This is a commonly used password!")

    return score, feedback


# ---- ENTROPY CALCULATION ----
def calculate_entropy(length, charset_size):
    if charset_size <= 0:
        return 0
    return length * math.log2(charset_size)


# ---- CRACK TIME ESTIMATION ----
def estimate_crack_time(entropy):
    if entropy <= 0:
        return "Instantly"
    
    guesses_per_second = 1_000_000_000  # 1 billion guesses/sec
    total_combinations = 2 ** entropy
    seconds = total_combinations / guesses_per_second

    if seconds < 60:
        return f"{round(seconds, 2)} seconds"
    elif seconds < 3600:
        return f"{round(seconds/60, 2)} minutes"
    elif seconds < 86400:
        return f"{round(seconds/3600, 2)} hours"
    elif seconds < 31536000:
        return f"{round(seconds/86400, 2)} days"
    else:
        return f"{round(seconds/31536000, 2)} years"


# ---- MAIN PROGRAM ----
print("=== Advanced Secure Password Generator ===")

try:
    length = int(input("Enter password length (min 8): "))
except ValueError:
    print("Error: Please enter a valid number.")
    exit()

use_upper = input("Include uppercase? (y/n): ").lower() == 'y'
use_numbers = input("Include numbers? (y/n): ").lower() == 'y'
use_symbols = input("Include symbols? (y/n): ").lower() == 'y'

if length < 8:
    print("Password must be at least 8 characters.")
else:
    password, charset_size = generate_password(length, use_upper, use_numbers, use_symbols)
    
    score, feedback = check_strength(password)
    entropy = calculate_entropy(length, charset_size)
    crack_time = estimate_crack_time(entropy)

    print("\nGenerated Password:", password)
    print("Strength Score (0-5):", score)
    print("Estimated Crack Time:", crack_time)
    print("Entropy:", round(entropy, 2), "bits")

    if feedback:
        print("\nFeedback:")
        for tip in feedback:
            print("-", tip)
    else:
        print("\nExcellent password! No improvements needed.")