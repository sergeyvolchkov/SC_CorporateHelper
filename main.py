import driver
import sys
from pprint import pprint
from os.path import join

debug_level = 0
path_to_tags = join('..', 'Corporate_Data')
version = "v0.22"


# Main menu
def main_menu():
    print "\n"
    driver.separator()
    print "Main Menu"
    driver.separator()
    print "List of current tags:"
    pprint(driver.get_list_of_tags())
    driver.separator()
    print "\n 1. Update all corporation tags"
    print " 2. Add new corporation tag"
    print "\n 3. Latest transfers for all tracked corporations"
    print " 4. Transfers for a 30 days (single corporation)"
    print "\n 5. Corporate activity for last 10 days"
    print "\n 0. Quit"
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
    driver.cls()
    driver.separator()
    driver.separator()
    driver.separator()
    number_of_records = 7
    corp_tags = driver.get_list_of_tags()
    for tag in corp_tags:
        print "\nLatest activity for: " + tag
        driver.compare_range_of_files(tag, number_of_records)
        driver.separator()
        driver.separator()
    exec_menu('9')
    return


# Menu 4
def activity_for_period():
    driver.cls()
    driver.separator()
    number_of_records = 30
    tag = sub_menu_corp_tag_selection()
    driver.compare_range_of_files(tag, number_of_records)
    driver.separator()
    exec_menu('9')
    return


# Menu 5
def corp_members_activity():
    driver.cls()
    driver.separator()
    number_of_records = 14
    tag = sub_menu_corp_tag_selection()
    print "\n {0:>4}".format(tag)
    print "Players activity for past {0}".format(number_of_records)
    print "\n " + ("-" * 82)

    driver.pr_activity_header()
    list_of_players = driver.get_list_of_players_in_corp(tag)
    for uid in list_of_players:
        avg_player_data = driver.avg_player_activity(uid, number_of_records)
        driver.pr_activity_member(avg_player_data)
    print " " + ("-" * 82)
    driver.separator()
    exec_menu('9')
    return


# Menu 6
def corp_avg_members_stats():
    driver.cls()
    driver.separator()
    print "NOT IMPLEMENTED\n"
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
def _exit():
    sys.exit()


def sub_menu_corp_tag_selection():
    corp_tags = driver.get_list_of_tags()
    print "\nSelect a corporation to proceed:"
    print "\n  {0:<2} - {1}".format(0, 'EXIT to Main Menu\n')
    for tag in corp_tags:
        print "  {0:<2} - {1}".format(corp_tags.index(tag)+1, tag)

    selection = raw_input("\n >>  ")
    if selection == '0':
        exec_menu('9')
    tag = corp_tags[int(selection)-1]
    return tag


# Menu definition
menu_actions = {
    'main_menu': main_menu,
    '1': update_all_tags,
    '2': add_new_tag,
    '3': latest_activity,
    '4': activity_for_period,
    '5': corp_members_activity,
    '6': corp_avg_members_stats,
    '9': back,
    '0': _exit,
}

if __name__ == '__main__':
    # Launch main menu
    driver.cls()
    print version
    # debug_level control debug console output from functions. 1 - Enable; 0 - Disable.
    print "Debug level is", driver.set_dbg_lvl(debug_level)
    driver.set_path_to_tags(path_to_tags)
    main_menu()
