import urllib2
from bs4 import BeautifulSoup
import datetime
import time
import os
import json
import jsonschema
from pprint import pprint


# debug level
def set_dbg_lvl(dbg_value):
    global _dbg
    _dbg = dbg_value
    return


# setup Corporate_Data folder path
def set_path_to_tags(path_to_tags):
    global _path
    _path = check_folder(path_to_tags)
    return


def cls():
    os.system('cls' if os.name == 'nt' else 'clear')
    return


def separator():
    print "="*80
    return


def main_get_data(corp_tag):
    # corp_tag used to get data and form final json object
    corporate_dict = full_corp_dict(corp_tag)
    corporate_json = json.dumps(corporate_dict, indent=4)
    pr_debug(corporate_json, 'main')
    pr_debug("current working dir >>  {0}".format(os.getcwd()), 'main')
    saved_file = save_json_in_file(corp_tag, corporate_json)
    return saved_file


def get_date_today():
    return str(datetime.date.today())


def pr_debug(_data, _function):
    # function that prints out debug data;
    # _data - text to print
    # _function - name of the function calling for debug
    # _dbg - flag (0 - disabled | 1 - enabled)
    if _dbg == 1:
        ts = time.time()
        st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
        pprint("[{0}] | [{1}:] {2}".format(st, _function, _data))
        pprint("=" * 50)


def corp_api_call(clan_tag):
    # function that calls 'Igroman787' star conflict players database using provided corp tag
    # returns a list with all the members with corp tag

    # setting up the link for a corporation tag
    _dbg_name = 'corp_api_call'
    link = 'http://ts2.scorpclub.ru/api/v1/findusers.php?search=clanTag%3D%22' \
           + clan_tag + '%22&sort=nickname&DESC=&limit=400'

    # get data from a web page
    page = urllib2.urlopen(link)
    # process html with soup
    soup = BeautifulSoup(page, "html.parser")

    pr_debug(link, _dbg_name)
    pr_debug(page, _dbg_name)
    pr_debug(soup, _dbg_name)

    table = soup.find("table")
    rows = table.find_all("tr")

    table_contents = []  # stores your table here
    for tr in rows:
        # processing data by html tags creating a 2d list containing each row as shorter list
        if rows.index(tr) == 0:
            row_cells = [th.getText().strip() for th in tr.find_all('th') if th.getText().strip() != '']
        else:
            row_cells = ([tr.find('th').getText()] if tr.find('th') else []) + [td.getText().strip() for td in
                                                                                tr.find_all('td') if
                                                                                td.getText().strip() != '']
        if len(row_cells) > 1:
            table_contents += [row_cells]
    pr_debug(table_contents, _dbg_name)
    return table_contents


def lists_to_user_dict(list_of_users):
    # this function creates a list of dictionaries
    # where each dictionary is a player with its id, name, and corpTag (corpTag is redundant but w/e)
    dict_tags = list_of_users[0]
    list_of_users_formatted = []
    pr_debug(dict_tags, 'lists_to_user_dict')
    for i in list_of_users:
        if i != dict_tags:
            pr_debug(i, 'lists_to_user_dict')
            temp_dict = dict(zip(dict_tags, i))
            pr_debug(temp_dict, 'lists_to_user_dict')
            user_link = "http://ts2.scorpclub.ru/api/v1/userinfo.php?uid=" + str(temp_dict["uid"])
            user_link_dict = {"userLink": user_link}
            temp_dict.update(user_link_dict)
            list_of_users_formatted.append(temp_dict)
    pr_debug(list_of_users_formatted, 'lists_to_user_dict')
    return list_of_users_formatted


def full_corp_dict(corp_tag):
    # function that populates full dictionary with received data
    # returns a dict that is ready for conversion to json
    # datetime is "YYYY-MM-DD" format

    list_from_web = corp_api_call(corp_tag)
    members = lists_to_user_dict(list_from_web)
    corporation_dict = {"timeStamp": str(datetime.date.today()), "corpTag": corp_tag, "headCount": len(members),
                        "members": members}
    pr_debug(corporation_dict, "full_corp_dict")
    return corporation_dict


def check_folder(path):
    # checks existence of the folder, relative to the current working path
    pr_debug(path, 'check_folder.folder_path:')
    if os.path.isdir(path):
        pr_debug("Folder '{0}' exists".format(path), 'check_folder()')
    else:
        pr_debug("Folder '{0}' does not exists, creating".format(path), 'check_folder()')
        os.makedirs(path)
    return path


def organise_files(corp_tag):
    # ensures folder structure
    path_to_corp_tag = os.path.join(_path, corp_tag)
    check_folder(path_to_corp_tag)
    return path_to_corp_tag


def validate_json_vs_schema(json_data):
    # validates JSON to meet defined json schema to ensure consistency
    corp_schema = open("corporateMembers_schema.json").read()
    pr_debug(corp_schema, 'validate_json_vs_schema()')
    try:
        jsonschema.Draft4Validator(json.loads(corp_schema)).validate(json.loads(json_data))
    except jsonschema.ValidationError as e:
        pr_debug(e.message, 'validate_json_vs_schema()')
        return False
    return True


def save_json_in_file(corp_tag, json_data):
    # checks if the file does not exists and saves as YYYY-MM-DD_{corpTag}.json file
    # each file contains single json object
    # Igroman787's database is refreshed once a day - hence only 1 file per day stored
    path_to_corp_file = ""
    if validate_json_vs_schema(json_data):
        path_to_corp_folder = organise_files(corp_tag)
        path_to_corp_file = os.path.join(path_to_corp_folder, get_date_today() + "__" + corp_tag + ".json")
        pr_debug(path_to_corp_file, 'save_json_in_file.path_to_corp_file:')
        if os.path.isfile(path_to_corp_file):
            pr_debug("File {0} already exists, skipping".format(path_to_corp_file), "save_json_in_file()")
        else:
            pr_debug("File {0} does not exists, creating".format(path_to_corp_file), "save_json_in_file()")
            json_file = open(path_to_corp_file, 'w')
            json_file.write(json_data)
            json_file.close()
    else:
        print "JSON validation failed"
    return path_to_corp_file


def get_list_of_tags():
    # returns a list of currently tracked corporation tags
    list_of_folders = os.listdir(_path)
    return list_of_folders


def get_list_of_files_to_compare(corp_tag):
    # returns a list of available files for specified corp_tag
    path_to_list = os.path.join(_path, corp_tag)
    file_names = next(os.walk(path_to_list))[2]
    file_names_with_path = []
    for i in file_names:
        file_names_with_path.append(os.path.join(_path, i))
        pr_debug(i, 'get_list_of_files_to_compare().i')
        pr_debug(file_names_with_path, 'get_list_of_files_to_compare().for loop')
    file_names_with_path.sort()
    pr_debug(file_names_with_path, 'get_list_of_files_to_compare().return value')
    return file_names_with_path


def compare_2_latest_files(corp_tag):
    list_of_files = get_list_of_files_to_compare(corp_tag)
    pr_debug(list_of_files, 'compare_2_latest_files()')
    if len(list_of_files) < 2:
        print "There less than 2 records for this corporation"
        print "Can not run report"
        return
    else:
        compare_2_files(list_of_files[-2:])
        return


def compare_2_files(file_names):
    pr_debug(file_names, 'compare_2_files()')
    return
