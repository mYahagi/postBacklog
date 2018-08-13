import requests
import os
import re
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    if event['body']['ref'].find("share") == -1 and event['body']['ref'].find("master") == -1:
        logger.info("masterまたはshareへのマージじゃないので無視する")
        return

    pattern = r'AAA_BB-[0-9]{3,}'
    baseUrl = 'https://xxx.backlog.jp/api/v2/issues/'

    issueIdArr = []

    def findIssueId(match, str):
        if match:
            issueId = match.group(0)
            issueIdArr.append(issueId)
            # すでに検出した課題番号はヒットしないよう空文字に置き換え
            str = str.replace(issueId, '')
            match = re.search(pattern, str)
            # 複数の課題番号が含まれているか再帰的に確認
            findIssueId(match, str)

    def postBacklog(issueIdArr, message, commitUrl):
        for issueId in issueIdArr:
            postUrl = baseUrl + issueId + '/comments'
            
            content = '''
            {message}
            {url}
            '''.format(message=message, url=commitUrl).strip()
        
            payload = {
                'content': content,
                'apiKey': os.environ['apiKey']
            }
        
            response = requests.post(postUrl, params=payload)
            logger.info(response.text)
    
    # 配列としてevent['body']['commits']内にローカルで溜め込んだコミットの情報が含まれている
    for commitRireki in event['body']['commits']:
        issueIdArr = []
        message = commitRireki['message']
        commitUrl = commitRireki['url']
        issueIdCheck = re.search(pattern, commitRireki['message'])
        # 課題番号が含まれているか確認
        findIssueId(issueIdCheck, commitRireki['message'])
        if len(issueIdArr) != 0:
            logger.info(issueIdArr)
            postBacklog(issueIdArr, message, commitUrl)