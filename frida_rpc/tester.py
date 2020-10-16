import redis
import time
import subprocess
from frida_rpc.device import get_serial_nos
from frida_rpc.monitor import send_msg

module = "tester"
usable_serial = []

def cmd(command):
    subp = subprocess.Popen(command, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding="utf-8")
    return subp.communicate()

def test(serial_id):
    # print(serial_id)
    # ret = cmd(f"adb -s {serial_id} shell ps -ef | grep fs-1280-arm64 | grep -v grep")  # Google

    for i in range(0, 20):
        ret = cmd(f"adb -s {serial_id} shell ps | grep fs-1280-arm64 | grep -v grep")  # xiaoMi
        if ret[0] == '':
            print(f"{serial_id} - 第 {i} 次尝试开启服务...")
            try:
                cmd(f"adb -s {serial_id} shell su -c /data/local/tmp/start.sh")
                time.sleep(2)
            except Exception as e:
                # TODO 监控报警
                info = f"{serial_id} ===> 第 {i} 次 frida-server 开启失败，失败原因 ===> {e}"
                send_msg(info, module)

        else:
            print(f"{serial_id} - 服务已经开启...")
            usable_serial.append(serial_id)
            break


def get_usable_serial():
    serial_nos = get_serial_nos()
    con_num = len(serial_nos)

    if con_num < 5:
        # TODO 监控报警：手机数量过少
        info = f"当前手机正常连接的设备量较少 ===> {con_num} 台"
        send_msg(info, module)


    if serial_nos != []:
        for serial_id in serial_nos:
            restart_app(serial_id)
            test(serial_id)

    usable_num = len(usable_serial)
    if usable_num < 4:
        info = f"当前 frida-server 正常开启的设备量较少 ===> {usable_num} 台"
        send_msg(info, module)

    return usable_serial


def restart_app(serial_id):
    try:
        cmd(f"adb -s {serial_id} shell am force-stop com.dianping.v1")
        # time.sleep(2)
        # cmd(f"adb -s {serial_id} shell am start -n com.dianping.v1/com.dianping.v1.NovaMainActivity")
    except Exception as e:
        info = f"{serial_id} -- restart failed!!! -- {e}"
        send_msg(info, module)


def save2redis():
    # 检测手机设备，将 frida-server 正常开启的手机设备存入 redis
    redis_name = "serial_id"
    client = redis.Redis(host='192.168.4.60', port=6379, password='Pmi@gaia', db=5, charset='utf-8')

    usable_serials = get_usable_serial()
    # purge pre redis
    client.delete(redis_name)

    for param in list(set(usable_serials)):
        client.sadd(redis_name, param)

if __name__ == '__main__':
    save2redis()

