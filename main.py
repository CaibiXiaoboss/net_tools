from olt_msg.ont_msg import ONTStatusMonitor
from ov2500_msg.ov2500_ctl import Ov2500Ctl
from zabbix_msg.msg_from_zbapi import ZabbixCtl
from util import logger_utils, wxpusher
from util import device_counter
from util.db_manager import DBManager


def main():
    # 实例化日志对象
    device_number_log = logger_utils.configure_logger('device_number', log_file='./device_number.log')
    device_counters = device_counter.DeviceCounter()
    ap_down_number = 0

    # 初始化数据库管理器
    db_manager = DBManager('device_number.db', 'device_number')

    # 获取上次记录的设备掉线数量，从txt文本里面获取
    last_ap_down_number = device_counters.get_ap_disconnect_count()
    last_switch_down_number = device_counters.get_switch_disconnect_count()
    last_new_onu_down_number = device_counters.get_new_onu_count()
    last_old_onu_down_number = device_counters.get_old_onu_count()

    # 初始化Zabbix、ONT和Ov2500实例
    zabbix = ZabbixCtl()
    ont = ONTStatusMonitor()
    ov2500 = Ov2500Ctl()

    # 获取Zabbix API响应，获取最新交换机掉线数量信息
    zabbix_all_response = zabbix.get_all_switch_number()
    zabbix_down_response = zabbix.send_zabbix_api_request()
    switch_down_number = len(zabbix_down_response['result'])
    all_switch_number = len(zabbix_all_response['result'])

    # 获取ONT状态
    ont.get_ont_status()

    # 登录Ov2500并获取AP状态,获取最新掉线ap的数量
    ov2500.login()
    host1_ap_msg, host2_ap_msg = ov2500.get_all_ap()
    ap_down_number = sum(1 for ap_info in host1_ap_msg + host2_ap_msg if ap_info['apStatus'] == 'Down')
    all_ap_number = len(host1_ap_msg) + len(host2_ap_msg)

    # 获取最新onu掉线数量
    old_ont_down_number = ont.get_old_ont_down_number()
    old_ont_up_number = ont.get_old_ont_up_number()
    old_ont_all_number = ont.get_old_ont_number()
    new_ont_down_number = ont.get_new_ont_down_number()
    new_ont_up_number = ont.get_new_ont_up_number()
    new_ont_all_number = ont.get_new_ont_number()

    # 把本次掉线个数记录日志里面
    logger_utils.log_info(device_number_log,
                          f'ap掉线个数:{ap_down_number}\t交换机掉线个数:{switch_down_number}\n'
                          f'旧校区onu在线个数{old_ont_up_number},onu掉线个数{old_ont_down_number}\n'
                          f'旧校区onu总数{old_ont_all_number}\n'
                          f'新校区onu在线个数{new_ont_up_number},onu掉线个数{new_ont_down_number}\n'
                          f'新校区onu总数{new_ont_all_number}'
                          )

    # 发送告警通知，新旧校区onu
    if old_ont_down_number > last_old_onu_down_number + 50:
        wxpusher.push_alarm_info('离线告警:旧校区ont离线数量比上一个时间段多50台',
                                 old_onu_down_number=old_ont_down_number,
                                 new_onu_down_number=new_ont_down_number,
                                 ap_down_number=ap_down_number,
                                 switch_down_number=switch_down_number)
    elif old_ont_down_number < last_old_onu_down_number - 50:
        wxpusher.push_alarm_info('恢复通知:旧校区ont离线数量比上一个时间段减少50台',
                                 old_onu_down_number=old_ont_down_number,
                                 new_onu_down_number=new_ont_down_number,
                                 ap_down_number=ap_down_number,
                                 switch_down_number=switch_down_number)
    if new_ont_down_number > last_new_onu_down_number + 50:
        wxpusher.push_alarm_info('离线告警:新校区ont离线数量比上一个时间段多50台',
                                 old_onu_down_number=old_ont_down_number,
                                 new_onu_down_number=new_ont_down_number,
                                 ap_down_number=ap_down_number,
                                 switch_down_number=switch_down_number)
    elif new_ont_down_number < last_new_onu_down_number - 50:
        wxpusher.push_alarm_info('恢复通知:新校区ont离线数量比上一个时间段减少50台',
                                 old_onu_down_number=old_ont_down_number,
                                 new_onu_down_number=new_ont_down_number,
                                 ap_down_number=ap_down_number,
                                 switch_down_number=switch_down_number)

    if switch_down_number >= last_switch_down_number + 1:
        str_list = []
        for msg in zabbix_down_response['result']:
            str_list.append(f'设备名：{msg["name"]}\n')
            str_list.append(f"""ip:{msg['snmp_error'].split('"')[1].split(':')[0]}\n""")
        wxpusher.push_alarm_info(f'离线告警:交换机离线数量比上一个时间段多1台或以上\n{"".join(str_list)}',
                                 old_onu_down_number=old_ont_down_number,
                                 new_onu_down_number=new_ont_down_number,
                                 ap_down_number=ap_down_number,
                                 switch_down_number=switch_down_number)
    elif switch_down_number <= last_switch_down_number - 1:
        wxpusher.push_alarm_info('恢复通知:交换机离线数量比上一个时间段减少1台或以上',
                                 old_onu_down_number=old_ont_down_number,
                                 new_onu_down_number=new_ont_down_number,
                                 ap_down_number=ap_down_number,
                                 switch_down_number=switch_down_number)

    if ap_down_number > last_ap_down_number + 50:
        wxpusher.push_alarm_info('离线告警:ap离线数量比上一个时间段多50台',
                                 old_onu_down_number=old_ont_down_number,
                                 new_onu_down_number=new_ont_down_number,
                                 ap_down_number=ap_down_number,
                                 switch_down_number=switch_down_number)
    elif ap_down_number < last_ap_down_number - 50:
        wxpusher.push_alarm_info('恢复通知:ap离线数量比上一个时间段减少50台',
                                 old_onu_down_number=old_ont_down_number,
                                 new_onu_down_number=new_ont_down_number,
                                 ap_down_number=ap_down_number,
                                 switch_down_number=switch_down_number)

    # 最后更新掉线数量到device_conunts.txt文本里面
    device_counters.record_ap_disconnect(ap_down_number)
    device_counters.record_switch_disconnect(switch_down_number)
    device_counters.record_old_onu_count(old_ont_down_number)
    device_counters.record_new_onu_count(new_ont_down_number)

    db_manager.insert_data(total_ap_devices=all_ap_number,total_switch_devices=all_switch_number,
                           total_old_ont_devices=old_ont_all_number,
                           total_new_ont_devices=new_ont_all_number,
                           ap_down_number=ap_down_number,
                           switch_down_number=switch_down_number,
                           old_ont_down_number=old_ont_down_number,
                          new_ont_down_number=new_ont_down_number
)

    '''wxpusher.push_alarm_info("测试",
                             old_onu_down_number=old_ont_down_number,
                             new_onu_down_number=new_ont_down_number,
                             ap_down_number=ap_down_number,
                             switch_down_number=switch_down_number)'''


# 按间距中的绿色按钮以运行脚本。
if __name__ == '__main__':
    main()
