# 使用Python 3.12.10作为基础镜像
FROM python:3.12.10

# 设置工作目录为/sdk_server2
WORKDIR /home/cq_server



# 替换为清华源（适配 Debian bookworm）
RUN echo "替换 apt 源为清华源..." && \
    (test -f /etc/apt/sources.list && mv /etc/apt/sources.list /etc/apt/sources.list.bak) || true && \
    echo "deb https://mirrors.tuna.tsinghua.edu.cn/debian/ bookworm main contrib non-free non-free-firmware" > /etc/apt/sources.list && \
    echo "deb-src https://mirrors.tuna.tsinghua.edu.cn/debian/ bookworm main contrib non-free non-free-firmware" >> /etc/apt/sources.list && \
    echo "deb https://mirrors.tuna.tsinghua.edu.cn/debian-security/ bookworm-security main contrib non-free non-free-firmware" >> /etc/apt/sources.list && \
    echo "deb-src https://mirrors.tuna.tsinghua.edu.cn/debian-security/ bookworm-security main contrib non-free non-free-firmware" >> /etc/apt/sources.list && \
    echo "deb https://mirrors.tuna.tsinghua.edu.cn/debian/ bookworm-updates main contrib non-free non-free-firmware" >> /etc/apt/sources.list && \
    echo "deb-src https://mirrors.tuna.tsinghua.edu.cn/debian/ bookworm-updates main contrib non-free non-free-firmware" >> /etc/apt/sources.list


# 安装系统依赖（如需编译Python包可能需要这些工具）
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    gcc \
    libssl-dev \
    libffi-dev \
    python3-dev libodbc1 libodbc2 unixodbc

# 用 pip 命令直接设置全局源（无需手动创建配置文件）
RUN pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple/ && \
    pip config set global.trusted-host pypi.tuna.tsinghua.edu.cn


# 复制requirements.txt到容器中（利用Docker缓存机制）
COPY ./cq_server/requirements.txt .

# 安装依赖，确保编译并永久保存到镜像中
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt



# 设置容器启动命令
CMD ["python", "manage.py"]


