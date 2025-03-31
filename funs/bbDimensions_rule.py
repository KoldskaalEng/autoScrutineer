import numpy as np
from vtk_funs import *
from settings import *

def rulebbdimensions(rule, settings):
    """Determine if the geometry can fit within a bouning-box of a certain size"""

    list_of_paths = get_list_of_paths( rule["given_geometry"] )
    actor = read_stls( list_of_paths, offset6dir= False)
    bbcords, _, _ = getBoundingBoxCoords_actor(actor)
    # BBcords format: (xmin, xmax, ymin, ymax, zmin, zmax)

    violation = False
    size = []
    # print(bbcords)
    for i in range(3):
        size.append( bbcords[2*i + 1] - bbcords[2*i] )
        if np.isnan(rule['max dimensions'][i]):
            pass
        if size[i] > rule['max dimensions'][i]:
            violation = True
    
    if violation:
        reportStr = 'Violates {}\n'.format(rule['rule_section_name'])
        reportStr += '    Bounding box coordinates for the part are: [{:.4f}, {:.4f}, {:.4f}].\n'.format(size[0], size[1], size[2])
        reportStr += '    But it should be smaller than: [{:.4f}, {:.4f}, {:4f}].\n'.format(rule['max dimensions'][0], rule['max dimensions'][1], rule['max dimensions'][2])
    else: 
        reportStr = 'Complies with {}\n'.format(rule['rule_section_name'])

    return reportStr


def test():

    rule = {
        'rule_section_name': '§ bounding box dimensions test rule',
        'rule_type': 'bbdimensions',
        'given_geometry': 'rw_flaps', 
        'max dimensions': np.array( [np.nan, 0.4, 0.1 ] ) # nan = not applicable / ignore 
    }
    
    print(rulebbdimensions(rule, runSettings))

if __name__ == "__main__":
    test()