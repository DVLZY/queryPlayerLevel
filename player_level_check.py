import requests
import json
from bs4 import BeautifulSoup

headers = {'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'}
l_name = "林丹 谌龙 辣子鸡 石宇奇"
for name in l_name.split(' '):
    response = requests.request("GET"
                                , "https://ydydj.univsport.com/index.php?a=seach_look&item=36.1&user_name=%s" % name
                                , headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    content = soup.select_one('div.jieguo_main i').get_text()
    if content != "0":
        crt_id = soup.select_one('div.main_lista p').get('id')
        response = requests.request("POST"
                                    , "https://ydydj.univsport.com/index.php?a=get_detail"
                                    , headers=headers
                                    , data="id=" + crt_id)
        rank_tilte = json.dumps(response.json()['data']['rank_tilte'], indent=4, ensure_ascii=False)  # 运动等级
        athlete_near_pic = json.dumps(response.json()['data']['athlete_near_pic'], indent=4, ensure_ascii=False)  # 照片
        event_time = json.dumps(response.json()['data']['event_time'], indent=4, ensure_ascii=False)  # 时间
        event_name = json.dumps(response.json()['data']['event_name'], indent=4, ensure_ascii=False)  # 比赛
        small_item_name = json.dumps(response.json()['data']['small_item_name'], indent=4, ensure_ascii=False)  # 项目
        event_grade = json.dumps(response.json()['data']['event_grade'], indent=4, ensure_ascii=False)  # 名次
        print(
            f"[{name}]\t[{rank_tilte}]\t[{event_time}{event_name}{small_item_name}{event_grade}]\t[{athlete_near_pic}]")
    else:
        print(f"[{name}]\t[未找到]")
