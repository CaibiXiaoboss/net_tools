from util import logger_utils, yaml_io
import requests
import json


class ZabbixCtl:
    def __init__(self, logger=logger_utils.configure_logger('zabbix_ctl', log_file='./app.log')):
        self._url = yaml_io.read_yaml('./config.yaml')['zabbix_request']['url']
        self._headers = yaml_io.read_yaml('./config.yaml')['zabbix_request']['header']
        self._logger = logger
        self._data = yaml_io.read_yaml('./config.yaml')['zabbix_request']['request_json']

    def send_zabbix_api_request(self, json_data=None):
        """
        调用zabbix接口，筛选有snmp警告的主机信息返回
        :return: 返回一个respone响应,json格式
        """
        if json_data is None:
            json_data = self._data
        # 发送POST请求
        response = requests.post(self._url, json=json_data, headers=self._headers)

        # 检查请求是否成功
        if response.status_code == 200:
            try:
                response_json = response.json()
                logger_utils.log_info(self._logger, 'zabbix请求成功,已筛选有警告的设备')
                return response_json
            except json.JSONDecodeError:
                logger_utils.log_info(self._logger, '返回的数据非json格式')
        else:
            logger_utils.log_error(self._logger, f"请求失败，状态码：{response.status_code}, 原因：{response.text}")

    def get_all_switch_number(self):
        """
        获取所有交换机
        :return: 交换机列表
        """
        # 读取配置文件
        config = yaml_io.read_yaml('./config.yaml')
        
        # 修改 filter 参数为空字典
        config['zabbix_request']['request_json']['params']['filter'] = {}
        
        # 生成新的 JSON 请求体
        new_request_json = config['zabbix_request']['request_json']
        
        # 发送请求
        response = self.send_zabbix_api_request(json_data=new_request_json)
        return response
        
        

