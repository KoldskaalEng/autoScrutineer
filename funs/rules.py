import numpy as np

# Covers version 0.9 of the 2025 regulations 

# Define list of all rules: 
allRules = [

    ## Bodywork:

    {
        'rule_section_name': '9.1.1 - Body inside RV-Body',           # The name given to this rule in the scrutineering report 
        'rule_type': 'obscure',                     # obscure or cut-section 
        'angles': 'all',                            # Camera angles to test, currently supported: 'all', 'below', 'above' and 'sides'
        'ref_geometry': 'RV_BODY_V',   # reference geometry is colored black
        'given_geometry': 'bodywork',                   # Given geometry is colored red  
        'focus': 'given'                            # focus camera on: "reference" or "given"
    },

    {
        'rule_section_name': '9.1.2 - Obscure RS-Nose', 
        'rule_type': 'obscure',         
        'angles': 'top',           
        'ref_geometry': 'bodywork',  
        'given_geometry': 'RS_NOSE_V',                 
        'focus': 'given'                            
    },

    {
        'rule_section_name': '9.1.3 - Obscure RS-EC', 
        'rule_type': 'obscure',         
        'angles': 'sides',           
        'ref_geometry': 'bodywork',  
        'given_geometry': 'RS_EC_V',                 
        'focus': 'given'                            
    },

    {    
        'rule_section_name': '9.1.4 - Number of nose sections',           
        'rule_type': 'n sections',                      
        'angle': 'front', 
        'number_of_sections': "<= 1",  # Options: = (must be exact number), <= (up to a number)                      
        'given_geometry': 'bodywork',                                     
        'cutting_plane_normal' : [1, 0, 0],
        'sampling_method': 'semi_random', #Options: semi_random (requires max_unprobed_distance (scalar)), specific (requires probing_locations (np.array)) 
        'sampling_interval': (-1.25, 0.05),
        'max_unprobed_interval': 10e-3,
        # 'probing_locations': np.linspace(0, 1, 10),
    },

    ## Frontwing:
    {
        'rule_section_name': '10.1.1 - FW mainplane inside RV-FW-Profiles',           # The name given to this rule in the scrutineering report 
        'rule_type': 'obscure',                     # obscure or cut-section 
        'angles': 'all',                            # Camera angles to test, currently supported: 'all', 'below', 'above' and 'sides'
        'ref_geometry': 'RV_FW_Profiles_V',   # reference geometry is colored black
        'given_geometry': 'fw_mainplane',                   # Given geometry is colored red  
        'focus': 'given'                            # focus camera on: "reference" or "given"
    },

    {    
        'rule_section_name': '10.1.2 - FW mainplane number of profiles.',           
        'rule_type': 'n sections',                      
        'angle': 'left side', 
        'number_of_sections': "= 1",  # Options: = (must be exact number), <= (up to a number)                      
        'given_geometry': 'fw_mainplane',                                     
        'cutting_plane_normal' : [0, 1, 0],
        'sampling_method': 'semi_random', #Options: semi_random (requires max_unprobed_distance (scalar)), specific (requires probing_locations (np.array)) 
        'sampling_interval': (0.0, 0.575),
        'max_unprobed_interval': 10e-3,
        # 'probing_locations': np.linspace(0, 1, 10),
    },

    {
        'rule_section_name': '10.2.1 FW flaps inside RV-FW-Profiles',           # The name given to this rule in the scrutineering report 
        'rule_type': 'obscure',                     # obscure or cut-section 
        'angles': 'all',                            # Camera angles to test, currently supported: 'all', 'below', 'above' and 'sides'
        'ref_geometry': 'RV_FW_Profiles_V',   # reference geometry is colored black
        'given_geometry': 'fw_flaps',                   # Given geometry is colored red  
        'focus': 'given'                            # focus camera on: "reference" or "given"
    },

    {    
        'rule_section_name': '10.2.2 - FW flaps number of profiles.',           
        'rule_type': 'n sections',                      
        'angle': 'left side', 
        'number_of_sections': "= 2",  # Options: = (must be exact number), <= (up to a number)                      
        'given_geometry': 'fw_flaps',                                     
        'cutting_plane_normal' : [0, 1, 0],
        'sampling_method': 'semi_random', #Options: semi_random (requires max_unprobed_distance (scalar)), specific (requires probing_locations (np.array)) 
        'sampling_interval': (0.0, 0.575),
        'max_unprobed_interval': 10e-3,
        # 'probing_locations': np.linspace(0, 1, 10),
    },

    {
        'rule_section_name': '10.3 - Obscure RS-FW-Profiles', 
        'rule_type': 'obscure',         
        'angles': 'top',           
        'ref_geometry': ['fw_mainplane', 'fw_flaps'], # Combine multiple geometries this way 
        'given_geometry': 'RS_FW_PROFILES_V',                 
        'focus': 'given'                            
    },

    # FWEP
    {
        'rule_section_name': '10.4 - FWEP inside RV-FW-Endplates', 
        'rule_type': 'obscure',         
        'angles': 'all',           
        'ref_geometry': 'RV_FW_Endplates_V',  
        'given_geometry': 'fw_ep',                 
        'focus': 'given'                            
    },

    {
        'rule_section_name': '10.4 - Obscure RS-FWEP-side', 
        'rule_type': 'obscure',         
        'angles': 'sides',           
        'ref_geometry': 'fw_ep',  
        'given_geometry': 'RS_FWEP_SIDE_V',                 
        'focus': 'given'                            
    },

    {
        'rule_section_name': '10.4 - Obscure RS-FWEP-bottom', 
        'rule_type': 'obscure',         
        'angles': 'bottom',           
        'ref_geometry': 'fw_ep',  
        'given_geometry': 'RS_FWEP_bottom',                 
        'focus': 'given'                            
    },
    # FW strake
    {
        'rule_section_name': '10.5 - FW-strakes inside RV-FW-strakes', 
        'rule_type': 'obscure',         
        'angles': 'all',           
        'ref_geometry': 'RV_FW_Strakes_V',  
        'given_geometry': 'fw_strake',                 
        'focus': 'given'                            
    },

    {    
        'rule_section_name': '10.5 - FW-strakes number of Z-sections',           
        'rule_type': 'n sections',                      
        'angle': 'top', 
        'number_of_sections': "<= 4",  # Options: = (must be exact number), <= (up to a number)                      
        'given_geometry': 'fw_strake',                                     
        'cutting_plane_normal' : [0, 0, 1],
        'sampling_method': 'semi_random', #Options: semi_random (requires max_unprobed_distance (scalar)), specific (requires probing_locations (np.array)) 
        'sampling_interval': (0.075, 0.200),
        'max_unprobed_interval': 10e-3,
        # 'probing_locations': np.linspace(0, 1, 10),
    },

    {    
        'rule_section_name': '10.5 - FW-strakes number of Y-sections',           
        'rule_type': 'n sections',                      
        'angle': 'left', 
        'number_of_sections': "<= 2",  # Options: = (must be exact number), <= (up to a number)                      
        'given_geometry': 'fw_strake',                                     
        'cutting_plane_normal' : [0, 1, 0],
        'sampling_method': 'semi_random', #Options: semi_random (requires max_unprobed_distance (scalar)), specific (requires probing_locations (np.array)) 
        'sampling_interval': (0.450, 0.555),
        'max_unprobed_interval': 10e-3,
        # 'probing_locations': np.linspace(0, 1, 10),
    },

    ## Rearwing 
    {
        'rule_section_name': '11.1 - RW-mainplane inside RV-RW-profiles', 
        'rule_type': 'obscure',         
        'angles': 'all',           
        'ref_geometry': 'RV_RW_Profiles_V',  
        'given_geometry': 'rw_mainplane',                 
        'focus': 'given'                            
    },

    {    
        'rule_section_name': '11.1 - RW-mainplane number of Y-sections',           
        'rule_type': 'n sections',                      
        'angle': 'left', 
        'number_of_sections': "<= 1",  # Options: = (must be exact number), <= (up to a number)                      
        'given_geometry': 'rw_mainplane',                                     
        'cutting_plane_normal' : [0, 1, 0],
        'sampling_method': 'semi_random', #Options: semi_random (requires max_unprobed_distance (scalar)), specific (requires probing_locations (np.array)) 
        'sampling_interval': (0.0, 0.575),
        'max_unprobed_interval': 10e-3,
        # 'probing_locations': np.linspace(0, 1, 10),
    },

    {
        'rule_section_name': '11.2 - RW-flaps inside RV-RW-profiles', 
        'rule_type': 'obscure',         
        'angles': 'all',           
        'ref_geometry': 'RV_RW_Profiles_V',  
        'given_geometry': 'rw_flaps',                 
        'focus': 'given'                            
    },
    
    {    
        'rule_section_name': '11.2 - RW-flaps number of Y-sections',           
        'rule_type': 'n sections',                      
        'angle': 'left', 
        'number_of_sections': "<= 2",  # Options: = (must be exact number), <= (up to a number)                      
        'given_geometry': 'rw_flaps',                                     
        'cutting_plane_normal' : [0, 1, 0],
        'sampling_method': 'semi_random', #Options: semi_random (requires max_unprobed_distance (scalar)), specific (requires probing_locations (np.array)) 
        'sampling_interval': (0.0, 0.575),
        'max_unprobed_interval': 10e-3,
        # 'probing_locations': np.linspace(0, 1, 10),
    },

    {
        'rule_section_name': '11.3 - RW-Endplate inside RV-RWEP', 
        'rule_type': 'obscure',         
        'angles': 'all',           
        'ref_geometry': 'RV_RWEP_BODY_V',  
        'given_geometry': 'rw_ep',                 
        'focus': 'given'                            
    },

    {    
        'rule_section_name': '11.3 - RWEP number of Y-sections',           
        'rule_type': 'n sections',                      
        'angle': 'left', 
        'number_of_sections': "<= 2",  # Options: = (must be exact number), <= (up to a number)                      
        'given_geometry': 'rw_ep',                                     
        'cutting_plane_normal' : [0, 1, 0],
        'sampling_method': 'semi_random', #Options: semi_random (requires max_unprobed_distance (scalar)), specific (requires probing_locations (np.array)) 
        'sampling_interval': (0.345, 0.575),
        'max_unprobed_interval': 10e-3,
        # 'probing_locations': np.linspace(0, 1, 10),
    },

    {
        'rule_section_name': '11.3 - RW-Endplate obscures RS-RWEP', 
        'rule_type': 'obscure',         
        'angles': 'sides',           
        'ref_geometry': 'rw_ep',  
        'given_geometry': 'RS_RWEP_V',                 
        'focus': 'given'                            
    },

    {
        'rule_section_name': '11.4 - RW-Pylon inside RV-RW-PYLON', 
        'rule_type': 'obscure',         
        'angles': 'all',           
        'ref_geometry': 'RV_RW_PYLON_V',  
        'given_geometry': 'rw_pylon',                 
        'focus': 'given'                            
    },

    {    
        'rule_section_name': '11.4 - RW-PYLON number of Z-sections',           
        'rule_type': 'n sections',                      
        'angle': 'top', 
        'number_of_sections': "= 2",  # Options: = (must be exact number), <= (up to a number)                      
        'given_geometry': 'rw_pylon',                                     
        'cutting_plane_normal' : [0, 0, 1],
        'sampling_method': 'semi_random', #Options: semi_random (requires max_unprobed_distance (scalar)), specific (requires probing_locations (np.array)) 
        'sampling_interval': (0.450, 0.725),
        'max_unprobed_interval': 10e-3,
        # 'probing_locations': np.linspace(0, 1, 10),
    },

    ### FLOOR
    {
        'rule_section_name': '12.1 - floor_body inside RV-floor', 
        'rule_type': 'obscure',         
        'angles': 'all',           
        'ref_geometry': 'RV_FLOOR_V',  
        'given_geometry': 'floor_body',                 
        'focus': 'given'                            
    },

    {    
        'rule_section_name': '12.1 - floor_body number of Z-sections',           
        'rule_type': 'n sections',                      
        'angle': 'top', 
        'number_of_sections': "<= 2",  # Options: = (must be exact number), <= (up to a number)                      
        'given_geometry': 'floor_body',                                     
        'cutting_plane_normal' : [0, 0, 1],
        'sampling_method': 'semi_random', #Options: semi_random (requires max_unprobed_distance (scalar)), specific (requires probing_locations (np.array)) 
        'sampling_interval': (0.035, 0.275),
        'max_unprobed_interval': 10e-3,
        # 'probing_locations': np.linspace(0, 1, 10),
    },

    {    
        'rule_section_name': '12.1 - floor_body top bottom visibility, X-sections',   # You probably need to test both x sections and y sections        
        'rule_type': 'top bottom visibility',                      
        'angle': 'front',
        'number_of_intersections': "<= 2", # 2 intersections means top and bottom visible. more than 2 means something is overhanging.                              
        'given_geometry': 'floor_body',                                     
        'cutting_plane_normal' : [1, 0, 0],
        # 'sampling_method': 'specific',
        'sampling_method': 'semi_random',
        'sampling_interval': (0.350, 3.750),
        'max_unprobed_interval': 10e-3,
        # 'probing_locations': np.array([ 0.175 ]),
    },

    {    
        'rule_section_name': '12.1  - floor_body top bottom visibility, Y-sections',   # You probably need to test both x sections and y sections        
        'rule_type': 'top bottom visibility',                      
        'angle': 'left side',
        'number_of_intersections': "<= 2", # 2 intersections means top and bottom visible. more than 2 means something is overhanging.                              
        'given_geometry': 'floor_body',                                     
        'cutting_plane_normal' : [0, 1, 0],
        # 'sampling_method': 'specific',
        'sampling_method': 'semi_random',
        'sampling_interval': (0.0, 0.770),
        'max_unprobed_interval': 10e-3,
        # 'probing_locations': np.array([ 0.175 ]),
    },

    {
        'rule_section_name': '12.1  - floor_body obscures RS- floor-step, floor-ref and floor-body', 
        'rule_type': 'obscure',         
        'angles': 'bottom',           
        'ref_geometry': 'floor_body',  
        'given_geometry': ['RS_FLOOR_STEP_V', 'RS_FLOOR_REF_V', 'RS_FLOOR_BODY_V'],                 
        'focus': 'given'                            
    },

    {
        'rule_section_name': '12.1  - floor_body obscures bodywork', 
        'rule_type': 'obscure',         
        'angles': 'bottom',           
        'ref_geometry': ['floor_body', 'RS_FLOOR_MASK_V'],  
        'given_geometry': 'bodywork',                 
        'focus': 'given'                            
    },

    {
        'rule_section_name': '12.2 - floor_board inside RV-floorboard', 
        'rule_type': 'obscure',         
        'angles': 'all',           
        'ref_geometry': 'RV_FLOOR_BOARD_V',  
        'given_geometry': 'floor_board',                 
        'focus': 'given'                            
    },

    {
        'rule_section_name': '12.2 - floor_board obscures RS-FLOOR-BOARD', 
        'rule_type': 'obscure',         
        'angles': 'sides',           
        'ref_geometry': 'floor_board',  
        'given_geometry': 'RS_FLOOR_BOARD_V',                 
        'focus': 'given'                            
    },

    {
        'rule_section_name': '12.2 - floor_board obscures RS-FLOOR-FOOT', 
        'rule_type': 'obscure',         
        'angles': 'top',           
        'ref_geometry': 'floor_board',  
        'given_geometry': 'RS_FLOOR_FOOT_V',                 
        'focus': 'given'                            
    },

    {
        'rule_section_name': '12.3 - floor_LEDs inside RV-floor_LED', 
        'rule_type': 'obscure',         
        'angles': 'all',           
        'ref_geometry': 'RV_FLOOR_LED_V',  
        'given_geometry': 'floor_led',                 
        'focus': 'given'                            
    },

    {
        'rule_section_name': '12.3 - floor_fence inside RV-floor_fence', 
        'rule_type': 'obscure',         
        'angles': 'all',           
        'ref_geometry': 'RV_FLOOR_FENCE_V',  
        'given_geometry': 'floor_fence',                 
        'focus': 'given'                            
    },

    ### Mirrors

    {
        'rule_section_name': '13 - mirrors inside RV-mirrors-support', 
        'rule_type': 'obscure',         
        'angles': 'all',           
        'ref_geometry': 'RV_MIRRORS_SUPPORT_V',  
        'given_geometry': 'mirror',                 
        'focus': 'given'                            
    },

    ### Suspension

    {
        'rule_section_name': '14 - front suspension inside RVs', 
        'rule_type': 'obscure',         
        'angles': 'all',           
        'ref_geometry': ['RV_FBrake_duct_frt_V', 'RV_Suspension_cover_FL_V', 'RV_Suspension_cover_FR_V'],  
        'given_geometry': ["frt_suspension_arms", "frt_suspension_hub"],                 
        'focus': 'given'                            
    },

    {
        'rule_section_name': '14 - rear suspension inside RVs', 
        'rule_type': 'obscure',         
        'angles': 'all',           
        'ref_geometry': ['RV_FBrake_duct_rr_V', 'RV_Suspension_cover_RL_V', 'RV_Suspension_cover_RR_V'],  
        'given_geometry': ["rr_suspension_arms", "rr_suspension_hub"],                 
        'focus': 'given'                            
    },

]