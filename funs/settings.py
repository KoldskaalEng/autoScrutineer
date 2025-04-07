import os

savedImageSettings = {
    'Geometry color': [0.9, 0.1, 0.1],
    'Background color': [0.2, 0.2, 0.2],
    'Reference geometry color': [0.05, 0.05, 0.05],
    'Reference geometry opacity': 0.1,
    'Save all non-compliant images': True, # Set to True to save ALL non-complying images. If False then only the first violation is saved. 
    # Saving all images obv. takes longer time. 
}

hires = "high_res_surfaces"
vb = "vehicle_body"

scrutineering2simulationFolder = { #Specifies which folder to place the different parts in. 
    "special_bc": "special_bc",
    "monitoring_surfaces": "monitoring_surfaces",
    "porous_media": "porous_media", 
    "frt_suspension_arms": "frt_suspension",
    "frt_suspension_hub": "frt_suspension",
    "rr_suspension_arms": "rr_suspension",
    "rr_suspension_hub": "rr_suspension",
    'bodywork': vb,
    'fw_mainplane': hires,
    'fw_flaps': hires,
    'fw_ep': hires,
    'fw_strake': hires,
    'floor_body': vb,
    'floor_board': hires,
    'floor_led': hires,
    'floor_fence': hires,
    'rw_mainplane': hires,
    'rw_flaps': hires,
    'rw_ep': hires,
    'rw_pylon': hires,
    'mirror': hires, 
} # Anything not in this dict, will be placed in a folder of the same name as the in the submission folder. e.g. submission/POROUS_MEDIA/part.stl is copied to input_files/POROUS_MEDIA/part.stl

runSettings = {
    # 'official geometry path': 'referenceGeometry\\',# Keep all official geoemtries in one folder. RVs, RSs and MAND_
    # 'official geometry prefix': ('RV-', 'RV_', 'RS-', 'RS_', 'MAND_', 'MAND-'),
    # 'submission geometry path': 'test_submission_1\\',
    # # 'submission geometry path': 'Koldskaal_Rd1\\', # For example
    'saved image settings': savedImageSettings,
    'Time keeping': True,
    'Verbose scrutineering': True,
    'sim folder repacking': scrutineering2simulationFolder,
    'prepare geometries for Mflow': True,

}
#
# # It seems that VTK does not understand pathlike objects, so paths are given as strings
# cwd_path = str(os.getcwd()) + '\\'
#
# runSettings['submission geometry path'] = cwd_path + runSettings['submission geometry path']
# runSettings['official geometry path'] =  cwd_path + runSettings['official geometry path']
