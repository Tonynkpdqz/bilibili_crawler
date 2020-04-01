import requests, re, time, csv
from bs4 import BeautifulSoup as BS


#打开网页函数
def open_url(url):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.103 Safari/537.36', 'Cookie' : "pgv_pvi=8900751360; LIVE_BUVID=AUTO5215113619636033; stardustvideo=1; CURRENT_FNVAL=16; OUTFOX_SEARCH_USER_ID_NCOO=486921251.3064985; im_notify_type_286517911=0; rpdid=|(um~u)l~|RJ0J'ullYJ~|RRR; _uuid=7899C3D5-5821-23AE-97B9-C774A0C4D41041166infoc; LIVE_PLAYER_TYPE=2; laboratory=1-1; CURRENT_QUALITY=0; buvid3=DAB2CB02-49B6-4B42-B4EE-CE36394ED90E155820infoc; INTVER=1; sid=81mtgo49; PVID=2; DedeUserID=286517911; DedeUserID__ckMd5=1f80bc3e87d223ed; SESSDATA=2e99ef67%2C1601271282%2C4db34*41; bili_jct=66e386ca378f073e62e547326e82866f"}
    response = requests.get(url=url, headers=headers)
    response.encoding = 'utf-8'
    html = response.text
    return html


#获取弹幕url中的数字id号
def get_danmu_id(html, url):
    try:
        soup = BS(html, 'lxml')
        #视频名
        title = soup.select('title[data-vue-meta="true"]')[0].get_text()
        #投稿人
        author = soup.select('meta[name="author"]')[0]['content']
        #弹幕的网站代码
        danmu_id = re.findall(r'cid=(\d+)&', html)[0]
        print(title, author)
        return danmu_id
    except:
        print('视频不见了哟')
        return False
#秒转换成时间
def sec2str(seconds):
    seconds = eval(seconds)
    m, s = divmod(seconds, 60)
    h, m = divmod(m, 60)
    time = "%02d:%02d:%02d" % (h, m, s)
    return time

#csv保存函数
def csv_write(tablelist,date):
    tableheader = ['出现时间', '弹幕模式', '字号', '颜色', '发送时间' ,'弹幕池', '发送者id', 'rowID', '弹幕内容']
    with open('danmu_'+date+'.csv', 'w', newline='', errors='ignore') as f:
        writer = csv.writer(f)
        writer.writerow(tableheader)
        for row in tablelist:
            writer.writerow(row)


video_url ='https://www.bilibili.com/video/BV1mk4y1d7BV'
video_html = open_url(video_url)
danmu_id = get_danmu_id(video_html, video_url)
date_list = ['2020-03-28','2020-03-29','2020-03-30','2020-03-31','2020-04-01']
all_list = []
def to_csv(date):
    if(date == 'now'):
        danmu_url = 'http://comment.bilibili.com/{}.xml'.format(danmu_id)
    else:
        danmu_url = 'https://api.bilibili.com/x/v2/dm/history?type=1&oid=170571779&date='+date
    #danmu_url = 'https://api.bilibili.com/x/v1/dm/list.so?oid=170571779&date=2020-3-29'
    #danmu_url = 'http://comment.bilibili.com/{}.xml'.format(danmu_id)
    danmu_html = open_url(url=danmu_url)
    soup = BS(danmu_html, 'lxml')
    all_d = soup.select('d')
    for d in all_d:
        #把d标签中P的各个属性分离开
        danmu_list = d['p'].split(',')
        #d.get_text()是弹幕内容
        danmu_list.append(d.get_text())
        danmu_list[0] = sec2str(danmu_list[0])
        danmu_list[4] = time.ctime(eval(danmu_list[4]))
        all_list.append(danmu_list)
        print(danmu_list)
    all_list.sort()
    csv_write(all_list,date)
for date in date_list :
    to_csv(date)
to_csv('now')