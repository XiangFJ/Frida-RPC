# _*_ coding:UTF-8 _*_

import subprocess
from frida_rpc.monitor import send_msg


def get_serial_status():
    """
    获取所有通过 USB 连接的手机设备
    :return:
    """
    popen_object = subprocess.Popen(["adb", "devices"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding='utf-8')
    object_stdout = popen_object.communicate()[0]
    stdout_list = object_stdout.split()
    # print(object_stdout)
    stdout_len = len(stdout_list)

    device_list = []
    for i in range(2, stdout_len//2):
        device_list.append((stdout_list[2*i], stdout_list[2*i+1]))

    return device_list


def get_serial_nos():
    serial_nos = []
    device_list = get_serial_status()
    print(device_list)

    for item in device_list:
        if item[1] == 'device':
            serial_nos.append(item[0])
        else:
            # TODO 监控报警
            module = "device"
            info = f"{item[0]} ===> 手机未连接，状态为 {item[1]}"
            send_msg(info, module)
            print(info)

    return serial_nos



