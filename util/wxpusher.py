import requests
import json
from util import yaml_io, logger_utils


def wxpusher_send_msg(msg: str, title: str):
    """
    :param msg: 要发送的消息
    :param title: 标题
    :return: 返回推送状态信息
    """
    data = {
        "appToken": yaml_io.read_yaml('config.yaml')['app_token'],
        "content": msg,
        "title": title,
        "uids": yaml_io.read_yaml('config.yaml')['uid'],  # 如果是群发，这里可以是多个uid组成的列表
        "url": '',  # 可选，点击消息后跳转的链接
    }
    # 发送POST请求
    response = requests.post('https://wxpusher.zjiecode.com/api/send/message', data=json.dumps(data),
                             headers={'Content-Type': 'application/json'})

    # 检查响应状态
    if response.status_code == 200:
        response_json = response.json()
        if response_json['code'] == 200 or response_json['code'] == 1000:
            return "消息发送成功"
        else:
            return f"消息发送失败，错误码：{response_json['code']}, 错误信息：{response_json['msg']}"
    else:
        return f"HTTP请求失败，状态码：{response.status_code}"


def push_alarm_info(main_info, old_onu_down_number, new_onu_down_number, ap_down_number, switch_down_number):
    """
    推送告警消息,把离线的数量统计出来推送到微信上面,调用wxpusher_send_msg()方法
    :param main_info: 主要告警信息
    :param onu_down_number: onu离线数量
    :param ap_down_number: ap离线数量
    :param switch_down_number: 交换机离线数量
    :return:
    """
    logger = logger_utils.configure_logger('push_alarm_info', log_file='./app.log')
    alarm_info = f"""<h1>主要故障</h1>
                    <h2>告警内容：\n{main_info}<h2>
                    <h2>ap离线个数：{ap_down_number}</h2>
                    <h2>交换机离线个数：{switch_down_number}</h2>
                    <h2>旧校区onu离线个数：{old_onu_down_number}</h2>
                    <h2>新校区onu离线个数：{new_onu_down_number}</h2>"""
    return_msg = wxpusher_send_msg(alarm_info, alarm_info)
    logger_utils.log_info(logger, return_msg)
