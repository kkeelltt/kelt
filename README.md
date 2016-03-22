# 各種申請自動化ツール

### 使用したサードパーティ製ライブラリ
* bottle
* beaker
* pytz

`# pip install bottle beaker pytz`

Uオプションを使うとユーザーのみにインストール可能

***

### ファイル構成
```
.
├── approve.py
├── database.py
├── entry.py
├── ldap.py
├── message.py
├── valid.py
└── views
    ├── check.tpl
    ├── confirm.tpl
    ├── error.tpl
    ├── finish.tpl
    ├── index.tpl
    └── send.tpl
```

***

### テスト方法
申請フォーム  
`$ python entry.py`  
をして、  
`http://localhost:8080`  
にアクセス


承認UI  
`$ python approve.py`  
したうえで、  
`http://localhost:8080/check/[ユーザ名]`  
にアクセス
