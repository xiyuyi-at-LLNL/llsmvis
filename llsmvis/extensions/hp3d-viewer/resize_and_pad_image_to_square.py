from PIL import Image, ImageOps
import cv2

desired_size = 368
im_pth = "F:\Papers\Xiyu\compiled_hp3d_report_elements\hp3d\2021-09-22-cell3\check_mass_center_on_smip_XY.png"

# im = Image.open(im_pth)
# old_size = im.size  # old_size[0] is in (width, height) format

# ratio = float(desired_size)/max(old_size)
# new_size = tuple([int(x*ratio) for x in old_size])

## using thumbnai() or resize() method to resize the input image and keep its aspect ratio
# im.thumbnail(new_size, Image.ANTIALIAS)
# im = im.resize(new_size, Image.ANTIALIAS) 

## create a new square image with desired size and paste the resized image onto it. 
# new_im = Image.new("RGB", (desired_size, desired_size))
# new_im.paste(im, ((desired_size-new_size[0])//2,
#                       (desired_size-new_size[1])//2))

## or we can expand the resized image by adding borders to its 4 side
# delta_w = desired_size - new_size[0]
# delta_h = desired_size - new_size[1]
# padding = (delta_w//2, delta_h//2, delta_w-(delta_w//2), delta_h-(delta_h//2))
# print(padding)
# new_im = ImageOps.expand(im, padding, fill="black")
# new_im.show()

## opencv has copyMakeBorder() method which is handy for making borders
im = cv2.imread(im_pth)
old_size = im.shape[:2] # old_size is in (height, width) format
ratio = float(desired_size)/max(old_size)
new_size = tuple([int(x*ratio) for x in old_size])

# new_size should be in (width, height) format
im = cv2.resize(im, (new_size[1], new_size[0])) 

delta_w = desired_size - new_size[1]
delta_h = desired_size - new_size[0]
top, bottom = delta_h//2, delta_h-(delta_h//2)
left, right = delta_w//2, delta_w-(delta_w//2)

color = [0, 0, 0]
new_im = cv2.copyMakeBorder(im, top, bottom, left, right, cv2.BORDER_CONSTANT,
    value=color)

cv2.imshow("image", new_im)
cv2.waitKey(0)
cv2.destroyAllWindows()