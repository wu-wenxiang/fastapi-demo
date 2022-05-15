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

### 2.1 框架搭建

参考：<https://github.com/tiangolo/full-stack-fastapi-couchbase>

```bash
pip install cookiecutter
cookiecutter https://github.com/tiangolo/full-stack-fastapi-couchbase
```

输入参数：

```console
project_name [Base Project]: fastapi-demo
project_slug [fastapi-demo]: 
domain_main [fastapi-demo.com]: 
domain_staging [stag.fastapi-demo.com]: 
docker_swarm_stack_name_main [fastapi-demo-com]: 
docker_swarm_stack_name_staging [stag-fastapi-demo-com]: 
secret_key [changethis]: 8861610eceb544c69098cb38c351e764
first_superuser [admin@fastapi-demo.com]: 
first_superuser_password [changethis]: 4dc2863ed5c24f4ebc410d28b5092d4c
backend_cors_origins [http://localhost, http://localhost:4200, http://localhost:3000, http://localhost:8080, https://localhost, https://localhost:4200, https://localhost:3000, https://localhost:8080, http://dev.fastapi-demo.com, https://stag.fastapi-demo.com, https://fastapi-demo.com, http://local.dockertoolbox.tiangolo.com, http://localhost.tiangolo.com]: 
smtp_port [587]: 
smtp_host []: 
smtp_user []: 
smtp_password []: 
smtp_emails_from_email [info@fastapi-demo.com]: 
couchbase_user [admin]: 
couchbase_password [changethis]: 081eb822042145778267b30eea0438ab
couchbase_sync_gateway_cors [http://localhost:4984, http://localhost:4985, http://localhost, http://localhost:4200, http://localhost:3000, http://localhost:8080, http://dev.fastapi-demo.com, https://stag.fastapi-demo.com, https://db.stag.fastapi-demo.com, https://fastapi-demo.com, https://db.fastapi-demo.com, http://local.dockertoolbox.tiangolo.com, http://local.dockertoolbox.tiangolo.com:4984, http://localhost.tiangolo.com, http://localhost.tiangolo.com:4984]: 
couchbase_sync_gateway_user [sync]: 
couchbase_sync_gateway_password [changethis]: 12e3d124c6bb42158667f830f123df15
traefik_constraint_tag [fastapi-demo.com]: 
traefik_constraint_tag_staging [stag.fastapi-demo.com]: 
traefik_public_network [traefik-public]: 
traefik_public_constraint_tag [traefik-public]: 
flower_auth [admin:4dc2863ed5c24f4ebc410d28b5092d4c]: 
sentry_dsn []: 
docker_image_prefix []: 
docker_image_backend [backend]: 
docker_image_celeryworker [celeryworker]: 
docker_image_frontend [frontend]: 
docker_image_sync_gateway [sync-gateway]: 
```

```
$ tree fastapi-demo
fastapi-demo
├── README.md
├── backend
│   ├── app
│   │   ├── Pipfile
│   │   ├── app
│   │   │   ├── __init__.py
│   │   │   ├── api
│   │   │   │   ├── __init__.py
│   │   │   │   ├── api_v1
│   │   │   │   │   ├── __init__.py
│   │   │   │   │   ├── api.py
│   │   │   │   │   └── endpoints
│   │   │   │   │       ├── __init__.py
│   │   │   │   │       ├── items.py
│   │   │   │   │       ├── login.py
│   │   │   │   │       ├── roles.py
│   │   │   │   │       ├── users.py
│   │   │   │   │       └── utils.py
│   │   │   │   └── utils
│   │   │   │       ├── __init__.py
│   │   │   │       └── security.py
│   │   │   ├── backend_pre_start.py
│   │   │   ├── celeryworker_pre_start.py
│   │   │   ├── core
│   │   │   │   ├── __init__.py
│   │   │   │   ├── celery_app.py
│   │   │   │   ├── config.py
│   │   │   │   ├── jwt.py
│   │   │   │   └── security.py
│   │   │   ├── crud
│   │   │   │   ├── __init__.py
│   │   │   │   ├── item.py
│   │   │   │   ├── user.py
│   │   │   │   └── utils.py
│   │   │   ├── db
│   │   │   │   ├── __init__.py
│   │   │   │   ├── couchbase_utils.py
│   │   │   │   ├── database.py
│   │   │   │   ├── full_text_search_utils.py
│   │   │   │   └── init_db.py
│   │   │   ├── email-templates
│   │   │   │   ├── build
│   │   │   │   │   ├── new_account.html
│   │   │   │   │   ├── reset_password.html
│   │   │   │   │   └── test_email.html
│   │   │   │   └── src
│   │   │   │       ├── new_account.mjml
│   │   │   │       ├── reset_password.mjml
│   │   │   │       └── test_email.mjml
│   │   │   ├── main.py
│   │   │   ├── models
│   │   │   │   ├── __init__.py
│   │   │   │   ├── config.py
│   │   │   │   ├── item.py
│   │   │   │   ├── msg.py
│   │   │   │   ├── role.py
│   │   │   │   ├── token.py
│   │   │   │   └── user.py
│   │   │   ├── search_index_definitions
│   │   │   │   ├── items.json
│   │   │   │   ├── items_01.json
│   │   │   │   ├── users.json
│   │   │   │   └── users_01.json
│   │   │   ├── tests
│   │   │   │   ├── __init__.py
│   │   │   │   ├── api
│   │   │   │   │   ├── __init__.py
│   │   │   │   │   └── api_v1
│   │   │   │   │       ├── __init__.py
│   │   │   │   │       ├── test_celery.py
│   │   │   │   │       ├── test_items.py
│   │   │   │   │       ├── test_login.py
│   │   │   │   │       └── test_users.py
│   │   │   │   ├── conftest.py
│   │   │   │   ├── crud
│   │   │   │   │   ├── __init__.py
│   │   │   │   │   ├── test_get_ids.py
│   │   │   │   │   ├── test_item.py
│   │   │   │   │   └── test_user.py
│   │   │   │   └── utils
│   │   │   │       ├── __init__.py
│   │   │   │       ├── item.py
│   │   │   │       ├── user.py
│   │   │   │       └── utils.py
│   │   │   ├── tests_pre_start.py
│   │   │   ├── utils.py
│   │   │   └── worker.py
│   │   ├── prestart.sh
│   │   ├── scripts
│   │   │   └── lint.sh
│   │   ├── tests-start.sh
│   │   └── worker-start.sh
│   ├── backend.dockerfile
│   ├── celeryworker.dockerfile
│   └── tests.dockerfile
├── cookiecutter-config-file.yml
├── docker-compose.deploy.build.yml
├── docker-compose.deploy.command.yml
├── docker-compose.deploy.images.yml
├── docker-compose.deploy.labels.yml
├── docker-compose.deploy.networks.yml
├── docker-compose.deploy.volumes-placement.yml
├── docker-compose.dev.build.yml
├── docker-compose.dev.command.yml
├── docker-compose.dev.env.yml
├── docker-compose.dev.labels.yml
├── docker-compose.dev.networks.yml
├── docker-compose.dev.ports.yml
├── docker-compose.dev.volumes.yml
├── docker-compose.shared.admin.yml
├── docker-compose.shared.base-images.yml
├── docker-compose.shared.depends.yml
├── docker-compose.shared.env.yml
├── docker-compose.test.yml
├── env-backend.env
├── env-couchbase.env
├── env-flower.env
├── env-sync-gateway.env
├── frontend
│   ├── Dockerfile
│   ├── README.md
│   ├── babel.config.js
│   ├── nginx-backend-not-found.conf
│   ├── package.json
│   ├── public
│   │   ├── favicon.ico
│   │   ├── img
│   │   │   └── icons
│   │   │       ├── android-chrome-192x192.png
│   │   │       ├── android-chrome-512x512.png
│   │   │       ├── apple-touch-icon-120x120.png
│   │   │       ├── apple-touch-icon-152x152.png
│   │   │       ├── apple-touch-icon-180x180.png
│   │   │       ├── apple-touch-icon-60x60.png
│   │   │       ├── apple-touch-icon-76x76.png
│   │   │       ├── apple-touch-icon.png
│   │   │       ├── favicon-16x16.png
│   │   │       ├── favicon-32x32.png
│   │   │       ├── msapplication-icon-144x144.png
│   │   │       ├── mstile-150x150.png
│   │   │       └── safari-pinned-tab.svg
│   │   ├── index.html
│   │   ├── manifest.json
│   │   └── robots.txt
│   ├── src
│   │   ├── App.vue
│   │   ├── api.ts
│   │   ├── assets
│   │   │   └── logo.png
│   │   ├── component-hooks.ts
│   │   ├── components
│   │   │   ├── NotificationsManager.vue
│   │   │   ├── RouterComponent.vue
│   │   │   └── UploadButton.vue
│   │   ├── env.ts
│   │   ├── interfaces
│   │   │   └── index.ts
│   │   ├── main.ts
│   │   ├── plugins
│   │   │   ├── vee-validate.ts
│   │   │   └── vuetify.ts
│   │   ├── registerServiceWorker.ts
│   │   ├── router.ts
│   │   ├── shims-tsx.d.ts
│   │   ├── shims-vue.d.ts
│   │   ├── store
│   │   │   ├── admin
│   │   │   │   ├── actions.ts
│   │   │   │   ├── getters.ts
│   │   │   │   ├── index.ts
│   │   │   │   ├── mutations.ts
│   │   │   │   └── state.ts
│   │   │   ├── index.ts
│   │   │   ├── main
│   │   │   │   ├── actions.ts
│   │   │   │   ├── getters.ts
│   │   │   │   ├── index.ts
│   │   │   │   ├── mutations.ts
│   │   │   │   └── state.ts
│   │   │   └── state.ts
│   │   ├── utils.ts
│   │   └── views
│   │       ├── Login.vue
│   │       ├── PasswordRecovery.vue
│   │       ├── ResetPassword.vue
│   │       └── main
│   │           ├── Dashboard.vue
│   │           ├── Main.vue
│   │           ├── Start.vue
│   │           ├── admin
│   │           │   ├── Admin.vue
│   │           │   ├── AdminUsers.vue
│   │           │   ├── CreateUser.vue
│   │           │   └── EditUser.vue
│   │           └── profile
│   │               ├── UserProfile.vue
│   │               ├── UserProfileEdit.vue
│   │               └── UserProfileEditPassword.vue
│   ├── tests
│   │   └── unit
│   │       └── upload-button.spec.ts
│   ├── tsconfig.json
│   ├── tslint.json
│   └── vue.config.js
├── scripts
│   ├── build-push.sh
│   ├── build.sh
│   ├── deploy.sh
│   ├── test-local.sh
│   └── test.sh
└── sync-gateway
    ├── Dockerfile
    ├── create_config.py
    ├── entrypoint.sh
    └── sync
        └── sync-function.js

42 directories, 174 files
```

重命名为 `fastapi-demo-template`

### 2.2 
