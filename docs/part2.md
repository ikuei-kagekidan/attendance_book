# Part2 データベースの構築からサンプルデータの挿入まで
## 1.モデルの構築
`attendance_book/attandance_book/models.py`に書かれたデータベースのモデルを構築するには以下の手順を実行する。  
(1) マイグレーションの作成
```
$ python manage.py makemigrations attendance_book
```
(2) マイグレーションの適応
```
$ python manage.py migrate
```

## 2.管理ユーザーの作成
管理者ページにアクセスするには管理者ユーザーを作る必要がある。次のコマンドを実行する。
```
$ python manage.py createsuperuser
```
ユーザー名、メールアドレス、パスワード、再度パスワードの入力が求められる。以下に入力例を示す。
```
Username (leave blank to use 'ubuntu'): admin
Email address: admin@example.com
Password:
Password (again):
Superuser created successfully.
```

## 3.管理者ページにログイン
サーバーを起動する。
```
$ python3 manage.py runserver
```
または
```
$ sudo python3 manage.py runserver 80
```
そしてブラウザを起動する。  
アドレスバーに`/admin/`を追加する。

<img width="620" alt="img201" src="https://user-images.githubusercontent.com/36835148/140327429-6ae7ad52-74c4-4e53-a5a6-72f0e1a6d57e.png">

すると管理者ページへのログイン画面が表示される。

<img width="610" alt="img202" src="https://user-images.githubusercontent.com/36835148/140327438-d328b08f-1a65-4c3b-9919-768c995de0d6.png">

先ほど設定したユーザー名とパスワードを入力してログインすると管理者ページが表示される。

<img width="575" alt="img203" src="https://user-images.githubusercontent.com/36835148/140327442-6e1f9f5a-bb41-4d42-a3aa-e69ae615fec9.png">

## 4.サンプルデータの挿入
管理者ページではデータベースに格納されているデータの確認や、データの追加、編集、削除ができる。例えば赤字で示したようにPersonsをクリックするとPersonsに格納されているデータを確認できる。しかし現在は空の状態である。

<img width="573" alt="img204" src="https://user-images.githubusercontent.com/36835148/140327446-67a44ae3-7a57-4eb6-9e0a-e25e5b9e5c6c.png">

そこで`attendance_book/attandance_book/fixtures/example_data.json`にサンプルデータを用意してある。これを読み込むには一度サーバーを停止させて次のコマンドを実行する。
```
$ python manage.py loaddata example_data.json
```
再びサーバーを起動し、管理者ページにアクセスし、Personsに格納されているデータを見ると12人分のデータが追加されていることが分かる。

<img width="460" alt="img205" src="https://user-images.githubusercontent.com/36835148/140327451-d8c3f3ac-8384-485a-9206-ceff86cd76a1.png">

## おまけ
### データベースのデータの出力
現在のデータベースに格納されているデータをjsonで出力するには次のコマンドを実行する。
```
$ python manage.py dumpdata attendance_book > attendance_book/fixtures/ファイル名.json
```
すると`attendance_book/attandance_book/fixtures/`にファイルが作成される。

### データベースのリセット
データベースをリセットするには`attendance_book/attandance_book/migrations/`にある`__init__.py`以外のファイル・フォルダを全て削除し、さらに`attendance_book/db.sqlite3`を削除する。すると「1.モデルの構築」からやり直すことができる。
