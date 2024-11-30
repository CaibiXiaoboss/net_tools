import json
import requests
import urllib3


def ov2500_login(session: requests.Session, url: str, user: str, pwd: str, global_msg: list):
    """
    传入一个会话，调用会话进行登录的方法
    :param session: 传入的会话对象
    :param url: api链接
    :param user: 用户名
    :param pwd: 密码
    :param global_msg: 全局信息列表
    :return: 返回相应的response对象
    """
    urllib3.disable_warnings()
    payload = {
        "userName": user,
        "password": pwd
    }

    # 将JSON数据转换为字符串
    data = json.dumps(payload)

    # 设置headers，通常POST JSON数据需要设置Content-Type为application/json
    headers = {
        'Content-Type': 'application/json'
    }

    # 发送POST请求
    response = session.post(url, data=data, headers=headers, verify=False)

    # 检查响应状态码和内容
    if response.status_code == 200:
        global_msg.append("ov2500登录成功")
        # 如果需要，可以进一步处理返回的数据
        # response_json = response.json()
        # print(response_json)
    else:
        global_msg.append(f"登录失败，HTTP状态码：{response.status_code}")

    return response


def get_notifications(session: requests.Session, url: str, payload: dict, global_msg: list):
    """
    在传入的会话里获取告警消息
    :param session: 保存的会话
    :param url: api
    :param payload: 参数
    :param global_msg: 全局消息列表
    :return: 返回一个消息数组，存放response返回的消息
    """
    urllib3.disable_warnings()
    headers = {'Content-Type': 'application/json'}  # 假设API需要JSON格式的内容类型头
    response = session.post(url, data=json.dumps(payload), headers=headers, verify=False)
    if response.status_code == 200:
        if response.status_code == 200:
            global_msg.append('查看消息方法调用成功')
            response_data = response.json()
        # 对response_data进行进一步处理...
            return response_data
    else:
        global_msg.append(f"请求失败，状态码：{response.status_code}")


def get_ap_msg(session: requests.Session, url: str, global_msg: list) -> dict:
    """
    获取会话中的所有ap信息
    :param url: api地址
    :param session: 会话
    :param global_msg: 消息列表
    :return: 返回ap_list列表
    """
    response = session.get(url,verify=False)
    if response.status_code == 200:
        ap_dict = response.json()
        global_msg.append('AP信息获取成功')
        return ap_dict
    else:
        global_msg.append(f'GET请求失败，状态码：{response.status_code}')

