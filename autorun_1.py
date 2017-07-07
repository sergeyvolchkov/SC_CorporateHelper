import main
import driver
import sys


if __name__ == '__main__':
    # Get latest data
    driver.cls()
    print main.version
    print "Debug level is", driver.set_dbg_lvl(main.debug_level)
    driver.set_path_to_tags(main.path_to_tags)
    list_of_tags = driver.get_list_of_tags()
    if not list_of_tags:
        print "There are no tags to update, please add corporation tags!"
    else:
        for corp_tag in list_of_tags:
            print "Getting the data for [{0}]".format(corp_tag)
            print "Data is in '{0}' file".format(driver.main_get_data(corp_tag))
            driver.separator()
        print "All done! updated data for {0}".format(driver.get_date_today())

    # If corporation tag has been passed as an argument to a script (from command line)
    # this script will generate report for that corporation
    # Report only includes transfers based on latest available data
    if len(sys.argv) == 1:
        main.exec_menu('0')
    elif sys.argv[1] in list_of_tags:
        corp_tag = sys.argv[1]
        print "\n\n\nArgument detected, generating a report on corporation transfers for [{}]".format(corp_tag)
        driver.separator()
        driver.separator()
        driver.separator()
        number_of_records = 2
        print "\nLatest activity for: " + corp_tag
        driver.compare_range_of_files(corp_tag, number_of_records)
        driver.separator()
        driver.separator()
    else:
        print "\n\n\nArgument detected, but there are no records for such corporation tag"
    main.exec_menu('0')
