"""
Haichao Miao @ LLNL, 2021.
"""
import vtk
import numpy as np
import os
import surface_morphometrics as sm


def test_protrusion_volume():
    sm.get_cut(r'C:\Users\miao1\Data\h3pd\cone test 2\cell.stl', r'C:\Users\miao1\Data\h3pd\cone test 2\cone_2.stl', r'C:\Users\miao1\Data\h3pd\cone test 2\cut_cell.stl', r'C:\Users\miao1\Data\h3pd\cone test 2\cut_protrusion.stl', r'C:\Users\miao1\Data\h3pd\cone test 2\cone_protrusion.stl')
    
    cell_prop = sm.get_volume_surface_area(r'C:\Users\miao1\Data\h3pd\cone test 2\cell.stl')
    cut_cell_prop = sm.get_volume_surface_area(r'C:\Users\miao1\Data\h3pd\cone test 2\cut_cell.stl')
    cut_protrusion_prop = sm.get_volume_surface_area(r'C:\Users\miao1\Data\h3pd\cone test 2\cut_protrusion.stl')
    
    print("volumes:")    
    print("\t cut cell: \t \t {}".format(cut_cell_prop[0]))    
    print("\t cut protrusion: \t {}".format(cut_protrusion_prop[0]))    
    print("\t difference: \t {}".format(cell_prop[0] - (cut_cell_prop[0] + cut_protrusion_prop[0])))

    print("surface area:")    
    print("\t cell: \t \t \t {}".format(cell_prop[1]))    
    print("\t cut cell: \t \t {}".format(cut_cell_prop[1]))    
    print("\t cut protrusion: \t {}".format(cut_protrusion_prop[1]))    
    print("\t difference: \t {}".format(cell_prop[1] - (cut_cell_prop[1] + cut_protrusion_prop[1])))
    
test_protrusion_volume()