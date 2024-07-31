thresholds = [(0, 100, -41, 108, -40, 113)]


import pyb
import sensor,image, time,math
from pyb import LED,Timer,UART
sensor.reset()  #初始化摄像头
sensor.set_pixformat(sensor.RGB565)    #设置摄像头格式
sensor.set_framesize(sensor.QVGA)      #设置像素格式
sensor.skip_frames(time = 2000)        #减少捕获到无效信息，所以我们跳过一段时间再进行后续的工作

sensor.set_auto_gain(False)    #关闭自动增益
sensor.set_auto_whitebal(False)     #关闭白平衡

clock = time.clock()

img = sensor.snapshot()    #捕获图片
#使用遍历的方式进行色块的寻找
for blob in img.find_blobs([thresholds[0]], pixels_threshold=200, area_threshold=200, merge=True):
    if blob.elongation() > 0.5:
        #下面三行代码分别是使用不同的颜色画出方框、中心十字、和横线，这三行代码可有可无不做要求
        img.draw_edges(blob.min_corners(), color=(255,0,0))
        img.draw_line(blob.major_axis_line(), color=(0,255,0))
        img.draw_line(blob.minor_axis_line(), color=(0,0,255))

        #下面的代码是稳定的，也就是不需要我们再次进行参数的设置
        img.draw_rectangle(blob.rect())    #画出矩形框
        img.draw_cross(blob.cx(), blob.cy())    #画中心位置的十字

        img.draw_keypoints([(blob.cx(), blob.cy(), int(math.degrees(blob.rotation())))], size=20)

