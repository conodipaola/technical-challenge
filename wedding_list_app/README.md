# Technical specs

The sructure of the WEDDING_LIST_APP:

WEDDING_LIST_APP

- data (storage for the json files: e.g., products.json)
- library: 1) authentication.py (authentication library); 2) library.py (class for the wedding list manipulation)
- setup.py (stand-alone driver)

Based on the following list provide of must do:

- Add a gift to the list
- Remove a gift from the list
- List the already added gifts of the list
- Purchase a gift from the list
- Generate a report from the list which will print out the gifts and their statuses.
  - The report must include two sections:
    - Purchased gifts: each purchased gift with their details.
    - Not purchased gifts: each available gift with their details.

I created an app in full Python languange that reflects the above list.

I also added the authentication with hashed password for owners and users.

The data directory is the place for the storage of:

- full product list
- authentication login data (authentication.json) updated on the fly
- wedding list data updated on the fly

Main things TO DO:

1. possibility to change already generated passwords

2. logging would be auspicable

3. use of frameworks like flask/Django and SQL database: to have a nive web application

4. web application for example with
