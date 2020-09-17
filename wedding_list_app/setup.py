import json

import os

import uuid
import hashlib

from library.library import *

from library.authentication import authentication


def add_remove_buy(wed_list, to_do, wed_guest):
    """
    This driver function takes care of the process of adding/removing/buying a gift to update the wedding list

    For one user at the time

    input params: 
        wed_list: the data list associated to the wedding list
        to_do: choice between 2) add; 3) remove; 4) buy gifts from the wedding list
        wed_guest: string with the name of the buyer 
    """
    os.system('clear')

    if to_do == "2":
        wed_list.list_products()
        print("====================")
        print()
        print("Please add/create from the above products!")
        print()

    # first it shows the wedding list so far
    wed_list.list_gifts()
    print("====================")
    print()
    # It asks for the gift to be added/removed/bought
    gift = input("GIFT ID > ")

    # It acts on the wed_list
    if to_do == "2":

        wed_list.add_gift(int(gift))

    elif to_do == "3":

        wed_list.remove_gift(int(gift))

    elif to_do == "4":

        wed_list.buy_gift(int(gift), guest=wed_guest)

    print()
    print("====================")
    # it shows again the updated wedding list
    wed_list.list_gifts()

    # finally it stores on the disk the updated wedding list
    wed_list.store_list_to_disk()


def user(aka, auth_tot, dir_absolute_path):

    os.system('clear')
    full_name = input("My full name> ")

    check = "ok"

    status = "ok"

    # dir_absolute_path = os.path.dirname(os.path.abspath(__file__))

    auth_file_path = os.path.join(
        dir_absolute_path, "data", "authentication.json")

    if aka == "couple":

        wed_list = wedding_list(dir_absolute_path, full_name)

        couple_name = full_name

    if aka == "guest":

        wed_couple = input("Couple full name> ")

        wed_list = wedding_list(dir_absolute_path, wed_couple)

        couple_name = wed_couple

    # try:
    #     with open(auth_file_path, "r") as auth_f:
    #         auth_tot = json.load(auth_f)
    # except IOError:
    #     auth_tot = []

    pass_try = 0
    while check != "q":

        success = authentication(aka, couple_name, auth_tot, auth_file_path)

        pass_try += 1

        print(f"----> password try number {pass_try}")

        if success:
            check = "q"
        elif pass_try == 3:
            check = "q"
            status = "q"

    while status != "q":

        if aka == "couple":

            os.system('clear')
            print(f"Dear {full_name.upper()} welcome to your gift list")
            print("Let's choose between the following options:")
            print("===============")
            print()
            print("1: print the available products")
            print("2: add gift to the list or create a new list")
            print("3: remove gift from the list")
            print("4: buy a gift")
            print("5: print gift list status report")
            print("(0 to exit)")
            print("===============")
            print()

            choice = input("My choice is> ")

            if choice == "0":

                status = "q"

                wed_list.store_list_to_disk(to_disc='prod')

            elif choice == "1":

                os.system('clear')
                wed_list.list_products()
                print()
                input("Type any key to exit from the product display?")

            elif choice == "5":

                os.system('clear')
                wed_list.report()
                print()
                input("Type any key to exit from the product display?")

            elif choice == "2" or choice == "3" or choice == "4":

                step = True
                while step:
                    os.system('clear')

                    if choice == "2":
                        wed_list.list_products()
                        print("====================")
                        print()
                        print("Please add from the above products!")
                        print()

                    add_remove_buy(wed_list, choice, full_name)

                    step = input("Would you like to do more?> (yes / no)")

                    if step == "no":
                        step = False
                    elif step != "yes" and step != "no":
                        print("I do not understand the answer, I am quitting!")
                        step = False

        elif aka == "guest":

            os.system('clear')
            print(f"Dear {full_name.upper()} welcome to our gift list")
            print("Let's choose between the following options:")
            print("===============")
            print()
            print("1: print the couple gift list")
            print("2: buy a gift")
            print("(0 to exit)")
            print("===============")
            print()

            choice = input("My choice is> ")

            if choice == "0":

                status = "q"

            elif choice == "1":

                os.system('clear')
                wed_list.list_gifts()
                print()
                input("Type any key to exit from the product display?")

            elif choice == "2":

                choice = "4"
                step = True
                while step:
                    os.system('clear')

                    add_remove_buy(wed_list, choice, full_name)

                    step = input("Would you like to do more?> (yes / no)")

                    if step == "no":
                        step = False
                    elif step != "yes" and step != "no":
                        print("I do not understand the answer, I am quitting!")
                        step = False


def main():
    """
    This is the main function of the driver

    It checks first if the authentication file 'authentication.json' is present 

    otherwise generates 
    """

    status = "ok"

    # wed_list = wedding_list(dir_absolute_path)

    dir_absolute_path = os.path.dirname(os.path.abspath(__file__))

    auth_file_path = os.path.join(
        dir_absolute_path, "data", "authentication.json")

    try:
        with open(auth_file_path, "r") as auth_f:
            auth_tot = json.load(auth_f)
    except IOError:
        auth_tot = []

    while status != "q":
        os.system('clear')
        print("=============================")
        print()
        print("     PREZOLA    ")
        print("     Wedding List  ")
        print()
        print("=============================")
        print()
        print()

        print("Pleae type: ")
        print()
        print("1 If you are a wedding couple")
        print("2 if you are a wedding guest")
        print("(0 to quit)")
        print()

        identity = input("I am > ")

        if int(identity) == 1:
            user("couple", auth_tot, dir_absolute_path)
        if int(identity) == 2:
            user("guest", auth_tot, dir_absolute_path)
        elif int(identity) == 0:
            status = "q"
            print()
            print("To next time! :-)")
        else:
            print()
            print("Please try again")


if __name__ == "__main__":
    main()
