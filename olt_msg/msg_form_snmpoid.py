import sys
import util.logger_utils
from logging import Logger
from pysnmp.hlapi import *


def snmp_walk(host, oid, logger: Logger):
    """
    实现snmp_walk的功能
    :param logger: 日志对象
    :param host: 主机名
    :param oid: oid基地址
    :return: 一个有oid和值的列表,列表里每个元素都是一个字典
    """
    results = []
    for (errorIndication, errorStatus, errorIndex, varBinds) in nextCmd(SnmpEngine(),
                                                                        CommunityData('public'),
                                                                        UdpTransportTarget((host, 161), timeout=5,
                                                                                           retries=2),
                                                                        ContextData(),
                                                                        ObjectType(ObjectIdentity(oid)),
                                                                        lexicographicMode=False,
                                                                        ):
        if errorIndication:
            util.logger_utils.log_info(logger, str(errorIndication))
            break
        elif errorStatus:
            util.logger_utils.log_info(logger, str('%s at %s' % (errorStatus.prettyPrint(),
                                                                 errorIndex and varBinds[int(errorIndex) - 1][
                                                                     0] or '?')))
            break
        else:
            for varBind in varBinds:
                oid, value = varBind
                results.append({'OID': oid.prettyPrint(), 'Value': value.prettyPrint()})
    return results

