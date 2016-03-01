# 各種申請自動化ツール

### 使用したサードパーティ製ライブラリ
* bottle
* beaker
* pytz

`# pip install bottle beaker pytz`

### ファイル構成
```
.
├── approve.py
├── database.py
├── entry.py
├── message.py
├── __pycache__
│   ├── database.cpython-35.pyc
│   ├── message.cpython-35.pyc
│   └── valid.cpython-35.pyc
├── README.md
├── sample.db
├── session
│   ├── container_file
│   └── container_file_lock
├── valid.py
└── views
    ├── ask.tpl
    ├── confirm.tpl
    ├── error.tpl
    ├── index.tpl
    └── send.tpl
```