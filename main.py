import driver
import json


try:
    # corporate tag used to get data and form final json object
    corpTag = 'Ninja'
    # debug_level control debug console output from functions. 1 - Enable; 0 - Disable.
    debug_level = 0
    corporate_dict = driver.full_corp_dict(corpTag, debug_level)
    corporate_json = json.dumps(corporate_dict, indent=4)
    driver.pr_debug(corporate_json, 'main', debug_level)
    print corporate_json
except:
    print "uh-oh! Stuff is not working"