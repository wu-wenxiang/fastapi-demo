# fastapi-demo

- Github: <https://github.com/wu-wenxiang/fastapi-demo>
- 同步到 Gitee: <https://gitee.com/wu-wen-xiang/fastapi-demo>

## 1. 搭建过程

[如何基于 FastAPI 搭建一个用于生产的 Restful API 框架？](doc/how-to-build-fastapi-web-service.md)

## 2. 快速开始

### 2.1 本地调试

```bash
# 创建 python 虚拟环境
python -m virtualenv .venv
# 进入 python 虚拟环境
. .venv/bin/activate

# 安装依赖
pip3 install -i https://pypi.tuna.tsinghua.edu.cn/simple -r requirements.txt
# 清理 sqlite 数据库 && 初始化数据库
rm -rf /tmp/rest-demo.db && python datainit.py

# 启动 web 服务
python run.py
# python run.py 0.0.0.0 8080
# 尝试访问
curl http://localhost:8080/
```

### 2.2 单元测试和代码格式检查

```bash
# python setup.py test -q
# stestr run
tox
```

### 2.3 接口测试

```bash
cd gabbi

ls *.yaml | xargs gabbi-run localhost:8080 --

# show verbose
gabbi-run -v all localhost:8080 -- crud-user.yaml
```

### 2.4 容器镜像制作和部署

```bash
DOCKER_NAME=fastapi-demo
DOCKER_IMAGE=99cloud/${DOCKER_NAME}

docker build -t ${DOCKER_IMAGE} .
docker stop ${DOCKER_NAME}; docker rm ${DOCKER_NAME}
docker run -d --name ${DOCKER_NAME} -p 8888:8080 ${DOCKER_IMAGE}
curl http://localhost:8888/
```
