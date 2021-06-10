# attendance book
## 0.初めにやること
GitHubアカウントを作成する。  
このリポジトリの右上のForkボタンを押してForkする。
## 1.準備
### gitの設定
設定していないならこれをやる。
```
git config --global user.name 'githubのアカウント名'
git config --global user.email 'githubに登録したメールアドレス'
```
### リポジトリをクローン
Forkしたリモートリポジトリからクローンする。
```
git clone https://github.com/githubのアカウント名/attendance_book.git
cd attendance_book
```
### ブランチ作成
ブランチを作成する。  
mainブランチから作成したブランチに切り替える。  
ブランチ名は分かりやすければなんでもいい。
```
git branch ブランチ名
git checkout ブランチ名
```
## 2.編集
ファイルを編集する。  
編集作業は作成したブランチで行う。  
mainブランチでは編集作業を行わない。
## 3.コミット
キリの良いところでファイルの変更点を記録する。  
コメントは変更点などを書く。
```
git add .
git commit -m 'コメント'
```
## 4.プッシュ
**2**,**3**を繰り返し行いキリの良いところでコミットを自分のリモートリポジトリに反映させる。
```
git push origin ブランチ名
```
## 5.Fork元リポジトリの最新を反映させたい場合
Fork元リポジトリが設定されていなければ設定する。
```
git remote add upstream https://github.com/izumi-reon/attendance_book.git
```
一度mainブランチに移動しプルする。
```
git checkout main
git pull upstream main
```
自分のリモートリポジトリにも反映させる。
```
git push origin main
```
## 6.プルリクエスト
GitHubのForkした自分のリポジトリに行き、
左側にあるボタンから**4**でプッシュしたブランチに切り替え、
Pull Requestを押す。
