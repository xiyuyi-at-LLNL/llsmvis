import surface_morphometrics

th = 600
fpath = r'C:\Users\miao1\Data\focused-fast-scans\trimmed_stacks\Trimmed_cell3_Iter_0_ch0_stack0000_3nm_0000000msec_0009286310msecAbs.tif'
output_dir = r'C:\Users\miao1\Data\focused-fast-scans\trimmed_stacks'
save_mask=True
surface_smoothing_steps = 10

output_file = surface_morphometrics.extract_surface(th, fpath=fpath, output_dir=output_dir, kernel_size=3, save_mask=True, surface_smoothing_steps=surface_smoothing_steps)

print(surface_morphometrics.calc_morphometrics(output_file))