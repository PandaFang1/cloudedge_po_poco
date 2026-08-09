import logging

logger = logging.getLogger("Cloudedge") #创建logger实例

logger.setLevel(logging.DEBUG) #设置日志默认级别

#设置流处理器，输出在控制台的日志
ch = logging.StreamHandler() #创建流处理器的实例
ch.setLevel(logging.INFO) #设置流处理展示的日志级别

#设置文件处理器，把日志保存在在文件中
file = logging.FileHandler("Execution.log") #创建文件处理器的实例
file.setLevel(logging.DEBUG) #设置文件处理展示的日志级别

#设置日志打印格式
formatter = logging.Formatter('%(asctime)s-%(name)s-%(levelname)s-%(message)s')

#处理器添加格式配置
ch.setFormatter(formatter)
file.setFormatter(formatter)

#添加日志配置
logger.addHandler(ch)
logger.addHandler(file)

