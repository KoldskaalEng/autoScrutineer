import numpy as np

# List of all rules: 
allRules = [
    {
        'rule_section_name': '§1.0',                 # The name given to this rule in the scrutineering report 
        'rule_type': 'obscure',                     # obscure or n sections
        'angles': 'all',                            # Camera angles to test, currently supported: 'all', 'below', 'above' and 'sides'
        'ref_geometry': 'RV-RW-PROFILES_v',         # reference geometry is colored black
        'given_geometry': 'rw_mainplane',           # Given geometry is colored red 
        'mask': 'none',                             # Maks are colored black, can be used to section off some areas.  
        'focus': 'given'                            # focus camera on: "reference", "given" or "mask" 
    },

    {
        'rule_section_name': '§1.1',
        'rule_type': 'obscure',
        'angles': 'all',
        'ref_geometry': 'RV-RW-PROFILES_v', 
        'given_geometry': 'rw_flaps', 
        'mask': 'none', 
        'focus': 'given'
    },

    {
        'rule_section_name': '§1.2',
        'rule_type': 'obscure',
        'angles': 'all',
        'ref_geometry': 'RV-RWEP-BODY_v', 
        'given_geometry': 'rw_endplate', 
        'mask': 'none',   
        'focus': 'given'
    },

    {
        'rule_section_name': '§1.3',
        'rule_type': 'obscure',
        'angles': 'all',
        'ref_geometry': 'RV-RW-PYLON_v', 
        'given_geometry': 'rw_pylon',  
        'mask': 'none',   
        'focus': 'given'
    },

    {    
        'rule_section_name': '§2.0, mainplane sections',           
        'rule_type': 'n sections',                      
        'angle': 'left side',
        'number_of_sections': "= 1",                              
        'given_geometry': 'rw_mainplane',                                     
        'cutting_plane_normal' : [0, 1, 0],
        # 'sampling_method': 'specific',
        'sampling_method': 'semi_random',
        'sampling_interval': (0.0, 0.535),
        'max_unprobed_interval': 25e-3,
        # 'probing_locations': np.array([ 0.25 ]),
    },

    {    
        'rule_section_name': '§2.1, flap sections',           
        'rule_type': 'n sections',                      
        'angle': 'left side', 
        'number_of_sections': "<= 2",  # Options: = (must be exact number), <= (up to a number)                      
        'given_geometry': 'rw_mainplane',                                     
        'cutting_plane_normal' : [0, 1, 0],
        'sampling_method': 'semi_random', #Options: semi_random (requires max_unprobed_distance (scalar)), specific (requires probing_locations (np.array)) 
        'sampling_interval': (0.0, 0.535),
        'max_unprobed_interval': 25e-3,
        # 'probing_locations': np.linspace(0, 1, 10),
    },
]
