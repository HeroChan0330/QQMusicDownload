# -*- coding: GB2312 -*-
#attention:only for learning!
#this program can`t get the music file if the music has to be payed
#reference:http://www.jb51.net/article/109229.htm
#reference:https://segmentfault.com/a/1190000007685830
#coded by HeroChanSysu 2018/2/18

import requests
import random
import time
import json
guid=0

def GetGUID():#get the matched GUID
    global guid
    guid = int(random.random() * 2147483647) * int(time.time() * 1000) % 10000000000
def GetMusicKey(cid,songmid,filename):#the request that get the vkkey return json
    global guid
    requestUrl='https://c.y.qq.com/base/fcgi-bin/fcg_music_express_mobile3.fcg?g_tk=5381&loginUin=0&hostUin=0&format=json&inCharset=utf8&outCharset=utf-8&notice=0&platform=yqq&needNewCode=0&cid=%s&uin=0&songmid=%s&filename=%s&guid=%s'
    GetGUID()
    #print guid
    res=requests.get(requestUrl%(cid,songmid,filename,guid))
    return res.text
    
def Analyze(requestRes):#analyze the http request result and return the target music file url
    global guid
    data=json.loads(requestRes)
    #print data['data']
    vkey=data['data']['items'][0]['vkey']
    filename=data['data']['items'][0]['filename']
    tarUrl='http://dl.stream.qqmusic.qq.com/%s?vkey=%s&guid=%s&uin=0&fromtag=66'
    return tarUrl%(filename,vkey,guid)

def Search(keyword):#return the result according the key world
    requestUrl='http://s.music.qq.com/fcgi-bin/music_search_new_platform?t=0&n=50&aggr=1&cr=1&loginUin=0&format=json&inCharset=GB2312&outCharset=utf-8&notice=0&platform=jqminiframe.json&needNewCode=0&p=1&catZhida=0&remoteplace=sizer.newclient.next_song&w='+keyword
    #print requestUrl
    res=requests.get(requestUrl)
    res.encoding='utf8'
    return json.loads(res.text)

def PrintSearchRes(result):#print the serach result and wait for input
    index=0
    for item in result['data']['song']['list']:
        if item:
            ids=item['f'].split('|')
            if len(ids)>20:
                songid=ids[20]
                print " [%s] name:%s\tsinger:%s\tsongid:%s"%(index,item['fsong'],item['fsinger'],songid)
            else:
                print '[%s] ————Unable to find the songid————'%index
        index+=1
    print 'Please Select the song`s index'
    select=int(input())
    print 'The file url is:'
    print(GetMp3Url(result['data']['song']['list'][select]))

def GetMp3Url(item):#get the target mp3 file url according the client`s selection from console window
    if item:
        ids=item['f'].split('|')
        if ids.count>20:
            songid=ids[20]
        #I think the cid means client Id, Each client has it`s own unique cid, maybe it won`t work in other machine
        #so you should scratch the package from QQMusic`s website to analyze your own cid
        res1=GetMusicKey('205361747',songid,'C400'+songid+'.m4a')
        return Analyze(res1)

print 'please input keyword'
kw=raw_input()
kw_Utf8=kw.decode('GB2312').encode('utf8')
PrintSearchRes(Search(kw_Utf8))