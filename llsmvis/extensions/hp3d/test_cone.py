import surface_morphometrics as sm

sm.get_cone(r'C:\Users\miao1\Data\h3pd\cone test 1\cone_test.stl')

#sm.get_cell_cone_intersection(r'C:\Users\miao1\Data\h3pd\cone test 1\sphere.stl', r'C:\Users\miao1\Data\h3pd\cone test 1\cone.stl', r'C:\Users\miao1\Data\h3pd\cone test 1\intersect.stl')

sm.get_cut(r'C:\Users\miao1\Data\h3pd\cone test 2\cell.stl', r'C:\Users\miao1\Data\h3pd\cone test 2\cone.stl', r'C:\Users\miao1\Data\h3pd\cone test 2\cut_cell.stl', r'C:\Users\miao1\Data\h3pd\cone test 2\cut_protrusion.stl', r'C:\Users\miao1\Data\h3pd\cone test 2\cone_protrusion.stl')

cut_protrusion_prop = sm.get_volume_surface_area(r'C:\Users\miao1\Data\h3pd\cone test 2\cut_protrusion.stl')
cone_protrusion_prop = sm.get_volume_surface_area(r'C:\Users\miao1\Data\h3pd\cone test 2\cone_protrusion.stl')

print('volume of cone and protrusion', cone_protrusion_prop[0])
print('surface area protrusion', cut_protrusion_prop[1])
#print('intersection surface area and volume', sm.calc_morphometrics(r'C:\Users\miao1\Data\h3pd\cone test\intersect.stl'))
