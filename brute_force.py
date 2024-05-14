import itertools
import string
import time
import timeit
from database import *

class BruteForcePasswordCracker:
    def __init__(self, max_length, charset=None):
        """
        Initializes the brute-force cracker.

        Parameters:
        max_length (int): Maximum password length to try.
        charset (str): Characters to use for the attack.
        """
        self.max_length = int(max_length)
        self.charset = charset or (string.ascii_letters + string.digits + string.punctuation)
    
    def crack_password(self, target_password):
        """
        Tries to crack the target password using brute-force.

        Parameters:
        target_password (str): The password to crack.

        Returns:
        str: The cracked password if found, otherwise None.
        """
        start_time = time.time()
        attempts = 0

        # Iterate through all password lengths up to max_length
        for length in range(self.max_length, self.max_length + 1):
            # Generate combinations of characters with the current length
            for attempt in itertools.product(self.charset, repeat=length):
                attempts += 1
                attempt_password = ''.join(attempt)
                
                # Check if the generated password matches the target password
                if attempt_password == target_password:
                    end_time = time.time()
                    print(end_time, start_time, end_time-start_time)
                    save_to_db(
                        Report(
                           user_id = 1,
                           password = target_password,
                           algorithm = "brute-force",
                           report_content =f'''Password {target_password} was cracked after {attempts} attempts''',
                           is_cracked = True,
                           attempts = attempts,
                           time_taken = end_time - start_time
                        )
                    )
                    return attempt_password
                
                # Display current attempt
                # print(f"Current attempt: {attempt_password}", end='\r', flush=True)
        
        end_time = time.time()
        save_to_db(
            Report(
                user_id = 1,
                password = target_password,
                algorithm = "brute-force",
                report_content =f'''Password not found within {self.max_length} character length limit.''',
                is_cracked = False,
                attempts = attempts,
                time_taken = end_time - start_time
            )
        )
        return None


