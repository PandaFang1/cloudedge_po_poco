import os
# from collections import Counter
# from dataclasses import field
# from itertools import count

import yaml
# from Xlib.Xcursorfont import pirate
# from selenium.webdriver.common.devtools.v136.cache_storage import request_entries

from utils.log_utils import logger


class ConfigError(Exception):
    """
    继承异常的基类
    """
    def __init__(self):
        pass

class ConfigManager:
    """统一管理配置"""
    def __init__(self,config_dir):
        self.config_dir = config_dir #初始化文件路径
        #类属性
        self.platform_lists = ["android", "ios"]
        self.keyword_lists = ["platform","uuid","app_package","wda_port"]

    def _read_yaml_file(self,filepath):
        """
        读取yaml文件
        :param filepath:
        :return:
        """
        try:
            file_path = os.path.join(self.config_dir,filepath)#拼接文件路径和文件名字
            with open(file_path,"r",encoding="utf-8") as f: #以只读的方式读取文件
                return yaml.safe_load(f) #返回读取的数据
        except FileNotFoundError as e:
            logger.error(f"文件不存在:{e}")
            return None
        except PermissionError as e:
            logger.error(f"文件权限问题：{e}")
            return None
        except UnicodeError as e:
            logger.error(f"文件编码错误：{e}")
            return None
        except yaml.YAMLError as e:
            logger.error(f"yaml文件内容不规范：{e}")
            return None
        except Exception as e:
            logger.error(f"其他错误:{e}")
            return None

    def _get_single_dev_key(self,device,filepath):
        """
        获取yaml文件中的所有设备的键值
        :param device:
        :param filepath:
        :return:
        """
        key_value_lists = []
        for k in device.keys():
            key_value_lists.append(k)
        logger.info(f"获取到{filepath}文件中{device}的键列表")
        return key_value_lists,"返回键列表"


    def _value_type_check(self,value,except_type,filepath):
        """
        yaml文件中的字段类型校验
        :param data:
        :return:
        """
        if not isinstance(value,except_type):
            raise ConfigError(
                f"文件{filepath}中的值不是预期的数据类型{except_type}",
                f"实际类型是{type(value)}"
            )

    def _value_platform_check(self,value,expect_platform,filepath):
        """
        判断platform是否正确
        :param value:
        :param expect_platform:
        :param filepath:
        :return:
        """

        if value.lowwer() not in self.platform_lists:
            raise ConfigError(
                f"文件{filepath}中的平台类型不是预期的数据类型{expect_platform}",
                f"实际数据是{value}"
            )

    def _keyword_check(self,filepath):
        """
        yaml文件中的关键字段检查：platform,uuid,app_package,wda_port
        :param value:
        :param except_keyword:
        :return:
        """
        existing_keys = list(data.keys()) #获取原始文件中的键，转换为列表
        allowed_key_list  = self.keyword_lists#获取必须要求的键
        #检查是否缺少键，missing_keyword返回的是列表，即使没有返回的也是列表
        missing_keyword = [k for k in allowed_key_list if k not in existing_keys]
        if missing_keyword:
            raise ConfigError(
                f"{filepath}中缺少关键属性{missing_keyword}",
                f"当前存在的属性是{existing_keys}",
                f"必要的属性是{allowed_key_list}"
            )

    def _device_port_check(self,device,filepath):
        """
        安卓手机无需配置端口号，ios多台需要配置端口号
        :param device:
        :param filepath:
        :return:
        """
        if device["platform"].lowwer() != "ios":
            if "wda_port" in device:
                ConfigError(
                    f'{filepath}文件中的{device["udid"]}的设备包含端口号',
                    f"安卓手机无需配置端口号"
                )
        if device["platform"].lowwer() == "ios":
            if "wda_port" not in device:
                ConfigError(
                    f'{filepath}文件中的{device["udid"]}的设备未包含端口号',
                    f"IOS手机需要配置端口号"
                )

    def _get_ios_port(self,devices,filepath):
        """
        检查IOS端口是否配置合理，包含重复性校验，范围检测
        :param devices:
        :param filepath:
        :return:
        """
        for device in devices:
            if devices["platform"].lowwer() == "ios":
                pass


    def get_all_devices(self):
        """
        获取手机的所有相关信息
        :return:
        """
        try:
            return self._read_yaml_file("config.yaml")["devices"]
        except Exception as e:
            logger.error(f"读取config.yaml文件出现异常：{e}")
            return None

    def get_mobile_platform(self):
        """
        获取设备列表长度以及
        :return:
        """
        if self.get_all_devices():
            devices_num = len(self.get_all_devices())
            for i in range(0,devices_num):
                mobile_platform = self.get_all_devices()[i]["platform"]
                if self.get_all_devices()[i]["platform"]:
                    if mobile_platform == "Android"or"android":
                        print(f'安卓机{self.get_all_devices()[i]["phone_model"]}')
                    else:
                        print(f'ios{self.get_all_devices()[i]["phone_model"]}')
                else:
                    print("配置列表无手机型号")


    def read_devices(self):
        if self._read_yaml_file("config.yaml"):
            print(self._read_yaml_file("config.yaml")["devices"])
        else:
            print("无数据")

config = ConfigManager("./")
data = config.get_all_devices()
print(data)
data_1 = {'user_name': '肥猪阿熊', 'phone_model': 'Redmi Note 11 5G', 'platform': 'Android', 'udid': 'TC55LJMR59W8ZPRK', 'app_package': 'com.cloudedge.smarteye'}
if "udid" in data_1:
    print(f"'udid'在字典里")
# config.get_mobile_platform()
# data = {'user_name': '肥猪阿熊', 'phone_model': 'Redmi Note 11 5G', 'platform': 'Android', 'udid': 'TC55LJMR59W8ZPRK', 'app_package': 'com.cloudedge.smarteye'}
# for k,v in data.items():
#     print("键：",k)
#     print("值：",v)