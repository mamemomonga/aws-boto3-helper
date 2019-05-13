# AWS便利ツール

# AWSキーの指定方法

## awscliの設定を使用する

	$ docker run --rm \
		-v ~/.aws:/home/app/.aws:ro \
		helper [コマンド] [引数]

## 環境変数を使用する

	$ docker run --rm \
		-e AWS_ACCESS_KEY_ID=AKIAXXXXXXXXXXXXXXXX \
		-e AWS_SECRET_ACCESS_KEY=XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX \
		-e AWS_DEFAULT_REGION=ap-northeast-1 \
		helper [コマンド] [引数]

# コマンド一覧

## r53-private-zone-update 
Route53 Private Zone 正引き・逆引きを更新する

### 使い方

	$ docker run --rm \
		helper r53-private-zone-update

### 追加

	$ docker run --rm \
		-v ~/.aws:/home/app/.aws:ro \
		helper r53-private-zone-update \
		-z [正引きゾーン名] \
		-r [逆引きゾーン名] \
		-o [FQDN] \
		-i [IPアドレス]

### 削除

	$ docker run --rm \
		-v ~/.aws:/home/app/.aws:ro \
		helper r53-private-zone-update \
		-d \
		-z [正引きゾーン名] \
		-r [逆引きゾーン名] \
		-o [FQDN] \
		-i [IPアドレス]

## ec2-wait-instance-state

EC2の起動が指定した状態になるまで待つ

### 使い方

	$ docker run --rm \
		helper ec2-wait-instance-state

### 実行

	$ docker run --rm \
		-v ~/.aws:/home/app/.aws:ro \
		helper ec2-wait-instance-state \
		[InstanceID] [State]


