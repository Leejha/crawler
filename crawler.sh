#!/bin/bash
# crawler.sh

# Python 스크립트를 백그라운드에서 실행하고 완료되면 메시지를 보냄
nohup python3 /Users/junghyunkim/corp-reviews/crawler/crawler.py > /Users/junghyunkim/corp-reviews/crawler/crawler.log 2>&1

# '업데이트 완료' 메시지를 슬랙으로 전송
echo "$(date) /crawler.py 실행 종료. 결과를 확인하세요." | curl -X POST -H "Content-type: application/json" --data "{\"text\":\"$(cat -)\"}" https://hooks.slack.com/services/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