import sqlite3
import datetime
import logging
from util import logger_utils

class DBManager:
    def __init__(self, db_name, table_name):
        """
        初始化数据库管理器。
        参数:
        db_name (str): 数据库文件名
        self.conn (sqlite3.Connection): 数据库连接对象
        self.cursor (sqlite3.Cursor): 数据库游标对象
        self.logger (logging.Logger): 日志记录器对象
        """
        self.db_name = db_name
        self.table_name = table_name
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.logger = logger_utils.configure_logger('db_manager',log_file='./db_manager.log')
        self.create_table()
        # self.insert_data()
        self.logger.info("数据库管理器初始化完成")

    def create_table(self):
        """创建数据库表"""
        create_table_sql = f"""
        CREATE TABLE IF NOT EXISTS {self.table_name} (
            id INTEGER PRIMARY KEY,
            timestamp TEXT NOT NULL,
            total_ap_devices INTEGER,
            total_old_ont_devices INTEGER,
            total_new_ont_devices INTEGER,
            total_switch_devices INTEGER,
            ap_down_number INTEGER,
            switch_down_number INTEGER,
            old_ont_down_number INTEGER,
            new_ont_down_number INTEGER
        )
        """
        self.cursor.execute(create_table_sql)
        self.conn.commit()
        self.logger.info(f"创建表 {self.table_name} 成功")


    
    def insert_data(self, total_ap_devices, total_old_ont_devices, total_new_ont_devices, total_switch_devices, ap_down_number, switch_down_number, old_ont_down_number, new_ont_down_number):
        """插入设备掉线数据"""
        timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        insert_sql = f"""
        INSERT INTO {self.table_name} (timestamp, total_ap_devices, total_old_ont_devices, total_new_ont_devices, total_switch_devices, ap_down_number, switch_down_number, old_ont_down_number, new_ont_down_number)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        self.cursor.execute(insert_sql, (timestamp, total_ap_devices, total_old_ont_devices, total_new_ont_devices, total_switch_devices, ap_down_number, switch_down_number, old_ont_down_number, new_ont_down_number))
        self.conn.commit()
        self.logger.info("插入设备掉线数据成功")


    def get_last_record(self):
        """获取最新的设备掉线数据记录"""
        select_sql = f"""
        SELECT * FROM {self.table_name} ORDER BY id DESC LIMIT 1
        """
        self.cursor.execute(select_sql)
        row = self.cursor.fetchone()
        if row:
            return {
                'timestamp': row[1],
                'total_ap_devices': row[2],
                'total_old_ont_devices': row[3],
                'total_new_ont_devices': row[4],
                'total_switch_devices': row[5],
                'ap_down_number': row[6],
                'switch_down_number': row[7],
                'old_ont_down_number': row[8],
                'new_ont_down_number': row[9]
            }
        else:
            return None

