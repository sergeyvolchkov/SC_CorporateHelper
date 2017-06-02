import driver
import sys
import pprint


debug_level = 0
version = "v0.02"


# Main menu
def main_menu():
    print "\n"
    driver.separator()
    print "Main Menu"
    driver.separator()
    print "List of current tags:"
    pprint.pprint(driver.get_list_of_tags())
    driver.separator()
    print "\n1. Update all corporation tags"
    print "2. Add new corporation tag"
    print "\n3. Latest activity for all tracked corporations"
    print "4. Activity for 2 selected dates (single corporation)"
    print "5. Activity for a time period (single corporation)"
    print "\n0. Quit"
    driver.separator()
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
    driver.separator()
    list_of_tags = driver.get_list_of_tags()
    if not list_of_tags:
        print "There are no tags to update, please add corporation tags!"
    else:
        for corp_tag in list_of_tags:
            print "Getting the data for [{0}]".format(corp_tag)
            print "Data is in '{0}' file".format(driver.main_get_data(corp_tag))
            driver.separator()
        print "All done! updated data for {0}".format(driver.get_date_today())
    exec_menu('9')
    return


# Menu 2
def add_new_tag():
    driver.separator()
    corp_tag = raw_input("Please enter corporate tag (it is case sensitive):  ")
    print "Getting the data for [{0}]".format(corp_tag)
    print "All done! Data is in '{0}' file".format(driver.main_get_data(corp_tag))
    print "\n"
    exec_menu('9')
    return


# Menu 3
def latest_activity():
    driver.separator()
    print "latest_activity\n"
    print "9. Back"
    print "0. Quit"
    driver.separator()
    choice = raw_input(" >>  ")
    exec_menu(choice)
    return


# Menu 4
def activity_for_2_dates():
    driver.separator()
    print "activity_for_2_dates\n"
    print "9. Back"
    print "0. Quit"
    driver.separator()
    choice = raw_input(" >>  ")
    exec_menu(choice)
    return


# Menu 5
def activity_for_period():
    driver.separator()
    print "activity_for_period\n"
    print "9. Back"
    print "0. Quit"
    driver.separator()
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
    '3': latest_activity,
    '4': activity_for_2_dates,
    '5': activity_for_period,
    '9': back,
    '0': exit,
}

if __name__ == '__main__':
    # Launch main menu
    driver.cls()
    print version
    # debug_level control debug console output from functions. 1 - Enable; 0 - Disable.
    print "Debug level is", driver.set_dbg_lvl(debug_level)
    main_menu()
