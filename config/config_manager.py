import os
from typing import AnyStr

import yaml
from utils.log_utils import logger


class ConfigError(Exception):
    """
    继承异常的基类
    """
    pass

class ConfigManager:
    """统一管理配置"""

    #类属性--平台列表
    platform_lists = ["android", "ios"]

    # 类属性--关键字段
    keywords_lists = ["platform", "uuid", "app_package"]

    #类属性--字段的数据类型
    COMMON_FIELD_TYPES = {
        "user_name" : str,
        "phone_model" : str,
        "platform" : str,
        "udid": str,
        "app_package" : str,
    }
    #类属性--IOS特有字段
    IOS_FIELD_TYPES = {
        "wda_port" : int
    }

    def __init__(self,config_dir):
        self.config_dir = config_dir #初始化文件路径

    def _read_yaml_file(self,filepath):
        """
        读取文件
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

    @staticmethod
    def _keyword_check(existing_dic:dict[str:AnyStr],allowed_key_list:list[AnyStr],filepath):
        """
        yaml文件中的关键字段检查：platform,uuid,app_package:
        """
        existing_key_list =[k for k in existing_dic.keys()] # 获取原始文件中的键，转换为列表
        # 检查是否缺少键，missing_keyword返回的是列表，即使没有返回的也是列表
        missing_keyword = [k for k in allowed_key_list if k not in existing_key_list]
        if missing_keyword:
            raise ConfigError(
                f"{filepath}中缺少关键属性{missing_keyword}",
                f"当前存在的属性是{existing_key_list}",
                f"必要的属性是{allowed_key_list}"
            )

    @staticmethod
    def _value_type_check(value,except_type,filepath):
        """
        yaml文件中的数据类型校验
        """
        if not isinstance(value,except_type):
            raise ConfigError(
                f"文件{filepath}中的值{value}不是预期的数据类型{except_type}",
                f"实际类型是{type(value)}"
            )

    @staticmethod
    def _value_check(value,expect_value,filepath):
        """
        yaml文件中关键字段的值校验
        """
        if value.lower() not in expect_value:
            raise ConfigError(
                f"文件{filepath}中的{value}不是预期的值{expect_value}"
            )

    @staticmethod
    def _validate_dictvalue_dependency(existing_dict,dependent_field,dependency_field,allowed_combinations,filepath):
        """
        exiting_dict:当前被校验的字典---{platform:ios/android,
                                        wda_port:8001}
        dependent_field：依赖者----wda_port
        dependency_field:被依赖者---paltorm
        allowed_combinations：两者的关系{ios:[wda_port]
                                       android:[]     }
        """
        depd_value = existing_dict[dependency_field] #获取被依赖者,如果无被依赖者则返回为None
        if not depd_value:
            raise ConfigError(
                f"文件{filepath}中缺少被依赖者{dependency_field}"
            )
        #判断depd_value是否在allowed_combinations中，保持一致性会先对两种数据进行小写处理
        allowed_combinations_lower_list =[k for k in allowed_combinations]
        if depd_value.lower() not in allowed_combinations_lower_list:
            raise ConfigError(
                f"文件{filepath}中被依赖者{dependency_field}的值不在依赖关系中"
            )

        #判断depd_value的具体的值，再根据allowed_combinations的值来做处理
        allowed_value = allowed_combinations[depd_value] #获取键depd_value在allowed_combinations的值
        if dependent_field in allowed_combinations:#判断依赖者是否在两者关系中的，存在继续对值做判断，不存在则抛出异常
            #allowed_value值做判断，空，和依赖者一致，和依赖者不一致
            if not allowed_value: #如果为空，则输出无需依赖者
                raise ConfigError(
                    f"文件{filepath}中的依赖者{dependent_field}不需要此依赖"
                )
        else:
            raise ConfigError(
                f"文件{filepath}中两者关系中未包含依赖者{dependent_field}"
            )

    @staticmethod
    def _value_range_check(value,expect_range,filepath):
        """
        对值的范围进行校验
        """
        if value not in expect_range:
            raise ConfigError(
                f"文件{filepath}中的{value}不在设定的范围内，设定的范围是{expect_range}"
            )

    @staticmethod
    def _value_repeatability_check(existing_lists,dependent_field,dependency_field,filepath):
        """
        existing_lists：列表嵌套字典形式
        dependency_field:需要检验的字段
        dependent_field:对值的重复性进行校验，找出相同的值，并找出他们在字典中的唯一关键字
        """
        exist_combinations = {} #用于记录整个列表嵌套字典中的唯一值和需要检测重复的值
        for existing_dic in existing_lists: #遍历列表
            if dependency_field not in existing_dic: #判断是否有这个字段在字典中
                continue #如果不存在则结束此次循环
            #判断这个键的值是否在已存在的
            





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


data = {
        "App":[1,2],
        "Package": []
    }
if "App" in data:
    print("t")