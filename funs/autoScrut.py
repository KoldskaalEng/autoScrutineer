# Automatic Scrutineering script by 'Koldskaal' on f1Technical
# For use in MVRC: https://mantiumchallenge.com/

import os
import time
import shutil
from obscure_rule import ruleObscure
from nSections_rule import ruleNSections

# Scrutineer a single submission: 
def scrutineer(allRules, settings):

    if settings['Time keeping']: # Start timer 
        startTime = time.time()

    # Checking that geometry folder exists. 
    if os.path.isdir(settings['submission geometry path']):
        print('Checking geometries in folder: ' + settings['submission geometry path'])
    else:
        print('Submission geometry folder not found! check settings')
        return # If the folder is not found then quit. 

    # Create folder for scrutineering images. 
    rendImgPath = settings['submission geometry path'] + '\\renderedImages'
    try: 
        os.mkdir(rendImgPath)
    except:
        pass

    report = '' 
    # Check rules: 
    for rule in allRules:
        print('Checking rule: ' + rule['rule_section_name'] )

        if rule['rule_type'] == 'obscure':
            report += ruleObscure(rule, settings)
            
        elif rule['rule_type'] == 'n sections':
            report += ruleNSections(rule, settings)
    
    # Write the report file 
    print('Writing scrutineering report...')
    report = report + "NB! Geometry shouldn't touch the outer bounds of reference volumes \n"
    reportFile = settings['submission geometry path'] + "report.txt"
    with open(reportFile, "w") as f:
        f.write(report)
    
    
    # Prepairing geometries for MFlow:
    if settings['prepare geometries for Mflow']:
        print('Copying files to MFlow input folder...')

        # Create a list of folders in the submission folder. e.g. "body", "floor" etc. 
        submission_geo_folders = [d for d in os.listdir(settings['submission geometry path']) if os.path.isdir(os.path.join(settings['submission geometry path'], d))] 
        if "renderedImages" in submission_geo_folders:
            submission_geo_folders.remove("renderedImages")

        # Create input_files folder for MFlow 
        try:
            os.mkdir(settings['submission geometry path'] + '\\input_files\\')
            os.mkdir(settings['submission geometry path'] + '\\input_files\\geometry\\')
        except:
            pass
        
        # Iterate over list of geometries in submission
        for geo_folder in submission_geo_folders:

            from_folder = os.path.join(settings['submission geometry path'], geo_folder)

            try:
                # If the given folder has a specified destination, e.g body -> vehicle_body. Then this is is used as the destination for the stl's within the folder 
                to_folder = settings['sim folder repacking'][geo_folder]
            except:
                # If no destination is specified, then stl's are copied to a folder with the same name. e.g. submission/porous_media -> input_files/geometry/porous_media
                to_folder = geo_folder
            
            # Get a list of all the files
            files = [f for f in os.listdir(from_folder) if os.path.isfile(os.path.join( from_folder, f))]

            # check that the destination folder exists, if it doesnt, create it. 
            if not os.path.exists(os.path.join(settings['submission geometry path'],'input_files\\geometry\\' ,to_folder)):
                os.mkdir(os.path.join(settings['submission geometry path'],'input_files\\geometry\\' ,to_folder))
            
            # Copy all files to destination folder 
            for file in files:
                shutil.copy(os.path.join(from_folder, file), os.path.join(settings['submission geometry path'],'input_files\\geometry\\' ,to_folder, file))

    print('Done.')
    if settings['Time keeping']:
        print('Total runtime: {:.3f}'.format(time.time()-startTime)) # End timer 


### ---- Single Submission Scrutineering ---- ###
# if __name__ == '__main__':
#     from settings import *
#     from rules import *

#     scrutineer(allRules, runSettings)


### ---- Multiple Submission Scrutineering ---- ###
if __name__ == '__main__':

    # Import settings and rules
    from settings import *
    # from rules import *
    from testRules2025 import allRules # NB!NB!NB!NB! TEST RULES

    # List of submissions to test: 
    teams = [
        'test_submission_1\\',
        'test_submission_2\\',
    ]

    # Individual colors for each team, if you feel that people will not identify with red cars
    # Currently only changes illustration images for obscure rule. 
    teamColors = [
        [0.1, 0.9, 0.1], # Team 1 -> green 
        [0.9, 0.1, 0.1], # Team 2 -> red
    ]
    
    cwd_path = str(os.getcwd()) + '\\'

    for i, team in enumerate(teams):
           # Overwrite submission settings: 
        runSettings['submission geometry path'] = cwd_path + team 
        runSettings['saved image settings']['Geometry color'] = teamColors[i]
        
        scrutineer(allRules, runSettings)