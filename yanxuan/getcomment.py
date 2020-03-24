import requests
from requests.exceptions import ConnectionError, ConnectTimeout
from pymongo import MongoClient
import time
from multiprocessing import Pool
client = MongoClient('localhost', 27017)
db = client['yanxuan']
sheet = db['phonemask']
headers = {
    'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36',
    'Accept': '*/*',
    'Host': 'you.163.com',
    'accept-encoding': 'gzip, deflate',
    'cookies': '_ntes_nuid=7b25136195bc611d7c2d34146803238a; mail_psc_fingerprint=d769bd08119accb9cd233eb966408474; usertrack=CrH5jV1nyntmg20JAwgmAg==; _ntes_nnid=c84b4aadf4e45d297a74a25b0e5cb3a8,1567082945331; P_INFO=hssss@126.com|1567083815|0|mail126|11&99|nmg&1566559383&yanxuan#nmg&150100#10#0#0|&0|yanxuan|hssss@126.com; yx_delete_cookie_flag=true; yx_aui=8097af98-35a7-4612-8f0b-5cb7d454160a; yx_s_device=ba88695-e6b5-393a-e7b3-af3e68a146; yx_s_tid=tid_web_8ca0cfd7941e430abd831952bb120f90_1f3f590f3_1; yx_but_id=9970c18b3c0e4313a0da5af039fdc2fc2aab726fa6cc7dc9_v1_nl; user-close-downloadGuide=true; yx_new_user_modal_show=1; yx_show_painted_egg_shell=false; yx_search_history=%5B%22%u725B%u4ED4%22%2C%22%u544A%u522B%u5543%u98DF%u5C34%u5C2C%uFF0C%u79D8%u5236%u65E0%u9AA8%u51E4%u722A%22%5D; yx_stat_seesionId=8097af98-35a7-4612-8f0b-5cb7d454160a1584936047617; yx_page_key_list=http%3A//you.163.com/%2Chttp%3A//you.163.com/item/detail%3Fid%3D3383008%26_stat_referer%3Dindex%26_stat_area%3Dmod_popularItem_item_1; yx_stat_seqList=v_cdee60ea0f%7Cv_602f0a7050%3Bc_2dbab4a949%3Bv_cdee60ea0f%3B-1'
}


def search_keyword(keyword):
    url = 'https://you.163.com/xhr/search/search.json'
    query = {
            'keyword': keyword,
            'page': 1
              }
    res = requests.get(url, params=query).json()
    result = res['data']['directly']['searcherResult']['result']
    product_id = []
    for item in result:
        product_id.append(item['id'])
    return product_id


def comment(pid):
    url = 'http://you.163.com/xhr/comment/listByItemByTag.json'
    num = 1

    LASTPAGE=False
    while LASTPAGE is not True:
        try:
            print('正在爬取id%s商品的第%i页' % (str(pid), num))
            query = {
                'itemId': pid,
                'page': num
            }
            res = requests.get(url, params=query, headers=headers).json()
            result = res['data']['commentList']

            for info in result:
                print(info)
                sheet.insert_one(info)
                # sheet.update_one(info, {'$set', info}, upsert=True)
            LASTPAGE=res['data']['pagination']['lastPage']
            num += 1
            time.sleep(1)
        except (ConnectionError, ConnectTimeout, UnicodeEncodeError) as e:
            print('请求异常', e)
            if LASTPAGE is False:
                num += 1
            pass


if __name__ == '__main__':
    pool = Pool()
    lst = search_keyword('手机保护壳')
    pool.map(comment, lst)
    print('任务完成')
