<!DOCtYPE html>
<html lang=ja>
<head>
<meta charset="UTF-8">
<title>共用計算機アカウント申請確認</title>
</head>

<body>
<h1>確認</h1>
<p>以下の内容で申請しますが、よろしいですか？</p>
<p>=================================================================</p>
<p> 共用計算機アカウント発行依頼</p>
<p>=================================================================</p>
<p>  Name    : {{name_last}} {{name_first}} ({{kana_last}} {{kana_first}})</p>
<p>  Number  : {{student_id}}</p>
<p>  ISC-Mail: {{isc_account}}@mail.kyutech.jp</p>
<p>  -------------------------------------------------------------</p>
<p>  Account : {{club_account}}</p>
<p>  -------------------------------------------------------------</p>
<p>  Date    : {{format_date}}</p>
<p>  From    : {{remote_host}} ({{remote_addr}})</p>
<p>=================================================================</p>
<form action="/send/{{key}}" method="GET">
  <input type="submit" value="送信">
</form>
</body>

</html>
