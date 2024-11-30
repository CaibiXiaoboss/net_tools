import os


class DeviceCounter():
    """
    DeviceCounter类用于统计设备数量。
    
    该类通过读取一个文本文件来获取设备数量的信息。文件路径在初始化时指定。
    """

    def __init__(self, file_path='device_counts.txt'):
        """
        初始化DeviceCounter类的实例。
        
        参数:
        file_path (str): 设备数量信息文件的路径，默认为'device_counts.txt'。
        """
        self.file_path = file_path

    def record_ap_disconnect(self, count: int) -> None:
        """记录AP断开的数量

        Args:
            count (int): AP断开的数量
        """
        self._record('AP_down Count', count)

    def record_switch_disconnect(self, count: int) -> None:
        """记录交换机断开的数量

        Args:
            count (int): 交换机断开的数量
        """
        self._record('Switch Count', count)

    def record_old_onu_count(self, count: int) -> None:
        """记录旧校区ONU掉线的数量

        Args:
            count (int): ONU掉线的数量
        """
        self._record('ONU_old_down Count', count)

    def record_new_onu_count(self, count: int) -> None:
        """记录新校区ONU掉线的数量

        Args:
            count (int): ONU掉线的数量
        """
        self._record('ONU_new_down Count', count)

    def _record(self, device_type, count: int) -> None:
        # 读取现有记录
        records = self._read_records()

        # 更新或添加新的记录
        records[device_type] = count

        # 写回文件
        self._write_records(records)

    def _read_records(self) -> dict:
        records = {
            'AP_down Count': 0,
            'Switch Count': 0,
            'ONU_old_down Count': 0,
            'ONU_new_down Count': 0
        }
        if os.path.exists(self.file_path):
            with open(self.file_path, 'r') as file:
                for line in file:
                    parts = line.strip().split(': ')
                    if len(parts) == 2 and parts[0] in records:
                        records[parts[0]] = int(parts[1])
        return records

    def _write_records(self, records: dict) -> None:
        with open(self.file_path, 'w') as file:
            for device_type, count in records.items():
                file.write(f"{device_type}: {count}\n")

    def get_ap_disconnect_count(self) -> int:
        """获取AP断开的数量

        Returns:
            int: AP断开的数量
        """
        return self._get_count('AP_down Count')

    def get_switch_disconnect_count(self) -> int:
        """获取交换机断开的数量

        Returns:
            int: 交换机断开的数量
        """
        return self._get_count('Switch Count')

    def get_new_onu_count(self) -> int:
        """获取新校区ONU掉线的数量

        Returns:
            int: ONU掉线的数量
        """
        return self._get_count('ONU_new_down Count')

    def get_old_onu_count(self) -> int:
        """获取旧校区ONU掉线的数量

        Returns:
            int: ONU掉线的数量
        """
        return self._get_count('ONU_old_down Count')

    def _get_count(self, device_type) -> int:
        # 读取现有记录
        records = self._read_records()
        return records.get(device_type, 0)
