# 月报站点 · 本地部署说明

## 本机访问

在项目根目录执行：

```bash
cd dist
python3 -m http.server 8080
```

浏览器打开：**http://localhost:8080**

- 索引页：http://localhost:8080/
- 2025.11 多语言月报：http://localhost:8080/reports/2025-11/report.html

## 局域网访问

若需同一局域网内其他设备访问，请绑定到所有网卡：

```bash
cd dist
python3 -m http.server 8080 --bind 0.0.0.0
```

然后在浏览器使用：**http://\<本机IP\>:8080**（将 \<本机IP\> 替换为当前电脑在局域网中的 IP，如 192.168.1.100）。
