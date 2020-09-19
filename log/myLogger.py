import logging


def initLogging(f, ex):
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s-%(levelname)s-%(message)s',
        datefmt='%y-%m-%d %H:%M',
        filename=f,
        filemode='a')
    # 文件处理器
    fh = logging.FileHandler(f, encoding='utf-8')
    # 添加处理器
    logging.getLogger().addHandler(fh)
    # 返回log实体
    log = logging.exception(ex)
    return log

