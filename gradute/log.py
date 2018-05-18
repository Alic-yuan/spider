import logging



class Logger(object):
    def __init__(self, path, clevel=logging.DEBUG, Flevel=logging.DEBUG):
        self.logger = logging.getLogger(path)
        self.logger.setLevel(logging.DEBUG)
        fmt = logging.Formatter('\033[0;30m' + '[%(asctime)s] [%(levelname)s] %(message)s', '%Y-%m-%d %H:%M:%S')
        # 设置CMD日志
        sh = logging.StreamHandler()
        sh.setFormatter(fmt)
        sh.setLevel(clevel)
        # 设置文件日志
        fh = logging.FileHandler(path)
        fh.setFormatter(fmt)
        fh.setLevel(Flevel)
        self.logger.addHandler(sh)
        self.logger.addHandler(fh)

    def debug(self, message):
        self.logger.debug(message)

    def info(self, message):
        self.logger.info(message)

    def war(self, message):
        self.logger.warn('\033[1;32m' + message)

    def error(self, message):
        self.logger.error('\033[1;31m' + message)

    def cri(self, message):
        self.logger.critical('\033[1;31m' + message)

if __name__ =='__main__':
     logyyx = Logger('yyx.log',logging.DEBUG,logging.DEBUG)
     logyyx.debug('一个debug信息')
     logyyx.info('一个info信息')
     logyyx.war('一个warning信息')
     logyyx.error('一个error信息')
     logyyx.cri('一个致命critical信息')
     # print('\033[1;32m' + 'green' + '\033[0m')