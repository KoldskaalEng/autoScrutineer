# Automatic Scrutineering script by 'Koldskaal' on f1Technical
# For use in MVRC: https://mantiumchallenge.com/

import os
import time
import shutil
from obscure_rule import ruleObscure
from nSections_rule import ruleNSections
from topBottomVis_rule import ruleTopBottomVisibility

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

    report = '' 
    # Checking the folders in the submission folder. 
    folders = [f for f in os.listdir(settings['submission geometry path']) if os.path.isdir(os.path.join(settings['submission geometry path'], f))]
    wrongFolders = []
    legalFolders = list( settings['sim folder repacking'].keys() )
    for folder in folders:
        if not folder in legalFolders:
            wrongFolders.append(folder)
    if wrongFolders:
        report += "Wrongly named folders detected: " + ", ".join(wrongFolders) + "\n"
        report += "These will not be included in input_files!\n"
    
    # Create folder for scrutineering images. 
    rendImgPath = settings['submission geometry path'] + '\\renderedImages'
    try: 
        os.mkdir(rendImgPath)
    except:
        pass

    # Check rules: 
    for rule in allRules:
        print('Checking rule: ' + rule['rule_section_name'] )

        if rule['rule_type'] == 'obscure':
            report += ruleObscure(rule, settings)
            
        elif rule['rule_type'] == 'n sections':
            report += ruleNSections(rule, settings)
        
        elif rule['rule_type'] == 'top bottom visibility':
            report += ruleTopBottomVisibility(rule, settings)
    
    # Write the report file 
    print('Writing scrutineering report...')
    reportFile = settings['submission geometry path'] + "scrutineering_report.txt"
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

            if geo_folder in legalFolders:
                from_folder = os.path.join(settings['submission geometry path'], geo_folder)
                # If the given folder has a specified destination, e.g body -> vehicle_body. Then this is is used as the destination for the stl's within the folder 
                try:
                    to_folder = settings['sim folder repacking'][geo_folder]
                except:
                    # If no destination is specified, then stl's are copied to a folder with the same name. e.g. submission/porous_media -> input_files/geometry/porous_media
                    to_folder = geo_folder
            
                # Get a list of all the files
                files = [f for f in os.listdir(from_folder) if all( [os.path.isfile(os.path.join( from_folder, f)), f.lower().endswith(".stl") ]) ]

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
    from rules import * # Full list of proper rules!
    # from testRules2025 import allRules # NB! ONLY TEST RULES

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