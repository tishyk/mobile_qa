import os

def conversion(command):
    device_id = 'aasafafafaff'
    #Get current coord (x , y) from command adb shell input tap x y
    to_int = lambda lst: [int(i) for i in lst]
    x1, y1 = to_int(command.split()[-2:])
    x_bm, y_bm = 1280, 800
    # get max coordinates x,y for tested device " Physical size: 480x800"
    answer = os.popen('adb -s %s shell wm size'%device_id).readline()
    assert ("Physical size:" in answer), 'Command "adb -s %s shell wm size" failed!'%device_id
    x_cm, y_cm = to_int((answer.split()[-1]).split('x'))
    ky1 = x_cm/x_bm
    kx1 = y_cm/y_bm
    x2 = x_cm-y1*kx1
    y2 = kx1*x1
    print 'Coord: old: (%s,%s)/ new: (%s,%s)'%(x1,y1,x2,y2)
    return os.popen('adb shell input tap %i %i'%(x2,y2))
    
os.system = conversion
os.system('adb shell input tap 165 250').read()



