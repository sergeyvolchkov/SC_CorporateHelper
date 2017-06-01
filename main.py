import driver
import json

import os

try:
    # corporate tag used to get data and form final json object
    corpTag = 'NASA'
    # debug_level control debug console output from functions. 1 - Enable; 0 - Disable.
    debug_level = 1
    corporate_dict = driver.full_corp_dict(corpTag, debug_level)
    corporate_json = json.dumps(corporate_dict, indent=4)
    driver.pr_debug(corporate_json, 'main', debug_level)

    # ======================

    driver.pr_debug("current working dir >>  {0}".format(os.getcwd()), 'main', debug_level)
    driver.save_json_in_file(corpTag, corporate_json, debug_level)

except:
    print "uh-oh! Stuff is not working"