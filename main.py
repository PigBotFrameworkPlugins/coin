import requests, sys, time
sys.path.append('../..')
import go, tools
from plugins.tools.main import zhuan

def bangding(meta_data):
    uid = meta_data.get('se').get('user_id')
    gid = meta_data.get('se').get('group_id')
    message = meta_data.get('message')
    
    if len(meta_data.get('args')) == 1:
        if gid != None:
            go.send(meta_data, '请在频道中发送“绑定频道”')
        else:
            go.send(meta_data, '[CQ:at,qq='+str(uid)+'] 请在任意地方（除频道外）发送“绑定频道 '+str(uid)+'”（不包括双引号）')
    else:
        value = meta_data.get('args')[1]
        go.commonx('UPDATE `botCoin` SET `cid`="'+str(value)+'" WHERE `qn`='+str(uid))
        go.send(meta_data, '绑定成功！')

def toushi(meta_data):
    uid = meta_data.get('se').get('user_id')
    gid = meta_data.get('se').get('group_id')
    cid = meta_data.get('se').get('channel_id')
    uuid = meta_data.get('uuid')
    
    if cid != None:
        strr = 'cid'
        sql = 'UPDATE `botCoin` SET `toushi`=1 WHERE `uuid`="{0}" and `cid`="{1}"'.format(uuid, cid)
        sqlstr = "SELECT * FROM `botCoin` WHERE `uuid`='{0}' and `cid`='{1}'".format(uuid, cid)
    else:
        strr = 'qn'
        sql = 'UPDATE `botCoin` SET `toushi`=1 WHERE `uuid`="{0}" and `qn`={1}'.format(uuid, uid)
        sqlstr = "SELECT * FROM `botCoin` WHERE `uuid`='{0}' and `qn`='{1}'".format(uuid, uid)
    
    coinlist = go.selectx(sqlstr)[0]
    
    if not coinlist:
        go.send(meta_data, '您还没有注册！\n快发送“注册”让猪比认识你吧')
        return
    
    if coinlist.get('toushi') == 0:
        go.commonx(sql)
        go.send(meta_data, '投食成功！\n获得'+str(go.addCoin(meta_data))+'个好感度qwq')
    else:
        meta_data['message'] = '不要贪心啊，你已经投过食啦！'
        zhuan(meta_data)

def zhuce(meta_data, sendFlag=1):
    uid = meta_data.get('se').get('user_id')
    gid = meta_data.get('se').get('group_id')
    userCoin = meta_data.get('userCoin')
    cid = meta_data.get('se').get('channel_id')
    
    if cid == None:
        sql = 'INSERT INTO `botCoin` (`qn`, `value`, `uuid`) VALUES ('+str(uid)+', '+str(meta_data.get('botSettings').get('defaultCoin'))+', "'+str(meta_data.get('uuid'))+'")'
    else:
        if sendFlag:
            go.send(meta_data, '请不要在频道里注册！')
        return False
    
    if userCoin == -1:
        go.commonx(sql)
        go.CrashReport(meta_data.get('uuid'), '注册用户'+str(uid), '好感度系统')
        if gid != None and sendFlag:
            go.send(meta_data, '[CQ:face,id=161] 注册成功！')
        tools.loadConfig(meta_data)
        return meta_data.get('botSettings').get('defaultCoin')
    else:
        go.send(meta_data, '猪比已经认识你了呢qwq')
        return userCoin
        
def addCoinFunc(meta_data):
    uid = meta_data.get('se').get('user_id')
    gid = meta_data.get('se').get('group_id')
    message = meta_data.get('message')
    
    if ' ' in message:
        message = message.split(' ')
        userid = message[0]
        num = message[1]
        
        if 'at' in userid:
            userid = go.getCQValue('qq', userid)
        
        userCoin = go.addCoin(meta_data, num)
    else:
        userid = message
        userCoin = go.addCoin(meta_data)
    go.CrashReport(meta_data.get('uuid'), userid, '加好感度')
    if userCoin == False:
        return go.send(meta_data, '用户未注册')
    go.send(meta_data, '[CQ:face,id=161] 成功给用户{0}添加{1}个好感度'.format(userid, userCoin))
