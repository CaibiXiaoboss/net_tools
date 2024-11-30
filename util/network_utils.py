def split_mac_address_and_port(input_string: str):
    """
    将包含MAC地址和端口信息的字符串拆分为两部分：MAC地址和端口路径
    :param input_string:输入字符串，格式如 "94:24:e1:82:8e:4d1/1/18
    :return:返回mac地址，端口号
    """
    index = input_string.rfind(':') + 3
    return input_string[:index], input_string[index:]
