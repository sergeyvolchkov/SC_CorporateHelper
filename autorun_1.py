import main
import driver


if __name__ == '__main__':
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
    main.exec_menu('0')
