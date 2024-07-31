import sensor, image, time
from pyb import UART
import json

output_str_green="[0,0]"
output_str_red="[0,0]"
output_str_blue="[0,0]"
output_str_brown="[0,0]"
output_str_yellow="[0,0]"


#green_threshold  = (   0,   80,  -70,   -10,   -0,   30)
#green_threshold  = (54, 14, -48, 106, -67, -53)
red_threshold    = (57, 20, 17, 85, -19, 20)
#orange_threshold = (   23,   39,  19,   42,   13,   31)
#blue_threshold = (16, 42, 11, 127, -76, -22)
#brown_threshold  = (   22,   30,  1,   17,   8,   25)
#yellow_threshold  = (50, 67, -17, 2, 26, 87)

sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA)
#sensor.set_windowing((0,20,320,240))#QVGA find Region Of Interest
#sensor.set_windowing((5,10,160,95))#QQVGA find Region Of Interest
sensor.skip_frames(10)
sensor.set_auto_whitebal(False)
clock = time.clock()

uart = UART(3, 115200)
def find_max(blobs):
    max_size=0
    for blob in blobs:
        if blob.pixels() > max_size:
            max_blob=blob
            max_size = blob.pixels()
    return max_blob

def detect(max_blob):#输入的是寻找到色块中的最大色块
    #print(max_blob.solidity())
    shape=0
    if max_blob.solidity()>0.90 or max_blob.density()>0.84:
        img.draw_rectangle(max_blob.rect(),color=(255,255,255))
        shape=1

    elif max_blob.density()>0.6:
        img.draw_circle((max_blob.cx(), max_blob.cy(),int((max_blob.w()+max_blob.h())/4)))
        shape=2

    elif max_blob.density()>0.4:
        img.draw_rectangle(max_blob.rect(),color=(0,0,0))
        shape=3

    return shape

while(True):
    #clock.tick()
    img = sensor.snapshot() # Take a picture and return the image.
    #blobs_green = img.find_blobs([green_threshold])
    blobs_red = img.find_blobs([red_threshold])
    #blobs_orange = img.find_blobs([orange_threshold])
 #   blobs_blue = img.find_blobs([blue_threshold])
#    blobs_brown = img.find_blobs([brown_threshold])
 #   blobs_yellow = img.find_blobs([yellow_threshold])

#    if blobs_green:
#        max_blob_green=find_max(blobs_green)
#        shape_green=detect(max_blob_green)
#        #img.draw_rectangle(max_blob_green.rect(),color=(0,255,0))#画框
#        img.draw_cross(max_blob_green.cx(), max_blob_green.cy(),color=(0,255,0))#画十字准星
#        output_str_green="[%d,%d,%d]" % (max_blob_green.cx(),max_blob_green.cy(),shape_green) #方式1
#        print('green:',output_str_green)

#    else:
#        print('not found green!')


    if blobs_red:
        max_blob_red=find_max(blobs_red)
        shape_red=detect(max_blob_red)
        #img.draw_rectangle(max_blob_red.rect(),color=(255,0,0))
        img.draw_cross(max_blob_red.cx(), max_blob_red.cy(),color=(255,0,0))
        #output_str_red="[%d,%d,%d]" % (max_blob_red.cx(),max_blob_red.cy(),shape_red) #方式1
        output_str_red="[%d]" % (240 - max_blob_red.cy())
#        output_str_red = int(output_str_red[1:-1])  # 提取出字符串中的整数部分并转换为整数
#        output_str_red = 240 - output_str_red
        print('red:',output_str_red)

    else:
        print('not found red !')


    #if blobs_orange:
        #max_blob_orange=find_max(blobs_orange)
        #detect(max_blob_orange)
        ##img.draw_rectangle(max_blob_orange.rect(),color=(255,128,0))
        #img.draw_cross(max_blob_orange.cx(), max_blob_orange.cy(),color=(255,128,0))
        #output_str_orange="[%d,%d]" % (max_blob_orange.cx(),max_blob_orange.cy()) #方式1
        #print('orange:',output_str_orange)
        #uart.write(output_str_orange+'\r\n')
    #else:
        #print('not found orange !')


#    if blobs_blue:
#        max_blob_blue=find_max(blobs_blue)
#        shape_blue=detect(max_blob_blue)
#        #img.draw_rectangle(max_blob_blue.rect(),color=(0,0,255))
#        img.draw_cross(max_blob_blue.cx(), max_blob_blue.cy(),max_blob_blue.w(),max_blob_blue.h(),color=(0,0,255))
#        #output_str_blue="[%d,%d,%d,%d,%d]" % (max_blob_blue.cx(),max_blob_blue.cy(),max_blob_blue.w(),max_blob_blue.h(),shape_blue) #方式1
#        output_str_blue="[%d]" % (max_blob_blue.w())
#        print('blue:',output_str_blue)
#    else:
#        print('not found blue !')


#    if blobs_brown:
#        max_blob_brown=find_max(blobs_brown)
#        shape_brown=detect(max_blob_brown)
#        #img.draw_rectangle(max_blob_brown.rect(),color=(205,133,63))
#        img.draw_cross(max_blob_brown.cx(), max_blob_brown.cy(),color=(205,133,63))
#        output_str_brown="[%d,%d,%d]" % (max_blob_brown.cx(),max_blob_brown.cy(),shape_brown) #方式1
#        print('brown:',output_str_brown)
#    else:
#        print('not found brown !')

#    if blobs_yellow:
#        max_blob_yellow=find_max(blobs_yellow)
#        shape_yellow=detect(max_blob_yellow)
#        #img.draw_rectangle(max_blob_yellow.rect(),color=(255,255,0))
#        img.draw_cross(max_blob_yellow.cx(), max_blob_yellow.cy(),max_blob_yellow.w(),max_blob_yellow.h(),color=(255,255,0))
#        #output_str_yellow="[%d,%d,%d,%d,%d]" % (max_blob_yellow.cx(),max_blob_yellow.cy(),max_blob_yellow.w(),max_blob_yellow.h(),shape_yellow) #方式1
#        output_str_yellow="[%d]" % (max_blob_yellow.w())
#        print('yellow:',output_str_yellow)
#    else:
#        print('not found yellow !')


    #uart.write(output_str_green + output_str_red + output_str_blue + output_str_brown + output_str_yellow + '\r\n')

    print(clock.fps())
