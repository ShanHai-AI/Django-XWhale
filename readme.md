🚀 **Linux 下 Nginx+uWSGI HTTPS 部署 Django 项目指南** 🚀

---

## 📦 一、安装 uWSGI

```bash
# 安装 uWSGI 📦
pip install uwsgi

# 查看版本信息 📊
uwsgi --version
```

---

## ⚙️ 二、配置 uWSGI + Django

### 1. 创建配置目录
在 Django 项目根目录（与 `manage.py` 同级）新建 `uwsgi_config` 文件夹：
```bash
mkdir /path/to/your/project/uwsgi_config
cd /path/to/your/project/uwsgi_config
```

### 2. 编写 uWSGI 配置文件 `uwsgi.ini`
```ini
[uwsgi]
# 📡 使用 socket 与 Nginx 通信（内网 IP 需替换为云服务器实际内网 IP）
socket = 192.168.3.14:5000

# 📍 项目根目录
chdir = /home/shanhai/Project/Django-XWhale

# 🧠 启动主进程管理
master = true

# 🧩 加载 WSGI 模块（替换为你的项目名）
module = XWhale.wsgi

# 🧑‍💻 工作进程数（建议与 CPU 核心数一致）
processes = 1

# 📦 日志配置
daemonize = /home/shanhai/Project/Django-XWhale/uwsgi_config/run.log

# 🧹 自动清理临时文件
vacuum = true

# 🐍 虚拟环境路径（通过 pip show django 获取）
pythonpath = /home/shanhai/anaconda3/envs/django5/lib/python3.10/site-packages

# 🔄 PID 文件用于重启/停止
pidfile = /home/shanhai/Project/Django-XWhale/uwsgi_config/uwsgi.pid

# 🧵 启用线程支持
enable-threads = true

# ⏱️ 优雅重启超时设置
reload-mercy = 8

# 📦 缓冲区大小优化
buffer-size = 65536
```

### 3. 管理 uWSGI 服务
```bash
# ▶️ 启动服务
uwsgi --ini uwsgi.ini

# 🔁 重启服务
uwsgi --reload uwsgi.pid

# ⏹️ 停止服务
uwsgi --stop uwsgi.pid

# 💥 强制终止（谨慎使用）
sudo pkill -f uwsgi -9
```

---

## 🔐 三、生成 SSL 证书（HTTPS 必备）

```bash
# 1️⃣ 生成带密码的私钥 🔐
openssl genrsa -des3 -out server.key 2048

# 2️⃣ 去除私钥密码（可选）
openssl rsa -in server.key -out server.key

# 3️⃣ 创建证书请求文件 📝
openssl req -new -key server.key -out server.csr

# 4️⃣ 生成自签名根证书 🌐
openssl req -new -x509 -key server.key -out ca.crt -days 3650

# 5️⃣ 签发服务器证书 ✅
openssl x509 -req -days 3650 -in server.csr -CA ca.crt -CAkey server.key -CAcreateserial -out server.crt
```

---

## 🛡️ 四、配置 Nginx

### 1. 创建 `uwsgi_params` 文件
```nginx
# uwsgi_params 配置文件
uwsgi_param  QUERY_STRING       $query_string;
uwsgi_param  REQUEST_METHOD     $request_method;
uwsgi_param  CONTENT_TYPE       $content_type;
uwsgi_param  CONTENT_LENGTH     $content_length;

uwsgi_param  REQUEST_URI        $request_uri;
uwsgi_param  PATH_INFO          $document_uri;
uwsgi_param  DOCUMENT_ROOT      $document_root;
uwsgi_param  SERVER_PROTOCOL    $server_protocol;
uwsgi_param  REQUEST_SCHEME     $scheme;
uwsgi_param  HTTPS              $https if_not_empty;

uwsgi_param  REMOTE_ADDR        $remote_addr;
uwsgi_param  REMOTE_PORT        $remote_port;
uwsgi_param  SERVER_PORT        $server_port;
uwsgi_param  SERVER_NAME        $server_name;
```

### 2. Nginx 主配置文件（`/etc/nginx/nginx.conf`）
```nginx
user root;
worker_processes auto;
pid /run/nginx.pid;

http {
  server {
    # 📡 监听 HTTPS 端口（示例：8005）
    listen 8005 ssl;
    server_name XWhale;

    # 🔐 SSL 证书路径
    ssl_certificate      /home/shanhai/Project/Django-XWhale/uwsgi_config/ssl/server.crt;
    ssl_certificate_key  /home/shanhai/Project/Django-XWhale/uwsgi_config/ssl/server.key;

    # 🕒 会话保持设置
    ssl_session_timeout  5000m;
    ssl_protocols        TLSv1 TLSv1.1 TLSv1.2;
    ssl_ciphers          HIGH:!aNULL:!MD5;
    ssl_prefer_server_ciphers  on;

    # 📡 反向代理到 uWSGI
    location / {
      uwsgi_pass 192.168.3.14:5000;
      include /home/shanhai/Project/Django-XWhale/uwsgi_config/uwsgi_params;
    }

    # 📁 静态文件服务
    location /static {
      alias /home/shanhai/Project/Django-XWhale/static;
    }
  }

  # 🧱 基础配置（保持默认即可）
  sendfile on;
  tcp_nopush on;
  gzip on;
}
```

### 3. Nginx 管理命令
```bash
# 🔍 检查配置文件语法
sudo nginx -t

# ♻️ 重载配置
sudo nginx -s reload

# 🔄 重启服务
sudo systemctl restart nginx

# 📋 查看状态
sudo systemctl status nginx

# 📄 实时查看日志
sudo tail -f /var/log/nginx/error.log
```

---

## ✅ 五、部署检查清单 🚦

| 步骤 | 状态 | 提示 |
|------|------|------|
| uWSGI 启动成功 | ✅/❌ | 检查 `run.log` 日志 |
| Nginx 配置语法正确 | ✅/❌ | `nginx -t` |
| 防火墙开放端口 | ✅/❌ | `ufw allow 8005` |
| 域名解析正确 | ✅/❌ | 指向服务器公网 IP |
| 静态文件收集 | ✅/❌ | `python manage.py collectstatic` |

---

🎉 **大功告成！现在可以通过 HTTPS 访问你的 Django 项目了！** 🎉  
如有疑问欢迎提交 Issue 💬 或参考官方文档 📚