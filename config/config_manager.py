import os
import yaml
from utils.log_utils import logger


class ConfigManager:
    """统一管理配置"""
    def __init__(self,config_dir):
        self.config_dir = config_dir #初始化文件路径

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

    def _value_check(self,filepath):
        """
        yaml文件内容校验，必须包含user_name,phone_model,platform,udid;
        ios如果有多台还需要有wda_port 
        :param data:
        :return:
        """
        try:
            data = self._read_yaml_file(filepath)
            if data:
        except Exception as e:
            logger.error(f"文件校验遇到其他问题：{e}")
            return False


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
                        print(f"安卓机{self.get_all_devices()[i]["phone_model"]}")
                    else:
                        print(f"ios{self.get_all_devices()[i]["phone_model"]}")
                else:
                    print("配置列表无手机型号")


    def read_devices(self):
        if self._read_yaml_file("config.yaml"):
            print(self._read_yaml_file("config.yaml")["devices"])
        else:
            print("无数据")

config = ConfigManager("./")
# config.read_devices()
config.get_mobile_platform()