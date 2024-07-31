import sensor, image, time
from machine import UART
from pyb import UART
import ustruct


thresholds = [(45, 100, -41, 127, -10, 120) ]# black
sensor.reset() #初始化设置
sensor.set_pixformat(sensor.RGB565) #设置为彩色
sensor.set_framesize(sensor.QVGA) #设置清晰度
#sensor.set_windowing(150,200)
sensor.skip_frames(time = 2000) #跳过前2000ms的图像
sensor.set_auto_gain(False) # must be turned off for color tracking
sensor.set_auto_whitebal(False) # must be turned off for color tracking
clock = time.clock() #创建一个clock便于计算FPS
sensor.set_auto_gain(False) # 关闭自动自动增益。默认开启的。
sensor.set_auto_whitebal(False) #关闭白平衡。
#uart = UART(3, 115200)
uart1 = UART(1, 115200)


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


at = None
distance =100
while(True):
    clock.tick()
    img = sensor.snapshot()#可以畸形也可以不用
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
                data3_bytes = distance.to_bytes(2, 'big')
                if at is not None:
                    time.sleep_ms(100)
                    send_five_uchar(at, 20,data3_bytes[0] , data3_bytes[1])




#aa ='12'
#def tc_data(data1, data2, data3):
#    tx_byte = [0] * 10

#    tx_byte[0] = 0xAA
#    tx_byte[1] = data1
#    tx_byte[2] = data2
#    # 由于 Python 中内存布局和 C 不同，无法直接进行类似的字节拆分
#    # 以下是一种可能的模拟方式，假设 data3 是一个整数
#    data3_bytes = data3.to_bytes(2, 'little')
#    tx_byte[3] = data3_bytes[0]
#    tx_byte[4] = data3_bytes[1]
#    tx_byte[5] = 0xFF

#    for i in range(5):
#        # 假设 uart_write_byte 功能是打印
#        #print(tx_byte[i])
#        uart1.write(aa)

#while(True):
#    tc_data(10,20,1010)










