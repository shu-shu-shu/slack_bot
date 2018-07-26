#coding: utf-8
from slackbot.bot import respond_to     # @botname: で反応するデコーダ
from slackbot.bot import listen_to      # チャネル内発言で反応するデコーダ
from slackbot.bot import default_reply  # 該当する応答がない場合に反応するデコーダ
import os
import subprocess
import json
import re

BLACK_BEAN_DIR = "./../BlackBeanControl/" #リモコン操作のeRemoteのスクリプトディレクトリ
CURRENT_DIR = os.getcwd()
print(CURRENT_DIR)
def_reply = "知らんがな"
filename = "slack.json"
json_dic = []

with open(filename, "r") as fp:
    json_dic = json.load(fp) #json形式のファイルを読み込む、辞書型になる
print(json_dic.keys())

#slack.jsonにあるkeyをメンションした場合その値を返す
#keyがxx_countの場合それをインクリメントする
@default_reply()
def default_func(message):
    text = message.body['text'].strip()
    if (text in json_dic):
        pattern = r"count"
        print(text)
        print(re.search(pattern, text))
        if (re.search(pattern, text) != None):
            json_dic[text] = str(int(json_dic[text]) + 1)
            print("count plus one")
        print(type(json_dic[text]))
        if isinstance(json_dic[text], str):
            print(json_dic[text])
            message.reply(json_dic[text])
        elif isinstance(json_dic[text], int):
            print(json_dic[text])
            message.reply(str(json_dic[text]))
    else:
       # message.reply(def_reply)
        message.reply(text)
        print(text)

#slack.jsonを渡す
@respond_to("list")
def ret_list(message):
    ret = json.dumps(json_dic, indent=2, ensure_ascii=False)
    message.reply(ret)

#help
@respond_to("help")
def ret_help(message):
    ret = '{\n"list":"slack.jsonを渡す",\n "reload":"slack.jsonを書き換えたら使用\",\n "json xxx":"slack.jsonに追加",\n "light off":"ライト消す",\n "light on":"ライトつける",\n "night mode":"明かりをナイトモードにする",\n "too hot":"エアコンをつける",\n "air conditioning off":"エアコンOFF"\n }'
    message.reply(ret)
    #message.reply("hello")


#slack.jsonを読み込む(先に読み込むことでdefault replyを早くする)
@respond_to('reload')
def reload_json(message):
    global json_dic
    with open(filename, "r") as fp:
        json_dic = json.load(fp) #json形式のファイルを読み込む、辞書型になる
    print(json_dic.keys())

#@respond_to(r'^set\s+\S.*') #set xxの場合
#    text = message.body['text']
#    temp, word = text.split(None, 1)
#    with open(filename, "r") as fp:
#        r = json.load(fp) #json形式のファイルを読み込む、辞書型になる

#"json xx"でxxをjsonファイルとしてslack.jsonに保存する。json形式であることは確かめていないwww
@respond_to(r'^json\s+\S.*') #json xxの場合
def set_json(message):
    text = message.body['text']
    temp, json_text = text.split(None, 1)
    with open(filename, "w") as fp:
        fp.write(json_text)

#test.jsonが作られる
@respond_to("test")
def set_json(message):
    data = {
        "traning":0,
        "燃えるゴミ":"月曜日・木曜日"
    }
    filename = "test.json"
    with open(filename, "w") as fp:
        json.dump(data, fp, indent=2, ensure_ascii=False)


@respond_to('light on')
def mention_func(message):
    os.chdir(BLACK_BEAN_DIR)
    subprocess.run("python BlackBeanControl.py -c light_power_on", shell=True)
    os.chdir(CURRENT_DIR)
    message.reply('電気つけたよ') # メンション

@respond_to('light off')
def mention_func(message):
    os.chdir(BLACK_BEAN_DIR)
    subprocess.run("python BlackBeanControl.py -c light_power_off", shell=True)
    os.chdir(CURRENT_DIR)
    message.reply('電気消したよ') # メンション

@respond_to('night mode')
def mention_func(message):
    os.chdir(BLACK_BEAN_DIR)
    for i in range(5):
        subprocess.run("python BlackBeanControl.py -c light_orenge", shell=True)
    os.chdir(CURRENT_DIR)
    message.reply('ナイトモード') # メンション

@respond_to('too hot')
def mention_func(message):
    os.chdir(BLACK_BEAN_DIR)
    subprocess.run("python BlackBeanControl.py -c air_conditioning_power_on", shell=True)
    os.chdir(CURRENT_DIR)
    message.reply('暑いからエアコン点けといたよ')

@respond_to('air conditioning off')
def mention_func(message):
    os.chdir(BLACK_BEAN_DIR)
    subprocess.run("python BlackBeanControl.py -c air_conditioning_power_off", shell=True)
    os.chdir(CURRENT_DIR)
    message.reply('エアコン消したよ')

