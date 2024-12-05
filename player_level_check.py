import random
import requests

l_name = "林丹 谌龙 辣子鸡 石宇奇"
for name in l_name.split(' '):

    # 获取运动员证书编号
    headers = {'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'}
    response = requests.request("GET"
                                , f"https://zwfw.sport.gov.cn/level.do?m=getLevelList&item=36.1&name={name}"
                                , headers=headers)

    if response.json()['data']['data']['list_data'] is None:
        print(f"[{name}]\t[未找到]")
        continue
    for list_data in response.json()['data']['data']['list_data']:
        # 获取运动员信息编号
        headers = {
            'content-type': 'application/json;charset=UTF-8',
            'requestid': f"{random.randint(1_000_000_000, 9_999_999_999):010d}"  # 逆向生成 requestid 算法
        }
        payload = f'{{"certificateNo":"{list_data['certificate_num']}","athleteRealName":"{name}"}}'
        response = requests.request("POST"
                                    , url="https://ydydj.univsport.com/api/system/athlete/front-end-list"
                                    , headers=headers
                                    , data=payload)
        # 获取运动员信息详情
        payload = f'{{"athleteInfoId":"{response.json()['data']['list'][0]['athleteInfoId']}"}}'
        response = requests.request("POST"
                                    , url="https://ydydj.univsport.com/api/system/athlete/front-end-detail"
                                    , headers=headers
                                    , data=payload)

        # 组装信息
        rank_tilte = response.json()['data']['rankTitle']  # 运动等级
        athlete_near_pic = f"https://ydydj.univsport.com/{response.json()['data']['oneInchPhoto']}"  # 照片
        event_time = response.json()['data']['eventTime']  # 时间
        event_name = response.json()['data']['eventName']  # 比赛
        small_item_name = response.json()['data']['smallItemName']  # 项目
        event_grade = response.json()['data']['eventGrade']  # 名次
        print(
            f"[{name}]\t[{rank_tilte}]\t[{event_time}{event_name}{small_item_name}{event_grade}]\t[{athlete_near_pic}]")
