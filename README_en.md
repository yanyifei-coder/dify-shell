# dify-shell

English | [简体中文](README.md)

A Shell tool plugin for Dify that allows executing system Shell commands within Dify applications, with security controls and flexible configuration.

## Features

- **Shell Command Execution**: Execute system commands directly in Dify applications
- **Security Controls**:
  - Blocklist mechanism: Blocks dangerous commands by default (rm, sudo, chmod, dd, mkfs, etc.)
  - Allowlist mode: Configure to only allow specific commands
  - Pipeline chain detection: Detects dangerous operations in command chains
- **Flexible Configuration**:
  - Custom working directory
  - Adjustable timeout
  - Blocklist/allowlist command configuration
- **Structured Output**: Returns complete information including stdout, stderr, exit_code

## Supported Commands

### Default Blocked Dangerous Commands

| Category | Commands |
|----------|----------|
| File Operations | rm, rmdir, mv, chmod, chown, chgrp |
| Disk Operations | dd, mkfs, format, fdisk, parted, mkswap |
| System Control | shutdown, reboot, halt, poweroff, systemctl, service |
| Process Management | kill, pkill, killall |
| Network Security | iptables, ip6tables |
| Scheduled Tasks | crontab, at, batch |
| User Management | passwd, useradd, userdel, usermod, groupadd, groupdel |
| Mount Operations | mount, umount |

### Common Allowed Commands

ls, cat, pwd, echo, grep, find, wc, head, tail, sort, uniq, awk, sed, cut, tr, tee, xargs, curl, wget, tar, gzip, unzip, git, python, node, npm, docker, ssh, scp, rsync, ping, nslookup, dig, netstat, ps, top, df, du, free, lsblk, mount, which, whereis, file, stat, hexdump, od, base64, md5sum, sha256sum

## Installation

### Method 1: Remote Debugging (Development)

```bash
# 1. Clone the project
git clone https://github.com/your-name/dify-shell.git
cd dify-shell/shell

# 2. Install dependencies
pip install -e .

# 3. Configure environment variables
cp .env.example .env
# Edit .env and fill in the debug key

# 4. Start debugging
python -m main
```

### Method 2: Package Installation (Production)

```bash
# Download Dify Plugin CLI
wget https://github.com/langgenius/dify-plugin-daemon/releases/latest/download/dify-plugin-linux-amd64
chmod +x dify-plugin-linux-amd64

# Package the plugin
./dify-plugin-linux-amd64 plugin package . -o shell-0.0.1.difypkg
```

## Configuration

Configure the following parameters in the Dify plugin marketplace:

| Parameter | Description | Default |
|-----------|-------------|---------|
| Allowed Commands | Allowed command list (comma-separated), empty means allow all (except blocklist) | - |
| Blocked Commands | Blocked command list (comma-separated) | Dangerous commands list |
| Working Directory | Working directory for command execution | /tmp |
| Timeout | Maximum execution time (seconds) | 30 |

## Usage Examples

### Using in Dify Application

1. Install Shell plugin from Dify plugin marketplace
2. Add Shell tool in your application
3. Configure plugin parameters (optional)
4. Use the tool to execute commands

### API Call Example

```python
# Command parameters
{
    "command": "ls",
    "args": "-la /home"
}

# Return result
{
    "stdout": "total 4096 May 18 21:00 .\ndrwxr-xr-x 19 root root 4096 May 18 21:00 ..\n...",
    "stderr": "",
    "exit_code": 0,
    "command": "ls -la /home"
}
```

## Project Structure

```
dify-shell/
├── shell/
│   ├── main.py                 # Plugin entry point
│   ├── manifest.yaml           # Plugin manifest
│   ├── pyproject.toml          # Python project config
│   ├── .env.example            # Environment variable template
│   ├── provider/
│   │   ├── shell.py            # Provider implementation
│   │   └── shell.yaml          # Provider config
│   └── tools/
│       ├── shell_command.py    # Shell command tool implementation
│       └── shell_command.yaml  # Tool config
├── CLAUDE.md                   # Claude development guide
├── LICENSE                     # MIT License
├── README.md                   # Chinese README
└── README_en.md                # This file
```

## Security Recommendations

1. **Use allowlist mode in production**: Only allow necessary commands
2. **Set reasonable timeout**: Prevent command hangs
3. **Limit working directory**: Use dedicated directories
4. **Regular log review**: Monitor command execution

## Notes

- Windows system commands may differ from Linux
- Some commands require specific permissions
- Network commands may be restricted by firewall

## Development Guide

```bash
# Install dev dependencies
pip install -e ".[dev]"

# Run tests
pytest tests/

# Code formatting
black .
ruff check .
```

## Contributing

Issues and Pull Requests are welcome!

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/AmazingFeature`
3. Commit your changes: `git commit -m 'Add some AmazingFeature'`
4. Push to the branch: `git push origin feature/AmazingFeature`
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details

## Related Links

- [Dify Documentation](https://docs.dify.ai/)
- [Dify Plugin Development Guide](https://docs.dify.ai/en/develop-plugin)
- [Dify Plugin Marketplace](https://cloud.dify.ai/plugins)
