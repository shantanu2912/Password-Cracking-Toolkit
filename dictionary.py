from database import *
class DictionaryAttack:
    def __init__(self, dictionary_file = r"C:\Users\shantanu sharma\Downloads\words.txt"):
        """
        Initialize the DictionaryAttack class with the dictionary file.
        """
        self.dictionary_file = dictionary_file

    def crack_password(self, target_password):
        """
        Attempt to crack the target password using the dictionary attack.
        """
        # Open the dictionary file and read all lines
        try:
            with open(self.dictionary_file, 'r') as file:
                dictionary = file.readlines()
        except FileNotFoundError:
            print(f"Dictionary file '{self.dictionary_file}' not found.")
            return False
        
        current_attempt = 0

        # Iterate through each password in the dictionary
        for password in dictionary:
            current_attempt += 1
            password = password.strip()  # Strip whitespace characters

            # Check if the password matches the target password
            if password == target_password:
                print(f"Password cracked! The password is: {password}")
                save_to_db(
                        Report(
                           user_id = 1,
                           password = target_password,
                           algorithm = "Dictionary",
                           report_content =f'''Password {target_password} was cracked after {current_attempt} attempts''',
                           is_cracked = True
                        )
                    )
                return True

        # If the loop completes without finding a match
        print("Password not found in the dictionary.")
        save_to_db(
            Report(
                user_id = 1,
                password = target_password,
                algorithm = "Dictionary",
                report_content =f'''Password not found''',
                is_cracked = False
            )
        )
        return False
  
