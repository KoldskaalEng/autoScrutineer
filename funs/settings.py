
savedImageSettings = {
    'Geometry color': [0.9, 0.1, 0.1],
    'Background color': [0.1, 0.1, 0.1],
    'Reference geometry color': [0.05, 0.05, 0.05],
    'Reference geometry opacity': 0.5,
    'Save all non-compliant images': False, # Set to True save ALL non-complying images. Default: False i.e. save only the first infringement, and then stop checking. 
    
}

scrutineering2simulationFolder = { #Specifies which folder to place the different parts in. 
    'body': 'vehicle_body',
    'fences': 'high_res_surfaces',
    'floor': 'vehicle_body',
    'front_wing': 'high_res_surfaces',
    'mirror_strut': 'vehicle_body', 
    'rear_wing': 'high_res_surfaces', 
} # Anything not in this dict, will be placed in a folder of the same name as the in the submission folder. e.g. submission/POROUS_MEDIA/part.stl is copied to input_files/POROUS_MEDIA/part.stl

runSettings = {
    'reference geometry path': 'referenceGeometry\\',
    'submission geometry path': 'team1_submission\\',
    # 'submission geometry path': 'Koldskaal_RD1\\',
    'mandatory geometry path': 'mandParts\\',
    'saved image settings': savedImageSettings,
    'Timed running': True,
    'sim folder repacking': scrutineering2simulationFolder,
    'prepare geometries for Mflow': True,

}