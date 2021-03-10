
def 写入日志(msg):
    import logging
    kwargs = {
        "filename": "logs.txt",
        "format": "%(asctime)s - %(message)s"
    }
    logger = logging.getLogger()
    fh = logging.FileHandler("test.log",encoding="utf-8",mode="a")
    formatter = logging.Formatter("%(asctime)s - %(message)s")
    fh.setFormatter(formatter)
    logger.addHandler(fh)
    logger.setLevel(logging.DEBUG)
    logger.warning(msg)

if __name__ == '__main__':
    写入日志("hello李华盛")