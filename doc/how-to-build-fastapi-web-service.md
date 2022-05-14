# How to Build a FastAPI Web Service

该项目用于 Demo 如何基于 FastAPI 搭建一个生产可用的 Restful API 服务

参考：

1. <https://github.com/mjhea0/awesome-fastapi>


## 1. Demo 内容

参考：<https://github.com/wu-wenxiang/restful-api-demo/blob/main/doc/how-to-build-rest-api-web-service.md>

### 1.1 同步写法和性能测试

1. 本 demo 研究 fastapi 的同步写法，异步写法已经在 OpenStack [Skyline](https://opendev.org/openstack/skyline-apiserver) 中尝试，工程开发效率和代码可读性不如同步友好
2. [对同步写法进行压测](/doc/how-to-take-a-stress-test-for-fastapi-sync-mode.md)

### 1.2 客户端对接

1. CLI 对接 restful API
2. react 前端框架对接 restful API

### 1.3 服务集成

1. 考虑 MQTT 服务集成，侦听和发送

### 1.4 实时输出显示

1. 基于 websocket 的长链接
1. 基于 restful 的增量日志

### 1.5 代码规范

项目测试接口：<https://governance.openstack.org/tc/reference/pti/python.html>

1. 单元测试：`stestr` & `pytest` / `unittest`
2. 代码风格检查：`tox -e pep8`
3. 覆盖率测试报告：`coverage` / `tox -e cover`
4. 源码包生成：`python setup.py sdist` / `python setup.py bdist_wheel`
5. 国际化：`babel`
6. 文档生成：`sphinx-build`
7. 自动格式化代码风格 `pylint`
8. API 接口文档：`API Doc` / `Swagger`

### 1.6 CI/CD

1. 容器镜像：`Dockerfile`
2. `.drone` 自动打包 / 部署
3. 数据初始化 `datainit.py`
4. 自动化接口测试 `gabbi`

### 1.7 开发流程

1. 先用户故事，前后端对齐
2. 数据库 + API，提交通过
3. 接口测试用例提交通过
4. 代码实现

### 1.8 ORM

1. SqlAlchemy：`Session Hook` / `Transaction` / `Relationship`
2. 支持 Sqlite3 做测试，MySQL 上生产
3. 数据库三范式，三表法
4. 级联删除

### 1.9 认证、鉴权和准入

1. 认证：本地认证和 OAUTH2
2. 鉴权：Casbin
3. 准入：API 计量，API Gateway，Kong

### 1.10 数据格式处理

1. API URL 定制化
2. 输入校验
3. 后端分页、排序、筛选框架

### 1.11 K8S 部署

1. K8S yaml
2. 数据库高可用
3. TLS 支持
4. Metrics 处理
5. Logging 处理

## 2. 搭建步骤