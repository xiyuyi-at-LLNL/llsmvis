import surface_morphometrics as sm

sm.get_cone(r'C:\Users\miao1\Data\h3pd\cone test\cone_test.stl')

sm.get_cell_cone_intersection(r'C:\Users\miao1\Data\h3pd\cone test\sphere.stl', r'C:\Users\miao1\Data\h3pd\cone test\cone.stl', r'C:\Users\miao1\Data\h3pd\cone test\intersect.stl')

print('intersection surface area and volume', sm.calc_morphometrics(r'C:\Users\miao1\Data\h3pd\cone test\intersect.stl'))