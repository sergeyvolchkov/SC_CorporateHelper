import urllib2
from bs4 import BeautifulSoup
import datetime
import time
import os
import json
import jsonschema
from pprint import pprint


# version
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
    print "="*105
    return


def pr_activity_header():
    print "|------- {0} --------|----- {1} ----|--- {2} --|--- {3} --|--- {4} ---|--- {5} --|".\
        format("Name", "Uid", "Games", "W/L", "KD", "KDA")
    return


def pr_activity_member(data):
    print "|--{0:>16} --|--{1:>9} --|--{2:>7} --|--{3:>5} --|--{4:>5} --|--{5:>5} --|".\
        format(data['name'], data['uid'], data['total_games'], data['avg_wl'], data['avg_kd'], data['avg_kda'])
    return


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
        separator()


def pr_debug_files(_filename, _label):
    # function to print out file names, follows debug level
    if _dbg == 1:
        ts = time.time()
        st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
        for i in _filename:
            print "[{0}] | [{1}:] {2}".format(st, _label, i)
            separator()


def pr_transfer_result(delta_removed, delta_added, delta_renamed, delta_date):
    print "\nComparing Dates {0} >> {1}:\n".format(delta_date[0], delta_date[1])
    print "Removed:"
    if len(delta_removed) > 0:
        for x in delta_removed:
            pr_member(x)
    else:
        print "  none"

    print "\nAdded:"
    if len(delta_added) > 0:
        for x in delta_added:
            pr_member(x)
    else:
        print "  none"

    print "\nRenamed:"
    if len(delta_renamed) > 0:
        for x in delta_renamed:
            pr_member(x)
    else:
        print "  none"
    separator()
    return


def pr_member(item):
    print "  Name: {0:<15} | uid: {1:<9} | stats: {2}".format(item["nickname"], item["uid"], item["userLink"])
    if "oldName" in item:
        print "  From: {0:<15}\n".format(item["oldName"])
    return


def souping_the_web(soup):
    table = soup.find("table")
    rows = table.find_all("tr")

    table_contents = []  # stores your table here
    for tr in rows:
        # processing data by html tags creating a 2d list containing each row as shorter list
        if rows.index(tr) == 0:
            row_cells = [th.getText().strip() for th in tr.find_all('th') if th.getText().strip() != '']
        else:
            row_cells = ([tr.find('th').getText()] if tr.find('th') else []) + [td.getText().strip() for td in
                                                                                tr.find_all('td')]
        if len(row_cells) > 1:
            table_contents += [row_cells]
    pr_debug(table_contents, 'souping_the_web()')
    return table_contents


def main_get_data(corp_tag):
    # corp_tag used to get data and form final json object
    corporate_dict = full_corp_dict(corp_tag)
    corporate_json = json.dumps(corporate_dict, indent=4)
    pr_debug(corporate_json, 'main')
    pr_debug("current working dir >>  {0}".format(os.getcwd()), 'main')
    saved_file = save_json_in_file(corp_tag, corporate_json)
    return saved_file


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
    return souping_the_web(soup)


def player_api_call(player_uid):
    # function that calls 'Igroman787' star conflict players database using provided uid of a player
    # returns a dict with all recorded activity for that user

    # setting up the link for a players uid
    _dbg_name = 'player_api_call'
    # link = http://ts2.scorpclub.ru/api/v1/userinfo.php?uid=177546
    link = 'http://ts2.scorpclub.ru/api/v1/userinfo.php?uid=' + player_uid

    # get data from a web page
    page = urllib2.urlopen(link)
    # process html with soup
    soup = BeautifulSoup(page, "html.parser")

    pr_debug(link, _dbg_name)
    pr_debug(page, _dbg_name)
    pr_debug(soup, _dbg_name)

    return souping_the_web(soup)


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


def formatted_players_activity(player_uid):
    players_activity_dump = player_api_call(player_uid)
    dict_tags = players_activity_dump[0]
    players_activity_formatted = []
    for i in players_activity_dump:
        if i != dict_tags:
            temp_dict = dict(zip(dict_tags, i))
            players_activity_formatted.append(temp_dict)
    pr_debug(players_activity_formatted, 'formatted_players_activity()')
    return players_activity_formatted


def avg_player_activity(player_uid, amount_of_days):
    player_data = formatted_players_activity(player_uid)
    if len(player_data) > amount_of_days:
        player_data = player_data[0-amount_of_days:]
    else:
        # in case when history for a player just started - remove 1st element, since it contains full history stats
        player_data.pop(0)


    avg_kd = 0
    avg_kda = 0
    avg_wl = 0
    total_games = 0
    avg_factor = 0

    for i in player_data:
        if int(i['gamePlayed+']) > 0:
            avg_kd += float(i['K/D+'])
            avg_kda += float(i['KDA+'])
            avg_wl += float(i['W/L+'])
            total_games += int(i['gamePlayed+'])
            avg_factor += 1
    avg_factor = float(avg_factor)

    if avg_factor > 0:
        avg_kd = float("{0:.1f}".format(avg_kd/avg_factor))
        avg_kda = float("{0:.1f}".format(avg_kda/avg_factor))
        avg_wl = float("{0:.1f}".format(avg_wl/avg_factor))

    avg_data = {
        'uid': player_uid,
        'name': player_data[1]['nickname'],
        'avg_kd': avg_kd,
        'avg_kda': avg_kda,
        'avg_wl': avg_wl,
        'total_games': total_games
    }
    return avg_data


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

        pr_debug("File {0} does not exists, creating".format(path_to_corp_file), "save_json_in_file()")
        json_file = open(path_to_corp_file, 'w')
        json_file.write(json_data)
        json_file.close()
        # if os.path.isfile(path_to_corp_file):
        #     pr_debug("File {0} already exists, skipping".format(path_to_corp_file), "save_json_in_file()")
        # else:
        #     pr_debug("File {0} does not exists, creating".format(path_to_corp_file), "save_json_in_file()")
        #     json_file = open(path_to_corp_file, 'w')
        #     json_file.write(json_data)
        #     json_file.close()
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
        file_names_with_path.append(os.path.join(path_to_list, i))
        pr_debug(i, 'get_list_of_files_to_compare().i')
        pr_debug(file_names_with_path, 'get_list_of_files_to_compare().for loop')
    file_names_with_path.sort()
    pr_debug_files(file_names_with_path, 'get_list_of_files_to_compare().return value')
    return file_names_with_path


def compare_2_latest_files(corp_tag):
    list_of_files = get_list_of_files_to_compare(corp_tag)
    pr_debug_files(list_of_files, 'compare_2_latest_files()')
    if len(list_of_files) < 2:
        print "There are less than 2 records for this corporation"
        print "Unable to generate the report"
        separator()
    else:
        delta_removed, delta_added, delta_renamed, delta_date = compare_2_files(list_of_files[-2:])
        pr_debug(delta_removed, "compare_2_latest_files() - Removed records:")
        pr_debug(delta_added, "compare_2_latest_files() - Added records:")
        pr_debug(delta_renamed, "compare_2_latest_files() - Renamed records:")
        pr_transfer_result(delta_removed, delta_added, delta_renamed, delta_date)
    return


def compare_range_of_files(corp_tag, range_of_files):
    list_of_files = get_list_of_files_to_compare(corp_tag)
    if len(list_of_files) > range_of_files:
        list_of_files = list_of_files[0-range_of_files:]
    separator()
    print "\nChecking [{0}] history, last {1} records".format(corp_tag, range_of_files)
    pr_debug(range_of_files, 'compare_range_of_files()')
    pr_debug_files(list_of_files, 'compare_range_of_files()')
    if len(list_of_files) < 2:
        print "There are less than 2 records for this corporation"
        print "Unable to generate the report"
        separator()
    else:
        for i in range(len(list_of_files)):
            pr_debug(i, 'compare_range_of_files() for loop index')
            if i == len(list_of_files)-1:
                break
            delta_removed, delta_added, delta_renamed, delta_date = compare_2_files(list_of_files[i:i+2])
            pr_debug(delta_removed, "compare_range_of_files() - Removed records:")
            pr_debug(delta_added, "compare_range_of_files() - Added records:")
            pr_debug(delta_renamed, "compare_range_of_files() - Renamed records:")
            pr_transfer_result(delta_removed, delta_added, delta_renamed, delta_date)
    return


def compare_2_files(file_names):
    pr_debug_files(file_names, 'compare_2_files()')

    with open(file_names[1]) as from_recent_file:
        file_recent = json.load(from_recent_file)
    with open(file_names[0]) as from_older_file:
        file_older = json.load(from_older_file)

    pr_debug(file_recent, "Last known data:")
    pr_debug(file_older, "Comparing to:")

    delta_date = []
    delta_added = []
    delta_removed = []
    delta_renamed = []

    for x in file_recent["members"]:
        if x not in file_older["members"]:
            delta_added.append(x)

    for x in file_older["members"]:
        if x not in file_recent["members"]:
            delta_removed.append(x)

    for i in range(len(delta_removed)):
        for x in delta_removed:
            for y in delta_added:
                if x["uid"] == y["uid"]:
                    delta_added.remove(y)
                    delta_removed.remove(x)
                    y["oldName"] = x["nickname"]
                    delta_renamed.append(y)

    delta_date.append(file_older["timeStamp"])
    delta_date.append(file_recent["timeStamp"])
    return delta_removed, delta_added, delta_renamed, delta_date


def get_list_of_players_in_corp(corp_tag):
    list_of_files = get_list_of_files_to_compare(corp_tag)
    list_of_files = list_of_files[-1:]
    list_of_players = []
    with open(list_of_files[0]) as from_file:
        corp_data = json.load(from_file)

    for i in corp_data['members']:
        list_of_players.append(i['uid'])
    return list_of_players

