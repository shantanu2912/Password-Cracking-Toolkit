import itertools
import string
import time
from database import *

class PasswordCracker:
    def __init__(self, max_length, dictionary_file = r"C:\Users\shantanu sharma\Downloads\words.txt", fileid=None):
        # Initialize with a dictionary file and maximum brute-force length
        self.dictionary_file = dictionary_file
        self.max_length = int(max_length)
        self.dictionary = self.load_dictionary()
        self.symbols = string.ascii_letters + string.digits + string.punctuation
        self.fileId = fileid

    def load_dictionary(self):
        # Load words from dictionary file
        with open(self.dictionary_file, 'r') as file:
            dictionary = file.read().splitlines()
        return dictionary

    def crack_password(self, target_password):
        # Try dictionary attack with variations and brute-force combinations
        attempt_count = 0
        start_time = time.time()

        # Try each word from dictionary with combinations of symbols
        for word in self.dictionary:
            for length in range(self.max_length, self.max_length + 1):
                # Create variations of the word by appending/prepending combinations of symbols
                for combination in itertools.product(self.symbols, repeat=length):
                    prefix = ''.join(combination)
                    # Check with prefix + word
                    attempt_count += 1
                    attempt_password = prefix + word
                    if attempt_password == target_password:
                        # print(f"Password cracked: {attempt_password}")
                        # print(f"Total attempts: {attempt_count}")
                        # print(f"Time taken: {time.time() - start_time:.2f} seconds")
                        save_to_db(
                        Report(
                           user_id = 1,
                           password = target_password,
                           algorithm = "hybrid",
                           report_content =f'''Password {target_password} was cracked after {attempt_count} attempts''',
                           is_cracked = True,
                           file = self.fileId
                        )
                    )
                        return True
                    
                    # Also check with word + suffix
                    attempt_count += 1
                    attempt_password = word + prefix
                    if attempt_password == target_password:
                        # print(f"Password cracked: {attempt_password}")
                        # print(f"Total attempts: {attempt_count}")
                        # print(f"Time taken: {time.time() - start_time:.2f} seconds")
                        save_to_db(
                        Report(
                           user_id = 1,
                           password = target_password,
                           algorithm = "hybrid",
                           report_content =f'''Password {target_password} was cracked after {attempt_count} attempts''',
                           is_cracked = True
                        )
                    )
                        return True
        
        print(f"\nPassword not cracked. Total attempts: {attempt_count}")
        save_to_db(
            Report(
                user_id = 1,
                password = target_password,
                algorithm = "hybrid",
                report_content =f'''Password not found within {self.max_length} character length limit.''',
                is_cracked = False
            )
        )
        return False
