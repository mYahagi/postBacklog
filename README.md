# githubのコミットURLとBacklogの課題番号を紐づける
* コミットメッセージにBacklogの課題番号を含めてpushすればそれを検出して該当の課題にコミット時のURLとコミットメッセージをコメントする
* apiKeyは予めBacklog側で発行しておいたものを利用する
* AWS lambdaにおいて使用している
* apigatewayと連携してgithubからはそこをhook先のurlとして指定している
* patternに自プロジェクトに適した正規表現を定義してあげれば動くはず

https://qiita.com/yahagin/items/d4237c9702952e7f4795

# 使い方
pattern1
* git commit -m " 課題番号 コミットコメント"

pattern2 課題番号複数紐付けれる
* git commit -m " 課題番号1 課題番号2 ... コミットコメント"

pattern3 ローカルでコミット分けても個々の課題に紐付け可能
* git commit -m " 課題番号1 コミットコメント"
* git commit -m " 課題番号2 コミットコメント"
* git push origin hoge
