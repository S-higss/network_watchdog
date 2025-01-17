import os
import time

def ping_sender(ip):
    response = os.system("ping -n 1 " + ip)
    if response == 0:
        return True
    else:
        return False

if __name__ == "__main__":
    pc1_ip = "192.168.1.10"  # PC1のIPアドレス
    while True:
        if not ping_sender(pc1_ip):
            print("Target PC is down!")
        time.sleep(10)  # 10秒ごとに確認