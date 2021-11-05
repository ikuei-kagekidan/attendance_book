# Part1 開発環境作成からサーバー起動まで
## 1.PaizaCloudで開発環境作成
[PaizaCloud](https://paiza.cloud/ja/)は無料で使えるクラウドIDEツールである。  
使用するにはアカウントを作成しておく必要がある。  

「利用する」をクリックし「新規サーバー作成」をクリックすると次のようなサーバー設定画面が表示される。

<img width="1086" alt="img101" src="https://user-images.githubusercontent.com/36835148/136541740-db0ffb9f-3e14-493f-a692-f33b28c62a2c.png">

サーバ名はなんでも構わない。  
初期インストールするのもとしてDjangoを指定しておく。  
これで「新規サーバ作成」をクリックすると開発環境が作成される。

## 2.GitHubリポジトリからclone
cloneとはgitのコマンドの一つで、リモートリポジトリを自分の環境に複製するコマンドである。

まず、右にある「ターミナル」をクリックするとターミナルが起動する。

<img width="913" alt="img102" src="https://user-images.githubusercontent.com/36835148/136541759-6fc6284a-3478-4401-aac4-32709741e915.png">

次にgitの設定をする。  
ターミナルで次のコマンドを実行する。  
```
git config --global user.name 'githubのアカウント名'
```
```
git config --global user.email 'githubに登録したメールアドレス'
```

次にこのリポジトリ[(izumi-reon/attendance_book)](https://github.com/izumi-reon/attendance_book)からForkした自分のリモートリポジトリからcloneする。  
[※Forkの方法ついて](https://docs.github.com/ja/get-started/quickstart/fork-a-repo)  
Forkした自分のリモートリポジトリのURLは`https://github.com/githubのアカウント名/attendance_book.git`となっているはずである。  
ターミナルで次のコマンドを実行する。 
```
git clone https://github.com/githubのアカウント名/attendance_book.git
```
この時アカウント名とパスワードの入力を要求されることがある。アカウント名はGitHubアカウントを入力すれば良い。パスワードについては個人アクセストークンを入力する。  
[※個人アクセストークンの生成について](https://docs.github.com/ja/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token)  

cloneに成功するとattendance_bookというディレクトリが作成されるのでそのディレクトリに移動する。
```
cd attendance_book
```

## 3.サーバー起動
次のコマンドでサーバーを起動する。
```
python3 manage.py runserver
```
これは8000番ポートでサーバーを起動するコマンドであるが、学校で実行すると失敗する。そのため学校でサーバーを起動するには80番ポートで起動する必要がある。それは次のコマンドを実行する。
```
sudo python3 manage.py runserver 80
```

以下は8000番ポートでサーバーを起動したとして説明を続ける。  
サーバーの起動に成功すると右に「8000」というのが出現するのでこれをクリックする。すると404ページが表示される。

<img width="962" alt="img103" src="https://user-images.githubusercontent.com/36835148/136541761-ca39ea54-ff34-464a-a58d-abed3166ed6b.png">

アドレスバーに`/attendance_book/`を追加するとアプリのページが表示される。

<img width="972" alt="img104" src="https://user-images.githubusercontent.com/36835148/136541766-f226f420-d762-493f-a662-7e0cfe2b2ace.png">

ちなみにこのページは`attendance_book/attendance_book/templates/attendance_book/index.html`に書かれている。
