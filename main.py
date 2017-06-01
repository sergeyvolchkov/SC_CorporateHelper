import driver
import json
import os


def main(corptag, debug_level):
    # corptag used to get data and form final json object
    # debug_level control debug console output from functions. 1 - Enable; 0 - Disable.

    corporate_dict = driver.full_corp_dict(corptag, debug_level)
    corporate_json = json.dumps(corporate_dict, indent=4)
    driver.pr_debug(corporate_json, 'main', debug_level)
    driver.pr_debug("current working dir >>  {0}".format(os.getcwd()), 'main', debug_level)
    driver.save_json_in_file(corptag, corporate_json, debug_level)


if __name__ == '__main__':
    corpTag = 'NASA'
    debug_level = 1
    main(corpTag, debug_level)

