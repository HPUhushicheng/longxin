import sensor, image, time
from machine import UART
from pyb import UART
import ustruct

sensor.reset() #初始化设置
sensor.set_pixformat(sensor.RGB565) #设置为彩色
sensor.set_framesize(sensor.QVGA) #设置清晰度
sensor.skip_frames(time = 2000) #跳过前2000ms的图像
sensor.set_auto_gain(False) # must be turned off for color tracking
sensor.set_auto_whitebal(False) # must be turned off for color tracking
clock = time.clock() #创建一个clock便于计算FPS
sensor.set_auto_gain(False) # 关闭自动自动增益。默认开启的。
sensor.set_auto_whitebal(False) #关闭白平衡。
#uart = UART(3, 115200)
uart1 = UART(1, 115200)


output_str_red="[0,0]"
output_str_blue="[0,0]"
output_str_yellow="[0,0]"
red_threshold    = (57, 20, 17, 85, -19, 20)
blue_threshold = (16, 42, 11, 127, -76, -22)
yellow_threshold  = (50, 67, -17, 2, 26, 87)

thresholds = [(45, 100, -41, 127, -10, 120) ] # black 二维码



def send_five_uchar(c1,c2,c3,c4):#功能发送五个无符号字符（unsigned char）
    global uart;
    data = ustruct.pack("<BBBBBBBB",#使用了 ustruct.pack() 函数将这些数据打包为二进制格式。使用 "<BBBBBBBB" 作为格式字符串来指定要打包的数据的类型和顺序：
           0xaa,
           c1,
           c2,
           c3,
           c4,
           0xff
               )
    uart1.write(data);#uart.write(data) 将打包好的二进制数据帧写入 UART 发送缓冲区，从而将数据通过串口发送出去
    print(data)#通过 print(data) 打印发送的数据到串行终端，方便调试和确认发送的内容。


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

at = None
red_distance =None
yellow_distance =None
blue_distance=None
white_distance=None


while(True):
    clock.tick()
    img = sensor.snapshot()#可以畸形也可以不用
    blobs_red = img.find_blobs([red_threshold])
    blobs_blue = img.find_blobs([blue_threshold])
    blobs_yellow = img.find_blobs([yellow_threshold])

    if blobs_red:
        max_blob_red=find_max(blobs_red)
        shape_red=detect(max_blob_red)
        #img.draw_rectangle(max_blob_red.rect(),color=(255,0,0))
        img.draw_cross(max_blob_red.cx(), max_blob_red.cy(),color=(255,0,0))
        #output_str_red="[%d,%d,%d]" % (max_blob_red.cx(),max_blob_red.cy(),shape_red) 
        output_str_red="[%d]" % (240 - max_blob_red.cy())
#        output_str_red = int(output_str_red[1:-1])  # 提取出字符串中的整数部分并转换为整数
#        output_str_red = 240 - output_str_red
        if int(output_str_red[1:-1]) < 10:
             red_distance = 55



    if blobs_blue:
       max_blob_blue=find_max(blobs_blue)
       shape_blue=detect(max_blob_blue)
       #img.draw_rectangle(max_blob_blue.rect(),color=(0,0,255))
       img.draw_cross(max_blob_blue.cx(), max_blob_blue.cy(),max_blob_blue.w(),max_blob_blue.h(),color=(0,0,255))
       #output_str_blue="[%d,%d,%d,%d,%d]" % (max_blob_blue.cx(),max_blob_blue.cy(),max_blob_blue.w(),max_blob_blue.h(),shape_blue) #方式1
       output_str_blue="[%d]" % (max_blob_blue.w())
       #width = int(output_str_blue[1:-1])
       if int(output_str_blue[1:-1]) < 10:
            blue_distance = 66

       
    if blobs_yellow:
       max_blob_yellow=find_max(blobs_yellow)
       shape_yellow=detect(max_blob_yellow)
       #img.draw_rectangle(max_blob_yellow.rect(),color=(255,255,0))
       img.draw_cross(max_blob_yellow.cx(), max_blob_yellow.cy(),max_blob_yellow.w(),max_blob_yellow.h(),color=(255,255,0))
       #output_str_yellow="[%d,%d,%d,%d,%d]" % (max_blob_yellow.cx(),max_blob_yellow.cy(),max_blob_yellow.w(),max_blob_yellow.h(),shape_yellow) #方式1
       output_str_yellow="[%d]" % (max_blob_yellow.w())
       #width = int(output_str_yellow[1:-1])  #取整
       if int(output_str_yellow[1:-1]) < 10:
            yellow_distance = 77
   
    for blob in img.find_blobs(thresholds, area_threshold = 200, pixels_threshold=200):
        for code in img.find_qrcodes():  # 进行二维码检测
                img.draw_rectangle(code.rect(), color = (255, 0, 0))
                print(code)
                #print(code.payload())
                if(code.payload()=="1 white"):
                     at=1
                if(code.payload()=="1 blue"):
                     at=2
                if(code.payload()=='1 yellow'):
                     at=3
                if(code.payload()=='2 white'):
                     at=4
                if(code.payload()=='2 blue'):
                     at=5
                if(code.payload()=='2 yellow'):
                     at=6
                if(code.payload()=='3 white'):
                     at=7
                if(code.payload()=='3 blue'):
                     at=8
                if(code.payload()=='3 yellow'):
                     at=9
                if(code.payload()=='4 white'):
                     at=10
                if(code.payload()=='4 blue'):
                     at=11
                if(code.payload()=='4 yellow'):
                     at=12
                #data1=bytearray([at])
                #uart.write(data1)
                if red_distance is not None:
                    data3_bytes = red_distance.to_bytes(1,'big')
                if blue_distance is not None:
                    data4_bytes = blue_distance.to_bytes(1,'big')
                if red_distance is not None:
                    data5_bytes = red_distance.to_bytes(1,'big')  
                if at is not None:
                    time.sleep_ms(100)
                    #send_five_uchar(at,data3_bytes[0] , data4_bytes[0],data5_bytes[0])
                    send_five_uchar(at,red_distance,blue_distance,yellow_distance)


