import logging
import sys
from loguru import logger

is_init = False

if not is_init :
  
    is_init = True
    
    # --------------------------
    # 第一步：禁用标准logging输出
    # --------------------------
    def disable_standard_logging():
        # 1. 清除root logger的所有处理器（包括默认的控制台输出）
        root_logger = logging.getLogger()
        root_logger.handlers = []
        
        # 2. 遍历所有已存在的logger，清除处理器并禁用传播
        for logger_name in logging.root.manager.loggerDict:
            logger = logging.getLogger(logger_name)
            logger.handlers = []  # 移除该logger的所有处理器
            logger.propagate = False  # 禁止日志向上传播到root
        
        # 3. 禁用logging的默认配置（防止后续自动添加处理器）
        logging.basicConfig(handlers=[], level=logging.CRITICAL + 1)

    # 立即执行禁用操作（必须在其他库初始化前执行）
    disable_standard_logging()

    # --------------------------
    # 第二步：配置Loguru（含文件输出）
    # --------------------------
    # 移除Loguru默认输出（可选，按需保留）
    logger.remove()

    # 1. 控制台输出配置
    logger.add(
        sink=sys.stdout,
        format="{time:YYYY-MM-DD HH:mm:ss.SSS} | {level:<8} | {message}",
        level="INFO"
    )

    # 2. 主日志文件（按大小轮转）
    logger.add(
        sink="logs/app.log",
        format="{time:YYYY-MM-DD HH:mm:ss.SSS} | {level:<8} | {module}:{line} | {message}",
        level="DEBUG",
        rotation="500 MB",
        retention="7 days",
        compression="zip",
        encoding="utf-8"
    )

    # 3. 错误日志单独记录
    logger.add(
        sink="logs/error.log",
        format="{time:YYYY-MM-DD HH:mm:ss.SSS} | {level:<8} | {module}:{line} | {message}",
        level="ERROR",
        rotation="1 day",
        retention="30 days",
        compression="gz",
        encoding="utf-8"
    )

    # --------------------------
    # 第三步：捕获标准输出（如HTTP请求日志）
    # --------------------------
    # 保存原始stdout/stderr
    original_stdout = sys.stdout
    original_stderr = sys.stderr

    # 状态码正则匹配（用于动态级别）
    # STATUS_CODE_PATTERN = re.compile(r'" \d{3} ')

    class StdoutToLoguru:
        def write(self, message):
            # 转发到Loguru的INFO级别
            logger.info(f"{message.strip()}")
        
        def flush(self):
            # 兼容标准输出的flush方法（必须实现）
            pass

    # 重定向stdout/stderr到Loguru
    sys.stdout = StdoutToLoguru()
    sys.stderr = StdoutToLoguru()

    # 程序退出时恢复原始输出
    import atexit
    atexit.register(lambda: setattr(sys, "stdout", original_stdout))
    atexit.register(lambda: setattr(sys, "stderr", original_stderr))
