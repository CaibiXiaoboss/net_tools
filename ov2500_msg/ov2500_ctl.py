from requests import Session
from util import yaml_io
from ov2500_msg import msg_from_api
from util import logger_utils


class Ov2500Ctl:
    def __init__(self, config_file='./config.yaml',
                 logger=logger_utils.configure_logger('ov2500_ctl', log_file='./app.log')):
        """
        根据传入的配置文件名,读取后进行登录以及获取消息等动作
        :param config_file: 配置文件路径,默认为当前目录下的config.yaml文件
        :param logger: 日志文件路径对象,默认为当前目录下的app.log文件
        """
        self._logger = logger
        self._config_file = config_file
        self._session = Session()
        self._request = yaml_io.read_yaml(f'{config_file}')['ov2500_requests']

    def login(self):
        """
        ov2500_login的上层方法,给main调用,提供log打印功能和读取yaml配置功能
        :return:None
        """
        login_msg = []
        host1_url = self._request['login_url'].format(server_ip=self._request['server_ip'][0])
        host2_url = self._request['login_url'].format(server_ip=self._request['server_ip'][1])
        msg_from_api.ov2500_login(self._session,
                                  host1_url,
                                  self._request['user'],
                                  self._request['pwd'],
                                  login_msg)
        msg_from_api.ov2500_login(self._session,
                                  host2_url,
                                  self._request['user'],
                                  self._request['pwd'],
                                  login_msg)
        if len(login_msg) > 1:
            logger_utils.log_info(self._logger, ",".join(login_msg))

    def get_all_ap(self):
        """
        筛选返回的字典里的data键里面的值:
        data的结构是一个list,里面每个元素都是一个dict
        get_ap_list的上层方法,给main调用,提供log打印
        :return: 返回两个有ap字典里的data键里面的list,list里面有dict
        """
        status_msg = []
        host1_url = self._request['getAPList_url'].format(server_ip=self._request['server_ip'][0])
        host2_url = self._request['getAPList_url'].format(server_ip=self._request['server_ip'][1])
        host1_ap_msg = msg_from_api.get_ap_msg(self._session, host1_url, status_msg)
        host2_ap_msg = msg_from_api.get_ap_msg(self._session, host2_url, status_msg)
        if len(status_msg) > 1:
            logger_utils.log_info(self._logger, ",".join(status_msg))
        return host1_ap_msg['data'], host2_ap_msg['data']
