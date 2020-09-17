import json

import os


class wedding_list:
    """
    This library consists of the following methods that act on the wedding list:

    1) add_gift: it adds a gift to the list or creates a new list

    2) remove_gift: it removes a gift from the list, by decreasing the quantity of a specific gift
       and, in case the quantity is reduced to 0, by deleting the gift from the list

    """

    def __init__(self, abs_path, full_name):
        """
        Initialization:
            the class takes advantage of Python list and dictionary data structures

            It takes as external params:

                abs_path: absolute path to find stored files in the right directory
                full_name: the user which instantiated the object

            internal paramas:

                counter: it traks the number of gift in the wedding list
                index: index to create a map for the wed_list

                position: dict to map the list of dicts data structure 'wed_list'
                _map_product: dict to map the list of dicts data structure available 'products_path'

        """
        self.counter = 0
        self.index = -1

        # self.wed_list = []
        self.position = {}
        self._map_product = {}

        self.product_path = os.path.join(abs_path, "data", "products.json")
        self.wed_list_path = os.path.join(
            abs_path, "data", full_name + "_wed_list.json")

        with open(self.product_path, "r") as products:
            self._list_products = json.load(products)
        for idx, product in enumerate(self._list_products):
            self._map_product[product['id']] = idx
        # print(self._map_product)

        try:
            with open(self.wed_list_path, "r") as store_wl:
                self.wed_list = json.load(store_wl)

            for wl in self.wed_list:
                self.index += 1
                self.position[wl['id']] = self.index

            # print(self.position)
            print("Wedding list already created!")
        except IOError:
            self.wed_list = []
            print("Start to create your wedding list now!")

        self.max_len_name = max([len(dict1['name'])
                                 for dict1 in self._list_products])
        # print(self.max_len_name)

    def add_gift(self, id):
        """
        This method allows users to add items from a selected gift list and
        if the list is not present to generate a new list

        imput params:
            id: identification number coming from the product lists

        self._map_product: important to map the position products in the product list with their ids
        """
        if id in self._map_product and self._list_products[self._map_product[id]]['in_stock_quantity'] > 0:
            # it check if the chosen id for th eproduct is in the product list
            # and if the quantity available of a specific product is not '0'
            try:
                idx = self.position[id]
                # it checks for the key 'idx' of the wedding list if exists
                # and for the index of the position in the product list if exists
                # if the gift is already in the list it oincreases teh quantity of '1'
                self.wed_list[idx]['quantity'] += 1
            except (IndexError, KeyError):
                # if IndexError/KeyError is generated this means the gift in not in the wedding list
                # the list then is created/updated with th enew gift as dict
                self.index += 1
                self.position[id] = self.index
                idx = self.position[id]
                dict_copy = self._list_products[self._map_product[id]].copy()
                self.wed_list.append(dict_copy)
                self.wed_list[idx].pop('in_stock_quantity')
                self.wed_list[idx]['quantity'] = 1
                self.wed_list[idx]['purchased'] = 0
                self.wed_list[idx]['guest'] = []
        else:
            print()
            print()
            print("=====  WARNING =====")
            print(f"---> Id: {id} is not a valid choice")
            print("====================")
            return

        self._list_products[self._map_product[id]]['in_stock_quantity'] -= 1

        # the total counter 'self.counter' update the total number of gifts in the list
        self.counter += 1

    def remove_gift(self, id):
        """
        This method allows users to remove items from a selected gift list

        imput params:
            id: identification number coming from the product lists
        """
        try:
            # It checks if idx and/or id are available otherwise generates an Index and Key Errors
            idx = self.position[id]
            # idx is created to align wedding list and available factory products list indices
            if self.wed_list[idx]['quantity'] > 1:
                self.wed_list[idx]['quantity'] -= 1
                # the remove process reduces the amount of the gift in the wedding list by '1''
            else:
                self.wed_list.pop(idx)
            # the total counter 'self.counter' update the total number of gifts in the list
            self.counter -= 1
        except (IndexError, KeyError):
            # this part takes care of a wrong typing
            print()
            print()
            print("=====  WARNING =====")
            print(f"---> You cannot remove gift id: {id}: not in the list")
            print("====================")

    def buy_gift(self, id, guest, quantity=1):
        """
        This method allows users to purchased items from a selected gift list

        imput params:
            id: identification number coming from the product lists
            guest: 'couple' or 'guest'. It allows the wedding list owner as well to buy gifts from wedding list
            quantity: default set to '1'. It is possible to choose beween single or multiple buy
        """
        try:
            # It checks if idx and/or id are available otherwise generates an Index and Key Errors
            idx = self.position[id]
            # idx is created to align wedding list and available factory products list indices
            if self.wed_list[idx]['purchased'] < self.wed_list[idx]['quantity']:
                # the purchased process reduces the amount of the gift in the wedding list by the set 'quantity'
                self.wed_list[idx]['purchased'] += quantity
                self.wed_list[idx]['guest'].append(guest)

            else:
                print()
                print()
                print("=====  WARNING =====")
                print(
                    f"---> No more {self.wed_list[idx]['name']} items available")
                print()
                print(f"---> Please choose another gift! ;-)")
                print("====================")

        except (IndexError, KeyError):
            # this part takes care of a wrong typing
            print()
            print()
            print("=====  WARNING =====")
            print(f"---> You cannot buy gift id: {id} not in the list")
            print("====================")

    def store_list_to_disk(self, to_disc='wed'):
        """
        This method is for storage purposes

        input params:
            to_disc: switch
                     'wed' to dsave the updated wedding list 
                     'prod' to save the updated factory products still available for the wedding list 
                     after previous manipulation by the users

        """
        if to_disc == 'wed':
            list_to_disc = self.wed_list
            abspath = self.wed_list_path
        elif to_disc == 'prod':
            list_to_disc = self._list_products
            abspath = self.wed_list_path

        if list_to_disc != []:
            # The  method saves to disk as json format only if the list is not empty
            with open(abspath, "w+") as store_wl:
                json.dump(list_to_disc, store_wl, indent=1)

    def wed_list_size(self):
        # method to retrieve the size of the wedding list generated so far
        print(f"Items in the wedding list: {self.counter}")

    def check_list(self):
        # method to check the existence of the file creted by each instance of the class
        # where the app store the wedding list as json format
        return os.path.exists(self.wed_list_path)

    def print_list(self, list_prod, key1, list_out=1):
        """
        Method that print fornmatted tables to the screen depending on the data provided

        input params:
            list_prod: list with the data to be printed
            key1: dictionary key that differs for different lists of data 
            list_out: switch index
                      0: wedding list data (default) for gifts still not purchased by users (for the full report)
                      1: factory prducts list data
                      2: wedding list data (default) for gifts purchased so far (for the full report)
                      3: wedding list data for gift list formatted table
        """
        for product in list_prod:
            idx = product['id']
            name = product['name']
            brand = product['brand']
            unit_price = product['price']
            quantity = product[key1]
            # purchased = product['purchased']
            if list_out > 0:
                if list_out == 2 or list_out == 3:
                    # check to be able to print report and gift list with the right format
                    # report: purchased separated from the sill available with the right quantity
                    # gift list: showing only the 'still available' gifts
                    quantity -= product['purchased']
                if quantity > 0:
                    print(
                        f"{idx:>10}{name:>60}{brand:>30}{unit_price:>20}{quantity:>25}")
            else:
                purchased = product['purchased']
                guest = tuple(product['guest'])
                if purchased > 0:
                    print(
                        f"{idx:>10}{name:>60}{brand:>30}{unit_price:>20}{purchased:>25}{', '.join(g for g in guest):>30}")

    def list_products(self):
        """
        This method setup printing on screen of the formatted list of available products where the couple can choose from

        It uses the 'self._list_of_products' list of dicts

        uses: the method "print_list" to send formatted text to the screen
        """
        print(f'{"PRODUCT LIST":^145}')
        print(f'{"======================":^145}')
        print()
        print(
            f'{"ID":>10}{"NAME":>60}{"BRAND":>30}{"UNIT_PRICE":>20}{"AVAILABLE_QUANTITY":>25}')
        print()
        # print("{:>5} name  brand   price   quantity in stock")
        # print(f"length list roducts {len(self._list_products)}")
        self.print_list(self._list_products, 'in_stock_quantity')

    def list_gifts(self):
        """
        This method setup printing on screen of the formatted remaining gifts available so far (not yet purchased)

        It uses the 'self.wed_list' list of dicts created so far

        uses: the method "print_list" to send formatted text to the screen
        """
        print(f'{"GIFT LIST":^145}')
        print(f'{"======================":^145}')
        print()
        print(
            f'{"ID":>10}{"NAME":>60}{"BRAND":>30}{"UNIT_PRICE":>20}{"QUANTITY":>25}')
        print()

        self.print_list(self.wed_list, 'quantity', list_out=3)

    def report(self):
        """
        This method setup printing on screen the formatted full report of the wedding list so far

        It uses the 'self.wed_list' list of dicts created so far
        and it separates the purchased from the still available gifts of the list

        uses: the method "print_list" to send formatted text to the screen
        """
        print()
        print(f'{"======================":^175}')
        print(f'{"GIFT LIST STATE REPORT":^175}')
        print(f'{"======================":^175}')
        print()
        print(f'{"PURCHASED GIFTS":^175}')
        print(f'{"======================":^175}')
        print()
        print(
            f'{"ID":>10}{"NAME":>60}{"BRAND":>30}{"UNIT_PRICE":>20}{"#PURCHASED":>25}{"GUEST(S)":>30}')
        print()

        self.print_list(self.wed_list, 'quantity', list_out=0)

        print()
        print(f'{"STILL AVAILABLE GIFTS":^175}')
        print(f'{"===========================":^175}')
        print()
        print(f'{"ID":>10}{"NAME":>60}{"BRAND":>30}{"UNIT_PRICE":>20}{"QUANTITY":>25}')
        print()

        self.print_list(self.wed_list, 'quantity', list_out=2)
