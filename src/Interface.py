
def get_user_info():
    user_info = ""

    while True:
        entry = input("$ ")

        # Check if semicolon is entered or if the string ends with a semicolon
        if entry.endswith(';'):
            user_info += entry[:-1]  # Exclude the semicolon
            break

        # Append the input to the user_info string
        user_info += entry + "\n"

    return user_info.strip()
