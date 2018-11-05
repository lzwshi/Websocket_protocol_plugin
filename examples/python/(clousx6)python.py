#!/usr/bin/env python
# -*- coding: utf-8 -*-


#pip install ws4py
#pip install pycurl
from ws4py.client.threadedclient import WebSocketClient
import json;
import re;
import pycurl;
import io;
from urllib.parse import quote;

def sendTo(socket,message_to_send,groupid,type,img_path_to_send,groupidName):
    message_json = json.loads("{}");
    message_json["method"] = str("send_message");
    message_json["message"] = str(message_to_send);
    message_json["groupid"] = int(groupid);
    message_json["type"] = int(type);
    message_json["img_path"] = str(img_path_to_send);
    message_to_send_json = json.loads("{}");
    message_to_send_json["from"]=str("client");
    message_to_send_json["msgparams"]=message_json;
    socket.send(json.dumps(message_to_send_json));
    log="\033[35m发送到群\033[0m: \033[32m%s\033[0m 消息: \033[31m%s%s\033[0m" %(groupidName,message_to_send,img_path_to_send);
    print(log);


def memberManager(socket,message_to_send,qquin,groupid,type,time):
    message_json = json.loads("{}");
    message_json["method"] = str("mamber_manager");
    message_json["message"] = str(message_to_send);
    message_json["qquin"] = int(qquin);
    message_json["groupid"] = int(groupid);
    message_json["type"] = int(type);
    message_json["time"] = int(time);
    message_to_send_json = json.loads("{}");
    message_to_send_json["from"]=str("client");
    message_to_send_json["msgparams"]=message_json;
    socket.send(json.dumps(message_to_send_json));

def Curl_Redirect(url):
    c = pycurl.Curl();
    c.setopt(pycurl.URL,url);
    c.setopt(pycurl.USERAGENT,"Mozilla/5.0 (Linux; U; Android 7.1.2; zh-Hans-CN; ONEPLUS A5010 Build/NJH47F) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/57.0.2987.108 Quark/2.4.2.986 Mobile Safari/537.36");
    c.setopt(pycurl.CUSTOMREQUEST,"GET");
    c.setopt(pycurl.FOLLOWLOCATION, 1);
    c.setopt(pycurl.TIMEOUT, 1000);
    body = io.BytesIO();
    c.setopt(pycurl.WRITEFUNCTION, body.write);
    c.perform();
    redirect_url=c.getinfo(pycurl.EFFECTIVE_URL);
    c.close;
    return redirect_url;


def Curl_Post(url,data):
    c = pycurl.Curl();
    c.setopt(pycurl.URL,url);
    c.setopt(pycurl.USERAGENT,"Mozilla/5.0 (Linux; U; Android 7.1.2; zh-Hans-CN; ONEPLUS A5010 Build/NJH47F) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/57.0.2987.108 Quark/2.4.2.986 Mobile Safari/537.36");
    c.setopt(pycurl.CUSTOMREQUEST,"POST");
    c.setopt(pycurl.POSTFIELDS,  data);
    c.setopt(pycurl.TIMEOUT, 1000);
    body = io.BytesIO();
    c.setopt(pycurl.WRITEFUNCTION, body.write);
    c.perform();
    html = body.getvalue();
    result=str(html,encoding = "utf8");
    c.close;
    return result;

def Curl_Get(url):
    c = pycurl.Curl();
    c.setopt(pycurl.URL,url);
    c.setopt(pycurl.USERAGENT,"Mozilla/5.0 (Linux; U; Android 7.1.2; zh-Hans-CN; ONEPLUS A5010 Build/NJH47F) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/57.0.2987.108 Quark/2.4.2.986 Mobile Safari/537.36");
    c.setopt(pycurl.CUSTOMREQUEST,"GET");
    c.setopt(pycurl.TIMEOUT, 1000);
    body = io.BytesIO();
    c.setopt(pycurl.WRITEFUNCTION, body.write);
    c.perform();
    html = body.getvalue();
    result=str(html,encoding = "utf8");
    c.close();
    return result;

def Netease_Music(song, position,mode):
    message_to_send ="";
    param = "hlpretag=<span class=\"s-fc2\">&hlposttag=</span>&s=" + quote(song.replace("\"","")) + "&offset=0&total=true&limit=10&type=1";
    info = Curl_Post("http://music.163.com/api/search/pc", param);
    songs_json = json.loads(info);
    songs_list = songs_json["result"]["songs"];
    songs_list_length = len(songs_list);
    if mode == 1:
        data = songs_list[position - 1];
        song_name = data["name"];
        song_id = data["id"];
        author_name = data["artists"][0]["name"];
        img = data["album"]["picUrl"];
        #String album_name =data.getJSONObject("album").getString("name");
        play_url = Curl_Redirect("http://music.163.com/song/media/outer/url?id=" + str(song_id) + ".mp3");
        if play_url == "http://music.163.com/404":
            message_to_send = "<msg serviceID=\"1\" brief=\"点歌失败\" flag=\"3\" templateID=\"1\"><item bg=\"#00BFFF\" layout=\"4\"><title color=\"#FFFFFF\" size=\"28\">该歌曲无外链</title></item></msg>";
        else:
            message_to_send = "<msg serviceID=\"2\" templateID=\"1\" action=\"web\" brief=\"网易音乐\" sourceMsgId=\"0\" url=\"\" flag=\"0\" adverSign=\"0\" multiMsgFlag=\"0\"><item layout=\"2\"><audio cover=\"" + img + "\" src=\"" + play_url + "\" /><title>" + song_name + "</title><summary>" + author_name + "</summary></item><source name=\"网易云音乐\" icon=\"https://url.cn/5TxJvzz\" url=\"http://url.cn/5pl4kkd\" action=\"app\" a_actionData=\"com.netease.cloudmusic\" i_actionData=\"tencent100495085://\" appid=\"205141\" /></msg>";
    elif mode == 2:
        time=0;
        while (time < songs_list_length):
            author_name = songs_list[time]["artists"][0]["name"];
            if re.match(position + ".*",author_name) != None: 
                message_to_send = Netease_Music(song, time + 1, 1);
                break;
            time=time+1;
        if message_to_send == "":
            message_to_send = "<msg serviceID=\"1\" brief=\"匹配失败\" flag=\"3\" templateID=\"1\"><item bg=\"#00BFFF\" layout=\"4\"><title color=\"#FFFFFF\" size=\"28\">未匹配到指定歌手</title></item></msg>";
    elif mode == 3:
        xml="<msg serviceID=\"1\" templateID=\"1\" action=\"web\" brief=\"点歌列表\" url=\"\" flag=\"3\"><item layout=\"5\"><picture cover=\"https://i.loli.net/2018/10/02/5bb37e1e7d09b.png\"/></item><item layout=\"6\"><summary  color=\"#32CD32\" style=\"1\">";
        line ="<item><hr/></item>";
        time=0;
        while (time < songs_list_length):
            data = songs_list[time];
            song_name = data["name"];
            author_name = data["artists"][0]["name"];
            if len(song_name) >10:
                song_name = song_name[:10] + "...";
            if len(author_name) >20:
                author_name = author_name[:20] + "...";
            xml = xml + str(time + 1) + ":" + song_name + "   " + author_name +  "@@@#10;"
            time=time+1;
        message_to_send = xml + "</summary></item></msg>";
    return message_to_send;

def Kugou_Music(song, position,mode):
    message_to_send ="";
    info = Curl_Get("http://songsearch.kugou.com/song_search_v2?keyword=" + quote(song) + "&page=0&pagesize=10&userid=-1&clientver=&platform=WebFilter&tag=em&filter=2&iscorrection=1&privilege_filter=0");
    songs_json = json.loads(info);
    songs_list = songs_json["data"]["lists"];
    songs_list_length = len(songs_list);
    if mode == 1:
        File_hash = songs_list[position -1]["FileHash"];
        data = json.loads(Curl_Get("http://www.kugou.com/yy/index.php?r=play/getdata&hash=" + File_hash))["data"];
        img = data["img"];
        author_name = data["author_name"];
        song_name = data["song_name"];
        play_url = data["play_url"];
        message_to_send = "<msg serviceID=\"2\" templateID=\"1\" action=\"web\" brief=\"酷狗音乐\" sourceMsgId=\"0\" url=\"\" flag=\"0\" adverSign=\"0\" multiMsgFlag=\"0\"><item layout=\"2\"><audio cover=\"" + img + "\" src=\"" + play_url + "\" /><title>" + song_name + "</title><summary>" + author_name + "</summary></item><source name=\"酷狗音乐\" icon=\"http://url.cn/4Asex5p\" url=\"http://url.cn/SXih4O\" action=\"app\" a_actionData=\"com.kugou.android\" i_actionData=\"tencent205141://\" appid=\"205141\" /></msg>";
    elif mode == 2:
        time=0;
        while (time < songs_list_length):
            author_name = songs_list[time]["SingerName"];
            if re.match(position + ".*",author_name) != None: 
                message_to_send = Kugou_Music(song, time + 1, 1);
                break;
            time=time+1;
        if message_to_send == "":
            message_to_send = "<msg serviceID=\"1\" brief=\"匹配失败\" flag=\"3\" templateID=\"1\"><item bg=\"#00BFFF\" layout=\"4\"><title color=\"#FFFFFF\" size=\"28\">未匹配到指定歌手</title></item></msg>";
    elif mode == 3:
        xml="<msg serviceID=\"1\" templateID=\"1\" action=\"web\" brief=\"点歌列表\" url=\"\" flag=\"3\"><item layout=\"5\"><picture cover=\"https://i.loli.net/2018/10/02/5bb37e1e7d09b.png\"/></item><item layout=\"6\"><summary  color=\"#32CD32\" style=\"1\">";
        line ="<item><hr/></item>";
        time=0;
        while (time < songs_list_length):
            File_hash = songs_list[time]["FileHash"];
            song_detail_json = json.loads(Curl_Get("http://www.kugou.com/yy/index.php?r=play/getdata&hash=" + File_hash))["data"];
            img = song_detail_json["img"];
            author_name = song_detail_json["author_name"];
            song_name = song_detail_json["song_name"];
            if len(song_name) >10:
                song_name = song_name[:10] + "...";
            if len(author_name) >20:
                author_name = author_name[:20] + "...";
            xml = xml + str(time + 1) + ":" + song_name + "   " + author_name +  "@@@#10;"
            time=time+1;
        message_to_send = xml + "</summary></item></msg>";
    return message_to_send;


def onQQMessage(socket,type,groupid,sendid,msg,nick,ATQ,ATname,robort,sendtime,groupidName):
    if len(re.findall("\], at=\[.*",msg)) != 0:
        msg=msg.replace(re.findall("\], at=\[.*",msg)[0],"");
    #socket----websocket对象
    #type----消息类型
    #groupid----群号码
    #sendid----信息发出者qq号码
    #msg----消息内容
    #nick----消息发出者qq昵称
    #ATQ----被艾特的qq号
    #ATname----被艾特qq昵称
    #robort----登陆机器人qq号码
    #sendtime----消息发送时间
    #groupidName----群名称
    if msg == "Hello":  #文本消息测试
        #@sendTo(socket,message_to_send,groupid,type,img_path_to_send,groupidName)
        #socket----websocket对象本身
        #message_to_send----消息内容
        #groupid----群号
        #type----消息类型 1:文本消息 2:卡片消息 4:开启全体禁言 5:关闭全体禁言 8:加群 9: 退群  12: 文字加图片消息
        #groupidName群名字，记录用
        sendTo(socket,"World",groupid,1,"",groupidName);
    elif msg == "测试卡片": #xml消息测试
        sendTo(socket,"<msg serviceID=\"2\" templateID=\"1\" action=\"web\" brief=\"酷狗音乐\" sourceMsgId=\"0\" url=\"\" flag=\"0\" adverSign=\"0\" multiMsgFlag=\"0\"><item layout=\"2\"><audio cover=\"http://singerimg.kugou.com/uploadpic/softhead/400/20170426/20170426152155521.jpg\" src=\"http://fs.w.kugou.com/201809150140/0fe84be3831cea79c86d693e721f0e7b/G012/M07/01/09/rIYBAFUKilCAV55kADj2J33IqoI680.mp3\" /><title>Innocence</title><summary>Avril Lavigne</summary></item><source name=\"酷狗音乐\" icon=\"http://url.cn/4Asex5p\" url=\"http://url.cn/SXih4O\" action=\"app\" a_actionData=\"com.kugou.android\" i_actionData=\"tencent205141://\" appid=\"205141\" /></msg>",groupid,2,"",groupidName);
    elif msg == "测试图片": #图片消息测试
        sendTo(socket,"这是图片",groupid,12,"https://i.loli.net/2018/10/10/5bbda09b17a1a.png",groupidName);
    elif re.match("开启全体禁言",msg) != None: #全体禁言
        sendTo(socket,"World",groupid,4,"",groupidName);
    elif re.match("关闭全体禁言",msg) != None: #全体禁言
        sendTo(socket,"World",groupid,5,"",groupidName);
    elif re.match("^禁@.*? .*",msg) != None:  #发送禁@需要禁言的qq，最后面加上禁言时长秒数
        #@memberManager(socket,message_to_send,qquin,groupid,type,time)
        #socket----websocket对象本身
        #message_to_send----名片内容
        #qquin----要操作的qq号
        #groupid----群号
        #time----禁言秒数
        #type----消息类型 7:禁言 10:踢人 11:改名片
        #加群退群不做演示
        memberManager(socket,"",ATQ,groupid,7,msg.split(" ")[-1]);    
    elif re.match("^踢@.*",msg) != None: #发送禁@需要踢出的qq，没试过
        memberManager(socket,"",ATQ,groupid,10,0,);
    elif re.match("^改@.*? .*",msg) != None: #发送禁@需要改名片的qq，最后面加上名片
        memberManager(socket,msg.split(" ")[-1],ATQ,groupid,11,0);
    elif re.match("^转卡片 .*",msg) != None: #发送禁@需要改名片的qq，最后面加上名片
        sendTo(socket,msg.replace("转卡片 ",""),groupid,2,"",groupidName);
    elif re.match("^网易点歌 .*",msg) != None:
        song="";
        singer="";
        song_list="false";
        song_position="false";
        singer_really_contented="false";
        message_to_send="";
        message_list=re.split("\s+",msg);
        if len(message_list) >= 2:
            song = message_list[1].replace("_", " ");
        if len(message_list) >= 3:
            singer = message_list[2].replace("_", " ");
            if re.match("[0-9]",singer) == None:
                singer_really_contented = "true";
            else:
                position = int(singer);
                song_position = "true";
        else:
            song_list="true";
        if song_position == "true":
            if position != 0:
                message_to_send = Netease_Music(song, position, 1);
            else:
                message_to_send = "<msg serviceID=\"33\" brief=\"格式错误\" flag=\"3\" templateID=\"1\"><item bg=\"#00BFFF\" layout=\"4\"><title color=\"#FFFFFF\" size=\"28\">序号必须大于0</title></item></msg>";
        elif singer_really_contented == "true":
            message_to_send = Netease_Music(song, singer, 2);
        elif song_list == "true":
            message_to_send = Netease_Music(song, singer, 3);
            message_to_send = message_to_send.replace("&", "&amp;").replace("@@@", "&");
        sendTo(socket,message_to_send,groupid,2,"",groupidName);
    elif re.match("^酷狗点歌 .*",msg) != None:
        song="";
        singer="";
        song_list="false";
        song_position="false";
        singer_really_contented="false";
        message_to_send="";
        message_list=re.split("\s+",msg);
        if len(message_list) >= 2:
            song = message_list[1].replace("_", " ");
        if len(message_list) >= 3:
            singer = message_list[2].replace("_", " ");
            if re.match("[0-9]",singer) == None:
                singer_really_contented = "true";
            else:
                position = int(singer);
                song_position = "true";
        else:
            song_list="true";
        if song_position == "true":
            if position != 0:
                message_to_send = Kugou_Music(song, position, 1);
            else:
                message_to_send = "<msg serviceID=\"33\" brief=\"格式错误\" flag=\"3\" templateID=\"1\"><item bg=\"#00BFFF\" layout=\"4\"><title color=\"#FFFFFF\" size=\"28\">序号必须大于0</title></item></msg>";
        elif singer_really_contented == "true":
            message_to_send = Kugou_Music(song, singer, 2);
        elif song_list == "true":
            message_to_send = Kugou_Music(song, singer, 3);
            message_to_send = message_to_send.replace("&", "&amp;").replace("@@@", "&");
        sendTo(socket,message_to_send,groupid,2,"",groupidName);
    elif re.match(".*qqbot.*发图.*",msg) != None:
        sendTo(socket,"qqbot不支持发图再问打死",groupid,1,"",groupidName);
    elif re.match(".*qqbot.*at.*",msg) != None or re.match(".*qqbot.*艾特.*",msg) != None:
        sendTo(socket,"qqbot不支持艾特再问打死",groupid,1,"",groupidName);
    elif re.match(".*qqbot.*获取.*号",msg) != None:
        sendTo(socket,"qqbot不支持获取qq号/群号再问打死",groupid,1,"",groupidName);

def Message_Factory(socket,message):
    message_json = json.loads(str(message));
    message_json = message_json['msgparams'];
    type=message_json["type"];
    groupid=message_json["groupid"];
    sendid=message_json["sendid"];
    msg=message_json["message"];
    nick=message_json["nick"];
    ATQ=message_json["ATQ"];
    ATname=message_json["ATname"]; 
    robort=message_json["robort"]; 
    sendtime=message_json["sendtime"];     
    groupidName=message_json["groupidname"];
    log="\033[33m收到来自群:\033[0m \033[32m%s\033[0m 的成员: \033[36m%s\033[0m 的消息: \033[31m%s\033[0m"  %(groupidName,nick,msg);
    print(log);
    onQQMessage(socket,type,groupid,sendid,msg,nick,ATQ,ATname,robort,sendtime,groupidName);


class DummyClient(WebSocketClient):
    def opened(self):
        print("connected");
    def closed(self, code, reason=None):
        print ("Closed down", code, reason)
    def received_message(self, message):
        Message_Factory(self,message)
        

if __name__ == '__main__':
    try:
        ws = DummyClient('ws://192.168.2.172:8888')
        ws.connect()
        ws.run_forever()
    except KeyboardInterrupt:
        ws.close()