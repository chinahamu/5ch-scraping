# 5chスクレイピングスクリプト
	ログ速でスレッドを検索し、5chスレッドのレスを取得するスクリプトです。

## 使い方
	`python3 scrap.py "kyeword" output_dir/output_file_name`

## 使用ライブラリ
 bs4,html5lib

## パラメーター
arg1 検索ワード

arg2 アウトプットファイル

--sort create=スレ立て順 write=書き込み順 デフォルト＝create

--order desc=新しい順,asc=古い順 デフォルト=desc

--sr 何スレ以上のスレを取得するか デフォルト=1

--active 0=過去スレのみ,1=現行のみ,2=すべて デフォルト=2

--limit 何スレ取得するか　デフォルトはあるだけ取得

## 要望など
　なにかありましたらissueを立てていただければ幸いです。