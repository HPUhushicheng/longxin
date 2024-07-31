
import time
from pyb import UART

uart = UART(1,19200, timeout_char =1000)

while(True):
  if uart.any():
    a = uart.read().decode().strip()
    print(a)
'''

import time
from pyb import UART

uart = UART(1, 19200, timeout_char=1000)

buffer = ""  # 用于累积接收到的数据

while True:
    if uart.any():
        # 读取所有可用的数据
        data = uart.read()
        if data:
            buffer += data.decode()
            if len(buffer) >= 6:  # 假设我们期望接收的数据长度为6
                print(buffer.strip())
                buffer = ""  # 清空缓冲区以接收新的数据
    time.sleep(0.1)  # 避免占用过多CPU资源
'''
