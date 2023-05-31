import numpy as np
import sounddevice as sd
import playsound
from concurrent.futures import ProcessPoolExecutor
import time


def play_alert():
    playsound.playsound("春日部つむぎ.wav")


def callback(indata, frames, time, status):
    volume_norm = np.linalg.norm(indata) * 10
    print(int(volume_norm))

    if volume_norm > 50:
        with ProcessPoolExecutor() as executor:
            play_alert()

def test():
    print("test start")
    time.sleep(1)
    print("test end")

def start_sound_volume_monitoring():
    # PCのデバイス一覧の取得
    device_list = sd.query_devices()
    # print(device_list)

    # for device_number in sd.default.device:
    #     print(device_number)
    #     print(device_list[device_number])
    #
    # print('=============================================')
    # print(sd.default.device)

    # デフォルトデバイスをセット
    rec_device_id = sd.default.device[0]  # 録音デバイス
    play_device_id = sd.default.device[1]  # 再生デバイス

    # 何秒おきに録音を開放するか
    duration = -1

    # デバイス情報関連
    sd.default.device = [rec_device_id, play_device_id]  # Input, Outputデバイス指定
    input_device_info = sd.query_devices(device=sd.default.device[1])
    sr_in = int(input_device_info["default_samplerate"])

    # 録音を開始
    with sd.InputStream(
            channels=1,
            dtype='float32',
            callback=callback
    ):
        sd.sleep(int(duration * 1000))
