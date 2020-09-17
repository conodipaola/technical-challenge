import os
import json

import uuid
import hashlib


def create_hash(password):
    # uuid is used to generate a random number for the salt that is the random head of the hashed password
    # it returns a crypted hashed password
    salt = uuid.uuid4().hex
    return hashlib.sha256(salt.encode() + password.encode()).hexdigest() + ':' + salt


def check_pass(hashed_password, user_password):
    # it accepts two passwors the first hashed and the second challenged
    # it returns True or False depending if the two passwords are the same
    password, salt = hashed_password.split(':')
    return password == hashlib.sha256(salt.encode() + user_password.encode()).hexdigest()


def create_owner_data(full_name, auth_file_path, auth_tot):
    """
    This function generates a new set of data for the new owner
    imput params:
        full_name: 'owner' real name (used also as username)
        auth_file_path: full path to the data file authorisation.json
        auth_tot: list of dictionaries bearing the full set of login data of each couple, owner of each separated list 
    TO DO: possibility to modify the passwords already created
    """

    # temp dict used top save login data for the actual couple owner of the list
    auth_data = {}

    password = input('Please enter the list owner password: ')
    print()

    # it creates the hashed passord from the ascii one (for he owner)
    hashed_password = create_hash(password)

    auth_data["owner"] = full_name

    auth_data["password"] = hashed_password

    password = input(
        'Please enter the guest password to access wedding list: ')
    print()

    hashed_password = create_hash(password)

    # it creates the hashed passord from the ascii one (for he guests)
    auth_data["guest_password"] = hashed_password

    auth_tot.append(auth_data)

    # here we save by overwriting the file the full auth_tot list created so far
    with open(auth_file_path, "w") as auth_f:
        json.dump(auth_tot, auth_f, indent=1)


def authentication(user, full_name, auth_tot, auth_file_path):
    """
    Authentication library has been implemented as a set of functions

    input params provided by the driver in main():

        user: 'couple' (list owner) or 'guest' (main buyer)
        full_name: actual name(also used has username) of the user
        auth_tot: full list of authorisation data created so far or to be created yet
        auth_file_path: full path where the file authorisation.json lives.

    autho_tot: is a list of dictionaries
               each dictionary collects data for each couple owner of the list
               fields: 'owner': couple username
                       'password': 'owner' hashed password
                       guest_password': 'guest' hashed password previously created by th owner


    """

    found = False

    # check if authorisation file has been found (created previously) so that 'auth_tot' is not an empty list
    if auth_tot != []:

        # check if the couple owner of the actual wedding list has already created an autherisation account and password
        # also for the guests
        for user_dict in auth_tot:
            if user_dict['owner'] == full_name:
                found = True

        # if the user is the couple owner, if the authority data are already there, it checks the password provided
        # otherwise creates authority data from scratch
        if user == "couple":
            if found:

                print()
                password = input(
                    'Please enter the list owner password: ')

                return check_pass(user_dict['password'], password)
            else:

                create_owner_data(full_name, auth_file_path, auth_tot)

        # if the 'user' is the uest, if the authority data are already there, it checks the password provided
        # otherwise return with a message
        elif user == "guest":

            if found:
                print()
                password = input(
                    'Please enter the guest password: ')

                return check_pass(user_dict['guest_password'], password)

            else:
                print(f"---> You cannot create authorisation data")

    # if authority file has not been found and it ios an empty list, it starts from scratch
    else:

        if user == "couple":

            create_owner_data(full_name, auth_file_path, auth_tot)

        else:
            print(f"---> You cannot create authorisation data")
