import time
import frida
import redis


HOOKSCRIPT = """
        rpc.exports = {
            callencryptfunc: function callEncryptFunc(param) {
            var ret = "";
            Java.perform(function () {
                try {
                    var classCandyPreprocessor = Java.use("com.meituan.android.common.candy.CandyJni");
                    var ctx = Java.use("android.app.ActivityThread").currentApplication().getApplicationContext();
                    var jString = Java.use("java.lang.String");
                    var specStr = jString.$new("CandyKey");
                    param = jString.$new(param).getBytes();
                    ret = classCandyPreprocessor.getCandyDataWithKeyForJava(ctx, param, specStr);
                } catch (e) {
                    console.log(e);
                }
            });
            return ret;
        }
    }
        """

redis_name = "serial_id"
client = redis.Redis(host='192.168.4.60', port=6379, password='xxxx', db=5, decode_responses=True)

def get_serial_ids():
    serial_ids = client.smembers(redis_name)
    # print(serial_ids)
    return serial_ids

def _my_message_handler(message, payload):
    print({'message': message, 'payload': payload})

def hook_start(serial_id):
    device = frida.get_device(serial_id, timeout=10)
    time.sleep(1)
    pid = device.spawn(["com.dianping.v1"])
    time.sleep(1)
    device.resume(pid)
    time.sleep(1)  # wait for app up.
    session = device.attach(pid)
    script = session.create_script(HOOKSCRIPT)
    script.on("message", _my_message_handler)
    script.load()
    return script


# flask 服务开启时，先将所有手机 attach 上，否则将该设备删除
serial_mapping = dict()
for serial_id in get_serial_ids():
    flag = 0
    for _ in range(10):
        try:
            serial_mapping[serial_id] = hook_start(serial_id)
            print(f"{serial_id} attach success...")
            flag = 1
            break
        except Exception as e:
            print(f"{serial_id} init attach failed -- {e}")
    if flag == 0:
        client.srem(redis_name, serial_id)


def run(query, serial_id):
    # print(serial_mapping)
    try:
        skcy = serial_mapping[serial_id].exports.callencryptfunc(query)
    except Exception as e:
        print('In run', e)
        serial_mapping[serial_id] = hook_start(serial_id)
        skcy = serial_mapping[serial_id].exports.callencryptfunc(query)

    return skcy
