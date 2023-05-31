import PySimpleGUI as sg
import sound
import threading
import numpy as np
import sounddevice as sd
import playsound
from concurrent.futures import ProcessPoolExecutor

is_start_volume_monitoring = False


def callback(indata, frames, time, status):
    volume_norm = np.linalg.norm(indata) * 10
    print(int(volume_norm))

    if volume_norm > 50:
        playsound.playsound("春日部つむぎ.wav")


def start_sound_volume_monitoring():
    # PCのデバイス一覧の取得
    device_list = sd.query_devices()

    # デフォルトデバイスをセット
    rec_device_id = sd.default.device[0]  # 録音デバイス
    play_device_id = sd.default.device[1]  # 再生デバイス

    # 何秒おきに録音を開放するか
    duration = 1

    # デバイス情報関連
    sd.default.device = [rec_device_id, play_device_id]  # Input, Outputデバイス指定
    input_device_info = sd.query_devices(device=sd.default.device[1])
    sr_in = int(input_device_info["default_samplerate"])

    # 録音を開始
    while is_start_volume_monitoring is True:
        with sd.InputStream(
                channels=1,
                dtype='float32',
                callback=callback
        ):
            sd.sleep(int(duration * 1000))


# ウィンドウの内容を定義する
layout = [
    [sg.Text("何デシベルを超えたら警告しますか？")],
    [sg.Text("（デフォルトは50デシベルです）")],
    [sg.Input(key='デシベル', default_text=50)],
    [sg.Text("監視: してない", key="監視テキスト")],
    [sg.Button('開始', key="監視開始ボタン"), sg.Button('終了')],
]

# ウィンドウを作成する
window = sg.Window('Sound Volume Guard', layout)

# イベントループを使用してウィンドウを表示し、対話する
record_thread = False
while True:
    print('最初')
    event, values = window.read()
    # ユーザーが終了したいのか、ウィンドウが閉じられたかどうかを確認してください
    if event == sg.WINDOW_CLOSED or event == '終了':
        break

    # 開始ボタンが押されたら
    if event == "監視開始ボタン":
        # 監視開始
        if not is_start_volume_monitoring:
            is_start_volume_monitoring = True
            record_thread = threading.Thread(target=start_sound_volume_monitoring)
            record_thread.start()

            window['監視テキスト'].update("監視: してる")
            window['監視開始ボタン'].update("停止")
            continue

        # 監視停止
        if is_start_volume_monitoring:
            is_start_volume_monitoring = False
            window['監視テキスト'].update("監視: してない")
            window['監視開始ボタン'].update("開始")
            continue

# 画面から削除して終了
window.close()
