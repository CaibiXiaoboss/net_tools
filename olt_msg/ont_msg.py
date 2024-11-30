from util import logger_utils, yaml_io
from olt_msg import msg_form_snmpoid


def _decode_ont_index(ont_index: str):
    # 根据公式逆运算解码 ont_index
    ont_index_num = int(ont_index)
    base = ont_index_num - 29360128
    lt_slot = (base // 33554432) - 1
    pon = ((base % 33554432) // 65536) + 1
    ont = ((base % 33554432) % 65536 // 512) + 1
    return f'{lt_slot}/{pon}/{ont}'


class ONTStatusMonitor:
    def __init__(self, config_file='./config.yaml',
                 logger=logger_utils.configure_logger('ont_status', log_file='./app.log'),
                 old_devices_list=None, new_devices_list=None):
        """
        类构造方法
        :type status_list: 一个存放状态信息的列表,存放已经进行端口转换的信息
        :param config_file: 配置文件路径,默认运行程序同级目录的config.yaml
        :param logger: 保存日志文件的路径,默认同级目录的app.log
        """
        if old_devices_list is None:
            self._old_status_list = []
        if new_devices_list is None:
            self._new_status_list = []
        self._config_file = config_file
        self._logger = logger
        self._old_ip = yaml_io.read_yaml(config_file)['olt_info']['old_ip']
        self._new_ip = yaml_io.read_yaml(config_file)['olt_info']['new_ip']
        self._snmp_oid = yaml_io.read_yaml(config_file)['olt_info']['snmp_oid']
        self._onu_status = {
            'old_ont_up': 0,
            'old_ont_down': 0,
            'new_ont_up': 0,
            'new_ont_down': 0
        }

    def get_ont_status(self):
        """
        根据snmpoid获取ont的状态,并可以根据返回的值换算出端口号
        :return:返回状态列表,列表里的元素是一个个ont的字典,key为端口号,value是状态
        """
        old_ont_status_list = msg_form_snmpoid.snmp_walk(self._old_ip, self._snmp_oid, self._logger)
        new_ont_status_list = msg_form_snmpoid.snmp_walk(self._new_ip, self._snmp_oid, self._logger)
        if len(old_ont_status_list) != 0:
            logger_utils.log_info(self._logger, '成功获取旧校区onu信息')
        if len(new_ont_status_list) != 0:
            logger_utils.log_info(self._logger, '成功获取新校区onu信息')
        for ont_status in old_ont_status_list:
            key = _decode_ont_index(ont_status['OID'].split('.')[10])
            value = ont_status['Value']
            self._old_status_list.append({f'1/1/{key}': value})
            if ont_status['Value'] == '1':
                self._onu_status['old_ont_up'] += 1
            else:
                self._onu_status['old_ont_down'] += 1
        for ont_status in new_ont_status_list:
            key = _decode_ont_index(ont_status['OID'].split('.')[10])
            value = ont_status['Value']
            self._new_status_list.append({f'1/1/{key}': value})
            if ont_status['Value'] == '1':
                self._onu_status['new_ont_up'] += 1
            else:
                self._onu_status['new_ont_down'] += 1
        return [self._old_status_list, self._new_status_list]

    def get_old_ont_up_number(self):
        """
        返回旧校区onu在线个数
        :return: self._old_ont_down
        """
        if self._onu_status['old_ont_up'] != 0:
            return self._onu_status['old_ont_up']

    def get_old_ont_down_number(self):
        """
        返回旧校区onu离线个数
        :return: self._old_ont_down
        """
        if self._onu_status['old_ont_down'] != 0:
            return self._onu_status['old_ont_down']
        
    def get_new_ont_up_number(self):
        """
        返回新校区onu在线个数
        :return: self._old_ont_down
        """
        if self._onu_status['new_ont_up'] != 0:
            return self._onu_status['new_ont_up']

    def get_new_ont_down_number(self):
        """
        返回新校区onu离线个数
        :return: self._old_ont_down
        """
        if self._onu_status['new_ont_down'] != 0:
            return self._onu_status['new_ont_down']

    def get_old_ont_number(self):
        """
        返回旧校区onu总个数
        :return: self._old_ont_down
        """
        if (self._onu_status['old_ont_up'] and self._onu_status['old_ont_down']) != 0:
            return self._onu_status['old_ont_up'] + self._onu_status['old_ont_down']
        
    def get_new_ont_number(self):
        """
        返回新校区onu总个数
        :return: self._old_ont_down
        """
        if (self._onu_status['new_ont_up'] and self._onu_status['new_ont_down']) != 0:
            return self._onu_status['new_ont_up'] + self._onu_status['new_ont_down']
