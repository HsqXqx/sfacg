import requests
import time
import uuid
import sys
import hashlib
import json
import os
# from sud import NovelDownloader





nonce = "C7DC5CAD-31CF-4431-8635-B415B75BF4F3"
device_token = str(uuid.uuid4())
SALT = "FN_Q29XHVmfV3mYX"
headers = {
    'Host': 'api.sfacg.com',
    'accept-charset': 'UTF-8',
    'authorization': 'Basic YW5kcm9pZHVzZXI6MWEjJDUxLXl0Njk7KkFjdkBxeHE=',
    'accept': 'application/vnd.sfacg.api+json;version=1',
    'user-agent': f'boluobao/5.0.36(android;32)/H5/{device_token}/H5',
    'accept-encoding': 'gzip',
    'Content-Type': 'application/json; charset=UTF-8'
}
device_token = device_token.upper()

def md5_hex(input, case):
    m = hashlib.md5()
    m.update(input.encode())

    if case == 'Upper':
        return m.hexdigest().upper()
    else:
        return m.hexdigest()


def check(cookie):
    headers['cookie'] = cookie
    resp = requests.get('https://api.sfacg.com/user?', headers=headers).json()
    if (resp["status"]["httpCode"] == 200):
        nick_Name = resp['data']['nickName']
        # print(f"{nick_Name} cookie未失效")
        return True
    else:
        return False


def login(username, password):
    
    timestamp = int(time.time() * 1000)
    sign = md5_hex(f"{nonce}{timestamp}{device_token}{SALT}", 'Upper')
    headers['sfsecurity'] = f'nonce={nonce}&timestamp={timestamp}&devicetoken={device_token}&sign={sign}'
    data = json.dumps(
        {"password": password, "shuMeiId": "", "username": username})
    url = "https://api.sfacg.com/sessions"
    
    resp = requests.post(url, headers=headers, data=data)
    if (resp.json()["status"]["httpCode"] == 200):
        cookie = requests.utils.dict_from_cookiejar(resp.cookies)
        return cookie[".SFCommunity"], cookie["session_APP"]
    else:
        return "", ""


exp = 0
couponNum = 0
fireCoin = 0


def checkin(cookie):
    global exp
    global couponNum
    global fireCoin
    
    timestamp = int(time.time() * 1000)
    sign = md5_hex(f"{nonce}{timestamp}{device_token}{SALT}", 'Upper')
    headers['sfsecurity'] = f'nonce={nonce}&timestamp={timestamp}&devicetoken={device_token}&sign={sign}'
    headers["cookie"] = cookie
    Date = time.strftime('%Y-%m-%d', time.localtime(time.time()))
    signDate = json.dumps({"signDate": Date})
    ReadData = json.dumps(
        {"seconds": 3605, "readingDate": Date, "entityType": 2})
    ListenData = json.dumps(
        {"seconds": 3605, "readingDate": Date, "entityType": 3})
    for _ in range(3):
            
        timestamp = int(time.time() * 1000)
        sign = md5_hex(f"{nonce}{timestamp}{device_token}{SALT}", 'Upper')
        headers['sfsecurity'] = f'nonce={nonce}&timestamp={timestamp}&devicetoken={device_token}&sign={sign}'
        resp = requests.put(
            "https://api.sfacg.com/user/newSignInfo", headers=headers, data=signDate).json()
        # print(resp)
        if('status' in resp and resp['status']['httpCode'] == 200):
            couponNum += resp['data'][0]['num']
            
        timestamp = int(time.time() * 1000)
        sign = md5_hex(f"{nonce}{timestamp}{device_token}{SALT}", 'Upper')
        headers['sfsecurity'] = f'nonce={nonce}&timestamp={timestamp}&devicetoken={device_token}&sign={sign}'
        requests.put('https://api.sfacg.com/user/readingtime',
                     headers=headers, data=ListenData)
            
        timestamp = int(time.time() * 1000)
        sign = md5_hex(f"{nonce}{timestamp}{device_token}{SALT}", 'Upper')
        headers['sfsecurity'] = f'nonce={nonce}&timestamp={timestamp}&devicetoken={device_token}&sign={sign}'
        requests.put('https://api.sfacg.com/user/readingtime',
                     headers=headers, data=ReadData)
        
        timestamp = int(time.time() * 1000)
        sign = md5_hex(f"{nonce}{timestamp}{device_token}{SALT}", 'Upper')
        headers['sfsecurity'] = f'nonce={nonce}&timestamp={timestamp}&devicetoken={device_token}&sign={sign}'
        requests.post('https://api.sfacg.com/user/tasks/5',
                      headers=headers, data=ListenData)
        
        timestamp = int(time.time() * 1000)
        sign = md5_hex(f"{nonce}{timestamp}{device_token}{SALT}", 'Upper')
        headers['sfsecurity'] = f'nonce={nonce}&timestamp={timestamp}&devicetoken={device_token}&sign={sign}'
        requests.post('https://api.sfacg.com/user/tasks/17',
                      headers=headers, data=ListenData)
        for _ in range(3):

            timestamp = int(time.time() * 1000)
            sign = md5_hex(f"{nonce}{timestamp}{device_token}{SALT}", 'Upper')
            headers['sfsecurity'] = f'nonce={nonce}&timestamp={timestamp}&devicetoken={device_token}&sign={sign}'
            requests.put('https://api.sfacg.com/user/readingtime',
                         headers=headers, data=ListenData)
            time.sleep(0.5)
            
            timestamp = int(time.time() * 1000)
            sign = md5_hex(f"{nonce}{timestamp}{device_token}{SALT}", 'Upper')
            headers['sfsecurity'] = f'nonce={nonce}&timestamp={timestamp}&devicetoken={device_token}&sign={sign}'
            resp = requests.put(
                'https://api.sfacg.com/user/tasks/5', headers=headers, data=ListenData).json()
            # print(resp)
            if(resp['status']['httpCode'] == 200):
                fireCoin += resp['data']['fireCoin']
                exp += resp['data']['exp']
            
            timestamp = int(time.time() * 1000)
            sign = md5_hex(f"{nonce}{timestamp}{device_token}{SALT}", 'Upper')
            headers['sfsecurity'] = f'nonce={nonce}&timestamp={timestamp}&devicetoken={device_token}&sign={sign}'
            resp = requests.put(
                'https://api.sfacg.com/user/tasks/17', headers=headers, data='').json()
            # print(resp)
            if(resp['status']['httpCode'] == 200):
                fireCoin += resp['data']['fireCoin']
                exp += resp['data']['exp']
                
        timestamp = int(time.time() * 1000)
        sign = md5_hex(f"{nonce}{timestamp}{device_token}{SALT}", 'Upper')
        headers['sfsecurity'] = f'nonce={nonce}&timestamp={timestamp}&devicetoken={device_token}&sign={sign}'
        url = f"https://api.sfacg.com/user/tasks?taskCategory=5&package=com.sfacg&deviceToken={device_token.lower()}&page=0&size=10"
        print(requests.get(url, headers=headers).json())
        
        timestamp = int(time.time() * 1000)
        sign = md5_hex(f"{nonce}{timestamp}{device_token}{SALT}", 'Upper')
        headers['sfsecurity'] = f'nonce={nonce}&timestamp={timestamp}&devicetoken={device_token}&sign={sign}'
        url = "https://api.sfacg.com/user/tasks/21"
        print(requests.post(url, headers=headers).json())  
        
        for _ in range(5):
            
            timestamp = int(time.time() * 1000)
            sign = md5_hex(f"{nonce}{timestamp}{device_token}{SALT}", 'Upper')
            headers['sfsecurity'] = f'nonce={nonce}&timestamp={timestamp}&devicetoken={device_token}&sign={sign}'
            url = f"https://api.sfacg.com/user/advertisements?deviceToken={device_token.lower()}&page=0&size=20"
            requests.get(url, headers=headers)   
            
            timestamp = int(time.time() * 1000)
            sign = md5_hex(f"{nonce}{timestamp}{device_token}{SALT}", 'Upper')
            headers['sfsecurity'] = f'nonce={nonce}&timestamp={timestamp}&devicetoken={device_token}&sign={sign}'
            url = f"https://api.sfacg.com/user/tasks/21/advertisement?aid=43&deviceToken={device_token.lower()}"
            requests.put(url, headers=headers, data=json.dumps({"num": 1}))
            
            timestamp = int(time.time() * 1000)
            sign = md5_hex(f"{nonce}{timestamp}{device_token}{SALT}", 'Upper')
            headers['sfsecurity'] = f'nonce={nonce}&timestamp={timestamp}&devicetoken={device_token}&sign={sign}'
            resp = requests.put("https://api.sfacg.com/user/tasks/21",
                                headers=headers, data='').json()
            if(resp['status']['httpCode'] == 200):
                couponNum += resp['data']['couponNum']
        time.sleep(5)
def test(cookie):
    print("\n=== 开始测试接口 ===")
    
    if not check(cookie):
        print("Cookie无效,请重新登录")
        return
        
#     downloader = NovelDownloader(cookie)
    
#     balance = downloader.get_balance()
#     print(f"账户余额: {balance}")
    
#     novelName, chapters = downloader.buy_novel_chapters()
#     print(f"购买小说: {novelName}")
#     print(f"购买章节: {chapters}")
#     downloader.save_content(novelName, chapters)        
    print("\n=== 接口测试完成 ===")


if __name__ == "__main__":
    users = os.environ.get('username').split(',')  
    for user in users:
        username, password = user.split('|')
        SFCommunity, session_APP = login(username, password)
        if (not check(f".SFCommunity={SFCommunity}; session_APP={session_APP}")):
            print(f"登录失败")
            continue
        checkin(f".SFCommunity={SFCommunity}; session_APP={session_APP}")
#         downloader = NovelDownloader(f".SFCommunity={SFCommunity}; session_APP={session_APP}")
        jianjie, novelName, chapters = downloader.buy_novel_chapters()
        downloader.save_content(jianjie, novelName, chapters)
