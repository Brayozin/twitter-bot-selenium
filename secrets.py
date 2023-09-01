"""
    Add your twitter handle's email and password
    in the credentials.txt file.
    This will be used to automate the login.
"""


def get_credentials() -> dict:
    # dictionary for storing credentials
    credentials = dict()
    # reading the text file
    # for credentials
    with open('credentials.txt') as f:
        # iterating over the lines
        for line in f.readlines():
            try:
                # fetching email and password
                key, value = line.split(": ")
            except ValueError:
                # raises error when email and password not supplied
                print('Add your email and password in credentials file')
                exit(0)
            # removing trailing
            # white space and new line
            credentials[key] = value.rstrip(" \n")
    # returning the dictionary containing the credentials
    return credentials
