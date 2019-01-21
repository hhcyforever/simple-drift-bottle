
import socket
import threading
import re
import random
import requests
import urllib
import json
#receive a bottle
# def bottleIn(conn,name):
#     global bottle
#     while True:
#         try:
#             temp = str(conn.recv(1024)).split('####')
#             if len(temp) == 3 and temp[0] == name:
#                 bottle_user.append(temp[0])
#                 bottle_tag.append(temp[1])
#                 bottle_inf.append(temp[2])
#                 msg = temp[0]+" throws a bottle, whose tag is:"+temp[1]
#                 send_to_all(msg)
#
#         except:
#             return

def messageIn(conn,name):
    global bottles
    global bottleId
    global data
    global bottle_for_user
    global reply
    while 1:
        try:
            print ('waitting data...')
            tempStr = str(conn.recv(1024))[2:-1]
            print(tempStr)
            #receive bottle
            if re.match(r'send bottle:(.*)',tempStr):
                realTempStr = re.match(r'send bottle:([\d\D]*)',tempStr).group(1)
                print(realTempStr)
                len_user = int(realTempStr.split('#')[0])
                # print(len_user)
                len_msg = int(realTempStr.split('#')[1])
                # print(len_msg)
                NoHeadString = re.match(r'(\d*)#(\d*)#([\d\D]*)',realTempStr).group(3)
                print(NoHeadString)
                usr = NoHeadString[0:len_user]

                msg = NoHeadString[len_user:len_user+len_msg]
                print(usr)
                print(msg)
                tmp_dict = dict()
                tmp_dict['id'] = bottleId
                tmp_dict['usr'] = usr
                tmp_dict['msg'] = msg
                bottles[str(bottleId)] = tmp_dict
                print(bottles)
                if usr in bottle_for_user.keys():
                    bottle_for_user[usr].append(tmp_dict)
                else:
                    print("false")
                    bottle_for_user[usr] = []
                    bottle_for_user[usr].append(tmp_dict)
                print(bottle_for_user)
                # msg = usr + " throws a bottle --tag:" + tag + " id:"+bottleId
                bottleId += 1
                # print(type(msg))
                # send_to_all(msg)

            #receive request for bottle
            elif re.match(r'try to find bottle:',tempStr):
                # real_id = re.match(r'bottle id:(.*)', tempStr).group(1)
                #judge if exists
                tmp_id = random.randint(0,bottleId-1)
                print(tmp_id)
                tmp_bottle = bottles[str(tmp_id)]
                msg = "fish up bottle:"+str(len(tmp_bottle['msg']))+"#"+str(len(tmp_bottle['usr']))+"#"+str(tmp_bottle['id'])+"#"+tmp_bottle['msg']+tmp_bottle['usr']
                print(msg)
                conn.send(msg.encode('utf-8'))

            elif re.match(r'back bottle reply:([\d\D]*)',tempStr):
                real_reply = re.match(r'back bottle reply:([\d\D]*)',tempStr).group(1)
                lUsr = int(real_reply.split("#")[0])
                lMsg = int(real_reply.split('#')[1])
                id = real_reply.split('#')[2]
                rStr = re.match(r'back bottle reply:([\d]*)#([\d]*)#([\d]*)#([\d\D]*)',tempStr).group(4)
                rUsr = rStr[0:lUsr]
                rMsg = rStr[lUsr:lUsr+lMsg]
                print("usr:"+rUsr)
                print("msg:"+rMsg)
                if id in reply.keys():
                    reply[id].append(rMsg)
                else:
                    reply[id] = []
                    reply[id].append(rMsg)
                print(reply)

            elif re.match(r'send message:(.*)',tempStr):
                message = re.match(r'send message:(.*)',tempStr).group(1)
                send_to_all('message:'+message)
            elif re.match(r'find my bottles:([\d\D]*)',tempStr):
                usr = re.match(r'find my bottles:([\d\D]*)',tempStr).group(1)
                if usr in bottle_for_user.keys():
                    btllist = bottle_for_user[usr]
                    print(btllist)
                    for i in range(0,len(btllist)):
                        id = str(btllist[i]['id'])
                        print(id)
                        btlsend = bottles[id]
                        print(btlsend)
                        btlback = ""
                        if id in reply.keys():
                            print("in keys")
                            for j in range(0,len(reply[id])):
                                print(reply[id][j])
                                btlback += ("reply"+str(j)+":"+reply[id][j]+"      ")
                        ans = "my bottles:"+ id + "#!@"+btlsend['msg'] +"#!@" +btlback
                        print(ans)
                        conn.send(ans.encode('utf-8'))
            elif re.match(r'chat:([\d\D]*)', tempStr):
                chat = re.match(r'chat:([\d\D]*)', tempStr).group(1)
                msg = Turing_chat(chat)
                conn.send(msg.encode('utf-8'))


        except:
            print('error...')
            # msg = name + 'leaves the room'
            # send_to_all(msg)
            return

def messageOut(conn):
    global data
    while 1:
        if con.acquire():
            con.wait()
            if data:
                # print(type(data))
                # print(data)
                print('try to send back...' + data)
                try:
                    conn.send(data.encode('utf-8'))
                    print('success in sending back' + data)
                    con.release()
                except:
                    print('error send back')
                    con.release()

def Turing_chat(info):
    print(info)
    key = '3bdfaee0248a4585b918233d26b81df4'
    api = 'http://www.tuling123.com/openapi/api?key=' + key + '&info=' + info
    responce = requests.get(api)
    print(responce)
    responce.encoding = 'utf-8'
    dic_json = json.loads(responce.text)
    print(dic_json)
    return "Aquaman: " + str(dic_json['text'])

def send_to_all(temS):
    global data
    if con.acquire():
        data = temS
        con.notifyAll()
        con.release()

con = threading.Condition()
data = ''
bottles = {}
bottleId = 0

bottle_for_user = {}

users = {}
userId = 0

reply = {}
replyId = 0

HostPort = ('127.0.0.1', 9898)
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(HostPort)
s.listen(5)
print("waiting to be connected.......")

while 1:
    conn, addr = s.accept()
    print("Connecting by:" + addr[0] + "," + str(addr[1]))
    name = (str(conn.recv(1024)))[2:-1]
    users[str(userId)] = name
    userId += 1
    send_to_all("message:Welcome " + name + " to our room!")
    person_num = int((threading.activeCount() + 1) / 2)
    print("There are " + str(person_num) + " person(s) in our room")
    conn.sendall(data.encode('utf-8'))
    print("welcome message has been sent")
    thrd1 = threading.Thread(target=messageIn, args=(conn, name))
    thrd1.start()
    # thrd3 = threading.Thread(target=bottleIn, args=(conn, name))
    # thrd3.start()
    thrd2 = threading.Thread(target=messageOut, args=(conn,))
    thrd2.start()

