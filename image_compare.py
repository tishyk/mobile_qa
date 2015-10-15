import os
import time
from PIL import Image
from PIL import ImageColor

os.popen("adb start-server")
deviceId = os.popen("adb get-serialno").readline().strip()
test_name = "test_1"
sname = test_name

def get_image_from_device(deviceId,test_name,sname):
    os.popen("adb -s {0} shell mkdir -p /sdcard/temp/".format(deviceId))
    os.popen("adb -s {0} shell screencap /sdcard/temp/{1}.png".format(deviceId,test_name))
    os.popen("adb -s {0} pull /sdcard/temp/{1}.png C:/{2}.png".format(deviceId,test_name,sname)).read()
    os.popen("adb -s {0} shell rm /sdcard/temp/*.png".format(deviceId))

get_image_from_device(deviceId,test_name,test_name) 

device_image = Image.open("C:/{0}.png".format(sname))

path_origin = "C:/originscreenshot/{0}/{0}.png".format(test_name)
path_current = "C:/{0}.png".format(sname)

def image_compare(path_origin,path_current,perc=100):
    '''image_compare function
    args - path_to origin screenshot,path_to screenshot for compare, type "str"
    compare percent (default = 100%, no difference between screenshot), type "int")
    '''
    original_image = Image.open(path_origin)
    width,height = origin_size = original_image.size
    device_image = Image.open(path_current)
    im_diff=original_image.copy()
    pixel_count = 0

    assert (origin_size==device_image.size),"Fatal Error!!! Images has different height or weight!!!"

    for x in xrange(width):
        for y in xrange(0,height):
            cur_pixel = original_image.getpixel((x,y))
            if cur_pixel!=device_image.getpixel((x,y)):
                pixel_count+=1
                if pixel_count==1:
                    im_diff=original_image.copy()
                im_diff.putpixel((x, y), ImageColor.getcolor('darkred', 'RGBA'))
                
    diff_percent = round(float(pixel_count)*100/(width*height),2)
    print "Image compare: {0}% difference from original screenshot".format(diff_percent)
    im_diff.save("C:/{0}_diff.png".format(test_name))
    if perc>100-diff_percent:
        return False
    else:
        return True
    
time.clock()
print image_compare(path_origin,path_current,94)
print time.clock()