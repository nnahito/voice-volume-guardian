# Sound Guard
マイクに一定音量以上の入力があると、wavファイルを再生します

## ソフトウェアとして使いたい方
Releasesよりダウンロードしてください
https://github.com/nnahito/voice-volume-guardian/releases

## 開発してみたい方
### （0）Python
自分で入れてください。
scoopとかでサクッと入れると楽。

### （1）venvの準備
```
$ python3 -m venv venv
$ venv\Scripts\activate

## macは source venv/bin/activate
```

### （2）必要モジュールのダウンロード
```
$ pip install -r requirements.txt
```

### （3）起動
```
$ python main.py
```

## クレジット
- 音源のデフォルトに以下を利用しています
- VOICEBOX 春日部つむぎ
    - https://voicevox.hiroshiba.jp/