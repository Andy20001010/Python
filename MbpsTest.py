# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
#需安裝speedtest 套件
#在cmd輸入 "pip install speedtest_cli"
import speedtest
import os

print("檔案位於 ：" +(os.path.abspath(os.getcwd())) +("\n"))

print("網速測試準備中...\n")


test = speedtest.Speedtest()
print("測試目標 ：\n" + str(test) + ("\n"))
#獲取伺服器
test.get_servers()

best = test.get_best_server()
print("伺服器資訊 ：\n" + str(best) + ("\n"))

print("網速測試中...\n")

download_speed = int(test.download()/1024/1024)
upload_speed = int(test.upload()/1024/1024)  

print("下載速度 ：" + str(download_speed) + "MB")
print("上傳速度 ：" + str(upload_speed) + "MB")
