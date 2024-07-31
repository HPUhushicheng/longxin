import time
from machine import UART
#from pyb import UART

# OpenMV4 H7 Plus, OpenMV4 H7, OpenMV3 M7, OpenMV2 M4 的UART(3)是P4-TX P5-RX
#uart = UART(3, 19200)   #OpenMV RT 注释掉这一行，用下一行UART(1)
uart = UART(1, 19200)  #OpenMV4 H7 用UART(1)这行，注释掉上一行UART(3)
# OpenMV RT 只有串口UART(1)，对应P4-TX P5-RX; OpenMV4 H7 Plus, OpenMV4 H7, OpenMV3 M7 的UART(1)是P0-RX P1-TX

while(True):
    uart.write("Hello World!\r\n")
    time.sleep_ms(1000)

#打开星瞳串口助手，打开端口com8,对应波特率19200，接受数据