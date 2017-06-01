import driver
import json
import os
import sys


menu_actions = {}
debug_level = 0     # debug_level control debug console output from functions. 1 - Enable; 0 - Disable.


def main_get_data(corptag):
    # corptag used to get data and form final json object
    corporate_dict = driver.full_corp_dict(corptag, debug_level)
    corporate_json = json.dumps(corporate_dict, indent=4)
    driver.pr_debug(corporate_json, 'main', debug_level)
    driver.pr_debug("current working dir >>  {0}".format(os.getcwd()), 'main', debug_level)
    saved_file = driver.save_json_in_file(corptag, corporate_json, debug_level)
    return saved_file


def cls():
    os.system('cls' if os.name == 'nt' else 'clear')
    return


# Main menu
def main_menu():
    cls()
    print "\nMain Menu"
    print "Please enter an action:"
    print "1. Get latest available corporate data"
    print "2. Corporate activity"
    print "\n0. Quit"
    choice = raw_input(" >>  ")
    exec_menu(choice)
    return


# Execute menu
def exec_menu(choice):
    cls()
    ch = choice.lower()
    if ch == '':
        menu_actions['main_menu']()
    else:
        try:
            menu_actions[ch]()
        except KeyError:
            print "Invalid selection, please try again.\n"
            menu_actions['main_menu']()
    return


# Menu 1
def menu1():
    cls()
    corp_tag = raw_input("Please enter corporate tag (it is case sensitive):  ")
    print "Getting the data for {0}!".format(corp_tag)
    print "Data is in '{0}' file".format(main_get_data(corp_tag))
    print "\n"*2
    exec_menu('9')
    return


# Menu 2
def menu2():
    print "Activity Menu!\n"
    print "9. Back"
    print "0. Quit"
    choice = raw_input(" >>  ")
    exec_menu(choice)
    return


# Back to main menu
def back():
    menu_actions['main_menu']()


# Exit program
def exit():
    sys.exit()


# =======================
#    MENUS DEFINITIONS
# =======================

# Menu definition
menu_actions = {
    'main_menu': main_menu,
    '1': menu1,
    '2': menu2,
    '9': back,
    '0': exit,
}

if __name__ == '__main__':
    # =======================
    #      MAIN PROGRAM
    # =======================
    # Launch main menu
    main_menu()
