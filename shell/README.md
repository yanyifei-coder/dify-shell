# Shell

Execute shell commands and return results with security controls.

## Features

- Execute shell commands with real-time output
- Configurable command timeout (default 10s, max 300s)
- Security controls: blocklist/allowlist mechanism
- Working directory support
- Environment variable configuration
- Standard output and error output capture

## Configuration

| Parameter | Description | Default |
|-----------|-------------|---------|
| Allowed Commands | Allowed command list (comma-separated), empty means allow all (except blocklist) | - |
| Blocked Commands | Blocked command list (comma-separated) | Dangerous commands list |
| Working Directory | Working directory for command execution | /tmp |
| Timeout | Maximum execution time (seconds) | 30 |

## Usage

1. Install the Shell plugin from Dify plugin marketplace
2. Add the Shell tool in your application or workflow
3. Configure plugin parameters (optional)
4. Use the tool to execute commands

### Example

**Input:**
```
command: ls
args: -la /home
```

**Output:**
```json
{
    "stdout": "total 4096 May 18 21:00 .\ndrwxr-xr-x 19 root root 4096 May 18 21:00 ..\n...",
    "stderr": "",
    "exit_code": 0,
    "command": "ls -la /home"
}
```

## Security

- Dangerous commands are blocked by default (rm, sudo, chmod, dd, mkfs, etc.)
- Pipeline chain detection prevents bypassing security controls
- Use allowlist mode in production for maximum security
- Set reasonable timeout to prevent command hangs

## Privacy

This plugin does not collect, store, or transmit any personal data to external services. Command execution occurs locally on the server where the plugin is running. See [PRIVACY.md](./privacy.md) for details.
