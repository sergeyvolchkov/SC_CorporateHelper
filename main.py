import driver
import json
import os
import sys
import pprint


menu_actions = {}
debug_level = 0     # debug_level control debug console output from functions. 1 - Enable; 0 - Disable.


def main_get_data(corp_tag):
    # corp_tag used to get data and form final json object
    corporate_dict = driver.full_corp_dict(corp_tag, debug_level)
    corporate_json = json.dumps(corporate_dict, indent=4)
    driver.pr_debug(corporate_json, 'main', debug_level)
    driver.pr_debug("current working dir >>  {0}".format(os.getcwd()), 'main', debug_level)
    saved_file = driver.save_json_in_file(corp_tag, corporate_json, debug_level)
    return saved_file


def cls():
    os.system('cls' if os.name == 'nt' else 'clear')
    return


def separator():
    print "="*80
    return


# Main menu
def main_menu():
    print "\n"
    separator()
    print "-"*10 + "Main Menu" + "-"*10
    separator()
    print "List of current tags:"
    pprint.pprint(driver.get_list_of_tags(debug_level))
    separator()
    print "\n1. Update all corporation tags"
    print "2. Add new corporation tag"
    print "\n3. Corporation activity"
    print "\n0. Quit"
    separator()
    choice = raw_input(" >>  ")
    exec_menu(choice)
    return


# Execute menu
def exec_menu(choice):
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
def update_all_tags():
    separator()
    list_of_tags = driver.get_list_of_tags(debug_level)
    if not list_of_tags:
        print "There are no tags to update, please add corporation tags!"
    else:
        for corp_tag in list_of_tags:
            print "Getting the data for [{0}]".format(corp_tag)
            print "Data is in '{0}' file".format(main_get_data(corp_tag))
            separator()
        print "All done! updated data for {0}".format(driver.get_date_today())
    exec_menu('9')
    return


# Menu 2
def add_new_tag():
    separator()
    corp_tag = raw_input("Please enter corporate tag (it is case sensitive):  ")
    print "Getting the data for [{0}]".format(corp_tag)
    print "All done! Data is in '{0}' file".format(main_get_data(corp_tag))
    print "\n"
    exec_menu('9')
    return


# Menu 3
def menu3():
    separator()
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


# Menu definition
menu_actions = {
    'main_menu': main_menu,
    '1': update_all_tags,
    '2': add_new_tag,
    '3': menu3,
    '9': back,
    '0': exit,
}

if __name__ == '__main__':
    # Launch main menu
    cls()
    main_menu()
