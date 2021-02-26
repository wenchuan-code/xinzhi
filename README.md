#### python=3.6 

#### 安装依赖包

```
python install -r requirements.txt
```

#### 创建数据表
```
# 初始化，生成migrations文件包
python manage.py db init
# 迁移数据，生成data.db
python manage.py db migrate
# 更新数据
python manage.py db upgrade
```

#### debug模式启动
```
python manage.py debug
```

#### 生产模式启动
```
python manage.py run
```

#### Tests
```
python -m tests.testapp
```

###  Api 访问地址
```text
http://127.0.0.1:5000/api/v1/tests
```

### 查看 Api文档
```text
使用的是Flask-Docs生成的 flask-api文档

访问地址:http://127.0.0.1/docs/api

格式：
    @@@
    在注释结尾用 “@@@” 包含 markdown 格式文档
    @@@
```
