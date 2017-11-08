# coding=utf-8
import sys
import serial
import time
import os
from multiprocessing import Process, Pipe
from PyQt4.QtGui import QApplication

from ui.mainwindow import MainWindow
from util import *


def change_light(_light_conn):
    while 1:
        if _light_conn.poll(0.1):
            msg = _light_conn.recv()
            turn_off_light()
            break
        turn_off_light()
        turn_on_light('R')
        turn_off_light()
        turn_on_light('G')
        turn_off_light()
        turn_on_light('B')
        turn_off_light()


def worker(conn, light_conn):
    # import sys
    # sys.path.append("/tmp/pycharm-debug-py3k.egg")
    # import pydevd
    # pydevd.settrace('192.168.3.73', port=51234, stdoutToServer=True, stderrToServer=True)
    conn.send(['changpg', 1])
    conn.send(["title", '恢复文件系统'])    
    conn.send(['info', '开始恢复文件系统，切勿断电'])
    #time.sleep(10)
	#os.system('sudo killall daemon')
    #os.system("sudo ps -ef |grep python |grep -v test2 |awk '{print $2}' |xargs sudo kill -9")

    #if os.path.exists('/dev/mmcblk0p7'):
    #    os.system('sudo dd if=/home/firefly/flash/linux-boot.img of=/dev/mmcblk0p7')
    #if os.path.exists('/dev/rknand_recovery'):
        #os.system('sudo dd if=/home/firefly/flash/linux-boot.img of=/dev/rknand_recovery')
    #if os.path.exists('/dev/rknand_linuxroot'):
        #os.system('sudo dd if=/home/firefly/flash/linuxroot-20161127.backup of=/dev/rknand_linuxroot bs=3M')
    #if os.path.exists('/dev/mmcblk0p14'):
        #os.system('sudo dd if=/home/firefly/flash/linuxroot-20161127.backup of=/dev/mmcblk0p14 bs=3M')
    #os.system('sync')
    #os.system('sync')
    time.sleep(30)
	#time.sleep(300)
    conn.send(["title", '恢复文件系统'])
    print("test")
    conn.send(['info', '恢复文件系统完毕，请重启设备'])
    conn.close()
    time.sleep(10)
    light_conn.send(['close', 1])
    light_conn.close()
    time.sleep(10)
    


if __name__ == '__main__':
    init_music()
    if sys.platform != 'win32':
        os.chdir(os.path.dirname(sys.argv[0]))

    parent_conn, child_conn = Pipe()
    light_parent_conn, light_child_conn = Pipe()
    p = Process(target=worker, args=(child_conn, light_child_conn))

    app = QApplication(sys.argv)

    mainwindow = MainWindow(parent_conn)
    mainwindow.show()
		print("test")
    p.start()
    light_p = Process(target=change_light, args=(light_parent_conn,))
    light_p.start()

    sys.exit(app.exec_())
