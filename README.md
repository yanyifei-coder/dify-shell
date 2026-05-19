# dify-shell

[English](README_en.md) | 简体中文

Shell 工具插件，允许在 Dify 应用中执行系统 Shell 命令，支持安全控制和灵活配置。

## 功能特性

- **Shell 命令执行**：在 Dify 应用中直接执行系统命令
- **安全控制**：
  - 黑名单机制：默认阻止危险命令（rm, sudo, chmod, dd, mkfs 等）
  - 白名单模式：可配置仅允许特定命令
  - 管道链检查：检测命令链中的危险操作
- **灵活配置**：
  - 自定义工作目录
  - 可调超时时间
  - 黑名单/白名单命令列表
- **结构化输出**：返回 stdout、stderr、exit_code 等完整信息

## 支持的命令

### 默认阻止的危险命令

| 类别 | 命令 |
|------|------|
| 文件操作 | rm, rmdir, mv, chmod, chown, chgrp |
| 磁盘操作 | dd, mkfs, format, fdisk, parted, mkswap |
| 系统控制 | shutdown, reboot, halt, poweroff, systemctl, service |
| 进程管理 | kill, pkill, killall |
| 网络安全 | iptables, ip6tables |
| 定时任务 | crontab, at, batch |
| 用户管理 | passwd, useradd, userdel, usermod, groupadd, groupdel |
| 挂载操作 | mount, umount |

### 允许的常见命令

ls, cat, pwd, echo, grep, find, wc, head, tail, sort, uniq, awk, sed, cut, tr, tee, xargs, curl, wget, tar, gzip, unzip, git, python, node, npm, docker, ssh, scp, rsync, ping, nslookup, dig, netstat, ps, top, df, du, free, lsblk, mount, which, whereis, file, stat, hexdump, od, base64, md5sum, sha256sum

## 安装

### 方式一：远程调试（开发中）

```bash
# 1. 克隆项目
git clone https://github.com/your-name/dify-shell.git
cd dify-shell/shell

# 2. 安装依赖
pip install -e .

# 3. 配置环境变量
cp .env.example .env
# 编辑 .env，填入调试密钥

# 4. 启动调试
python -m main
```

### 方式二：打包安装（生产环境）

```bash
# 下载 Dify Plugin CLI
wget https://github.com/langgenius/dify-plugin-daemon/releases/latest/download/dify-plugin-linux-amd64
chmod +x dify-plugin-linux-amd64

# 打包插件
./dify-plugin-linux-amd64 plugin package . -o shell-0.0.1.difypkg
```

## 配置说明

在 Dify 插件市场配置以下参数：

| 参数 | 说明 | 默认值 |
|------|------|--------|
| Allowed Commands | 允许的命令列表（逗号分隔），留空则允许所有（除黑名单） | - |
| Blocked Commands | 禁止的命令列表（逗号分隔） | 危险命令列表 |
| Working Directory | 命令执行的工作目录 | /tmp |
| Timeout | 最大执行时间（秒） | 30 |

## 使用示例

### 在 Dify 应用中使用

1. 在 Dify 插件市场安装 Shell 插件
2. 在应用中添加 Shell 工具
3. 配置插件参数（可选）
4. 在应用中使用工具执行命令

### API 调用示例

```python
# 命令参数
{
    "command": "ls",
    "args": "-la /home"
}

# 返回结果
{
    "stdout": "total 4096 May 18 21:00 .\ndrwxr-xr-x 19 root root 4096 May 18 21:00 ..\n...",
    "stderr": "",
    "exit_code": 0,
    "command": "ls -la /home"
}
```

## 项目结构

```
dify-shell/
├── shell/
│   ├── main.py                 # 插件入口
│   ├── manifest.yaml           # 插件清单
│   ├── pyproject.toml          # Python 项目配置
│   ├── .env.example            # 环境变量示例
│   ├── provider/
│   │   ├── shell.py            # Provider 实现
│   │   └── shell.yaml          # Provider 配置
│   └── tools/
│       ├── shell_command.py    # Shell 命令工具实现
│       └── shell_command.yaml  # 工具配置
├── CLAUDE.md                   # Claude 开发指南
├── LICENSE                     # MIT 许可证
├── README.md                   # 本文件
└── README_en.md                # English README
```

## 安全建议

1. **生产环境使用白名单模式**：只允许必要的命令
2. **设置合理的超时时间**：防止命令卡死
3. **限制工作目录**：使用专用目录
4. **定期审查日志**：监控命令执行情况

## 注意事项

- Windows 系统命令可能与 Linux 不同
- 某些命令需要特定权限
- 网络命令可能受防火墙限制

## 开发指南

```bash
# 安装开发依赖
pip install -e ".[dev]"

# 运行测试
pytest tests/

# 代码格式化
black .
ruff check .
```

## 贡献

欢迎提交 Issue 和 Pull Request！

1. Fork 本仓库
2. 创建特性分支：`git checkout -b feature/AmazingFeature`
3. 提交更改：`git commit -m 'Add some AmazingFeature'`
4. 推送分支：`git push origin feature/AmazingFeature`
5. 创建 Pull Request

## 许可证

本项目采用 MIT 许可证 - 详见 [LICENSE](LICENSE) 文件

## 相关链接

- [Dify 文档](https://docs.dify.ai/)
- [Dify 插件开发指南](https://docs.dify.ai/zh/develop-plugin)
- [Dify 插件市场](https://cloud.dify.ai/plugins)
