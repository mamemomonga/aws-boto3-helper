FROM alpine:3.8

# 時間をJSTに設定する
RUN set -xe && \
	apk --update add tzdata && \
	cp /usr/share/zoneinfo/Asia/Tokyo /etc/localtime && \
	apk del tzdata && \
	rm -rf /var/cache/apk/*

RUN set -xe && \
	apk --update add \
		su-exec build-base py-pip && \
	rm -rf /var/cache/apk/*

RUN set -xe && \
	pip install boto3 pyyaml

RUN set -xe && \
	adduser -u 10000 -D app

ADD entrypoint.sh /
ADD bin /home/app/bin

RUN set -xe && \
	chown -R app:app /home/app

ENTRYPOINT ["/entrypoint.sh"]

