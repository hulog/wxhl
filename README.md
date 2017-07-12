# wxhl
微信app
## 部署说明

1. 确保服务器有`Python`环境(废话).
2. 需要安装的包相关：`web.py`,`requests`,`lxml`等.
3. 将`index.wsgi`备份，重命名为`index.py`.
4. vim `index.py` 将文中代码进行替换
  将
  ```python
  app = web.application(urls, globals()).wsgifunc()        
  application = sae.create_wsgi_app(app)
  ```
  替换成
  ```python
  if __name__ == "__main__":
    app = web.application(urls, globals())
    app.run()
  ```
5. 去掉`index.py`中的`sae`模块，并移除第6行`sae.add_vendor_dir('vendor')`.
6. 正常使用图灵机器人，需要修改`talk_api.py`第10行 `da = {"key": "9a978db57a90xxxxx3f0b52fcfe040b", "info": content, "userid":userid}`中的`key`值.
7. 执行`python index.py`即可开启默认**8080**端口供访问.
8. 如需对接公众号，必须是外网**80**端口。可以将`7`中的端口改为**8080**，也可以用`nginx`或者`apache`转发.
