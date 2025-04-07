# Automatic Scrutineering script by 'Koldskaal' on f1Technical
# For use in MVRC: https://mantiumchallenge.com/

import os
import sys
import argparse
import time
import shutil
from obscure_rule import ruleObscure
from nSections_rule import ruleNSections
from topBottomVis_rule import ruleTopBottomVisibility
from vtk_funs import get_stl_geometries

# Scrutineer a single submission: 
def scrutineer(allRules, settings):

    if settings['Time keeping']: # Start timer 
        startTime = time.time()

    # Checking that geometry folder exists. 
    if not os.path.isdir(settings['submission geometry path']):
        sys.exit('Submission geometry folder not found!\nPlease provide valid folder!')

    report = '' 
    legalFolders = list(set(settings['sim folder repacking'].values()))
    geo_path = os.path.join(settings['submission geometry path'], 'input_files', 'geometry')
    # Checking the folders in the submission folder. 
    folders = [f for f in os.listdir(geo_path) if f in legalFolders]
    wrongFolders = []
    for folder in folders:
        if folder not in legalFolders:
            wrongFolders.append(folder)
    if len(wrongFolders) > 0:
        report += "Wrongly named folders detected: " + ", ".join(wrongFolders) + "\n"
        report += "These will not be included in input_files!\n"

    # Create folder for scrutineering images. 
    rendImgPath = os.path.join(settings['submission geometry path'], 'autoScrut_renderedImages')
    if not os.path.exists(rendImgPath):
        os.makedirs(rendImgPath)

    # Check rules: 
    for rule, rule_settings in allRules.items():
        print('Checking rule: ' + rule)
        if rule_settings['rule_type'] == 'obscure':
            report += ruleObscure(rule_settings, settings)
            
        elif rule_settings['rule_type'] == 'n sections':
            report += ruleNSections(rule_settings, settings)

        elif rule_settings['rule_type'] == 'top bottom visibility':
            report += ruleTopBottomVisibility(rule_settings, settings)
    
    # Write the report file 
    print('Writing scrutineering report...')
    reportFile = os.path.join(settings['submission geometry path'], "scrutineering_report.txt")
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


### ---- Multiple Submission Scrutineering ---- ###
if __name__ == '__main__':

    # Import settings and rules
    from settings import *
    from rules import * # Full list of proper rules!
    # from testRules2025 import allRules # NB! ONLY TEST RULES

    parser = argparse.ArgumentParser(description="autoScrut checks MVRC entries against many rules described on the challenge homepage.")

    parser.add_argument(
        '-sf',
        '--submission-folders',
        nargs='+',  # accepts one or more values
        required=True,
        help='Define one or multiple folders to check.'
    )

    parser.add_argument(
        '-rg',
        '--reference-geometry-folder',
        required=True,
        help='Specify folder with reference CAD stl files, provided by MVRC.'
    )

    args = parser.parse_args()

    runSettings['reference_geometries'] = get_stl_geometries(args.reference_geometry_folder)
    for folder in args.submission_folders:
        # Overwrite submission settings:
        runSettings['submission geometry path'] = folder
        runSettings['saved image settings']['Geometry color'] = [0.8, 0.8, 0.8] # Grey, colors could later get defined in args
        runSettings['submission_geometries'] = get_stl_geometries(os.path.join(folder,'input_files'))
        # runSettings['official geometry path'] = args.reference_geometry_folder

        scrutineer(allRules, runSettings)
