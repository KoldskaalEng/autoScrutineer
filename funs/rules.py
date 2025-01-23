import numpy as np

# Define list of all rules: 
allRules = [
    {
        'rule_section_name': '9.1-BODY',           # The name given to this rule in the scrutineering report 
        'rule_type': 'obscure',                     # obscure or cut-section 
        'angles': 'all',                            # Camera angles to test, currently supported: 'all', 'below', 'above' and 'sides'
        'ref_geometry': 'RV_Vehiclebody_MVRC_V',   # reference geometry is colored black
        'given_geometry': 'body',                   # Given geometry is colored red 
        'mask': 'MandParts',                        # Maks are colored black, can be used to section off some areas.  
        'focus': 'given'                            # focus camera on: "reference", "given" or "mask" 
    },

    {
        'rule_section_name': '9.8-FRT_WHL_DEFL',
        'rule_type': 'obscure',
        'angles': 'all',
        'ref_geometry': 'RV_FRT_WHL_DEFL_V', 
        'given_geometry': 'frt_suspension', 
        'mask': 'none', 
        'focus': 'given'
    },

    {
        'rule_section_name': '9.8-RR_Winglet',
        'rule_type': 'obscure',
        'angles': 'all',
        'ref_geometry': 'RV_RR_WHL_Winglet_V', 
        'given_geometry': 'rr_suspension', 
        'mask': 'none',   
        'focus': 'given'
    },

    {
        'rule_section_name': '10.1',
        'rule_type': 'obscure',
        'angles': 'all',
        'ref_geometry': 'RV_FRT_WING_VOL_V', 
        'given_geometry': 'front_wing',  
        'mask': 'none',   
        'focus': 'given'
    },

    {
        'rule_section_name': '10.5',
        'rule_type': 'obscure',
        'angles': 'below',
        'ref_geometry': 'front_wing', 
        'given_geometry': 'RS-FW-PROFILES_V', 
        'mask': 'none',   
        'focus': 'given'
    },

    {
        'rule_section_name': '10.6',
        'rule_type': 'obscure',
        'angles': 'sides',
        'ref_geometry': 'front_wing', 
        'given_geometry': 'RS-FWEP-BODY_V', 
        'mask': 'none',   
        'focus': 'given'
    },

    {
        'rule_section_name': '11.1',
        'rule_type': 'obscure',
        'angles': 'all',
        'ref_geometry': 'RV_REARWING_V', 
        'given_geometry': 'rear_wing', 
        'mask': 'none',   
        'focus': 'given'
    },

    {
        'rule_section_name': '11.4',
        'rule_type': 'obscure',
        'angles': 'sides',
        'ref_geometry': 'rear_wing', 
        'given_geometry': 'RS-RW-RWEP_V', 
        'mask': 'none',   
        'focus': 'given'
    },

    {
        'rule_section_name': '12.1',
        'rule_type': 'obscure',
        'angles': 'all',
        'ref_geometry': 'RV_FLOOR_BODY_V', 
        'given_geometry': 'floor', 
        'mask': 'none',   
        'focus': 'given'
    },

    {
        'rule_section_name': '12.2.1',
        'rule_type': 'obscure',
        'angles': 'below',
        'ref_geometry': 'floor', 
        'given_geometry': 'RS_FLOOR-PLAN_V', 
        'mask': 'none',   
        'focus': 'given'
    },

    {
        'rule_section_name': '12.2.2',
        'rule_type': 'obscure',
        'angles': 'sides',
        'ref_geometry': 'floor', 
        'given_geometry': 'RS_FLOOR_REAR_V', 
        'mask': 'none',   
        'focus': 'reference'
    },

    {
        'rule_section_name': '12.5',
        'rule_type': 'obscure',
        'angles': 'below',
        'ref_geometry': 'floor', 
        'given_geometry': 'body', 
        'mask': 'RS_FLOOR_MASK_V',   
        'focus': 'reference'
    },

    {
        'rule_section_name': '12.6',
        'rule_type': 'obscure',
        'angles': 'all',
        'ref_geometry': 'RV_FLOOR_FENCE_V', 
        'given_geometry': 'fences', 
        'mask': 'none',   
        'focus': 'given'
    },

    {
        'rule_section_name': '13.2',
        'rule_type': 'obscure',
        'angles': 'all',
        'ref_geometry': 'RV_Mirror_Strut_MVRC_V', 
        'given_geometry': 'mirror_strut', 
        'mask': 'none',   
        'focus': 'given'
    },
]


## Define "cut-section"-rules
# rule9_6 = {
#     'rule_section_name': '9.6',
#     'rule_type': 'cut-section',
#     'angles': 'front', 
#     'plane normal axis': [1, 0, 0], # x section = [1, 0, 0], y = [0, 1, 0], you get the point... 
#     'cut planes': np.linspace(-0.85, 0, 5), # planes are this distance along normal axis, from the origin, so if plane normal is [1, 0, 0], then the numbers given here are x-coords for the cutplanes.  
#     'strict planes': False, # if True then the the exact coordinates for cut planes will be used. If False then some randomness will be added.
#     'min plane': -0.9,
#     'max plane': 0.0, # if strict planes is false, then this value is the highest allowed 
#     'sigma': 0.15, # std. dev. for the random value to be added to cut planes
#     'ref_geometry': 'RS_NOSE_AREA_V*', # Reference used to calibrate section area calculations 
#     'given_geometry': 'body', # parts to be cut  
#     'mask': 'none',   
#     'focus': 'given',
#     'max area': 'none',
#     'min area': 'none',
#     'max number of sections': 1,
#     'min number of sections': 'none'
# }

# rule9_7 = {
#     'rule_section_name': '9.7',
#     'rule_type': 'cut-section',
#     'angles': 'front', 
#     'plane normal axis': [1, 0, 0], # x section = [1, 0, 0], y = [0, 1, 0], you get the point... 
#     'cut planes': [-0.55], # origin point for the cutting planes are the scalars in this list*normalaxis above. So if plane normal is [1, 0, 0], then the numbers given here are x-coords for the cutplanes.  
#     'strict planes': True, # if True then the the exact coordinates for cut planes will be used. If False then some randomness will be added.
#     'min plane': 'none',
#     'max plane': 'none', # if strict planes is false, then this value is the highest allowed 
#     'sigma': 'none', # std. dev. for the random value to be added to cut planes
#     'ref_geometry': 'RS_NOSE_AREA_V*', # Reference used to calibrate section area calculations 
#     'given_geometry': 'body', # parts to be cut  
#     'mask': 'none',   
#     'focus': 'given',
#     'max area': 'none',
#     'min area': 0.044, # fraction of the reference geometry, reference = 1m2 = 1e6mm2, minimum area = 44e3mm2 -> 1e6/44e3 = 0.044
#     'max number of sections': 'none',
#     'min number of sections': 'none'
# }


# Now it should be possible to access the rules by simply importing this module 