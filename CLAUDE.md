# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Dify Shell Plugin — a Dify Tool plugin that executes shell commands with security controls (blocklist/allowlist, timeout, working directory restrictions). Designed to run on Linux servers alongside a Dify instance.

## Commands

```bash
# Install dependencies (requires Python 3.12)
cd shell && uv sync --python 3.12

# Run the plugin (connects to Dify plugin daemon via .env config)
cd shell && uv run python -m main

# Quick import check
cd shell && uv run python -c "from dify_plugin import Plugin; print('OK')"
```

## Architecture

The plugin follows the standard Dify plugin structure:

- **`manifest.yaml`** — Plugin identity, permissions (tool + storage), and runtime config (Python 3.12, entrypoint: main). Must include `description` field or the daemon rejects it.
- **`provider/shell.yaml`** — Declares the tool provider and its `credentials_for_provider` (security config fields shown to users during plugin installation). The `extra.python.source` path must be relative to project root (e.g. `provider/shell.py`), not relative to the yaml file.
- **`provider/shell.py`** — Validates credentials by running `echo hello` through the tool.
- **`tools/shell_command.yaml`** — Tool parameter definitions (`command`, `args`) and output schema (`stdout`, `stderr`, `exit_code`, `command`). Parameters use `form: llm` so the AI agent fills them.
- **`tools/shell_command.py`** — Core logic: parses credentials for security config, validates the command against blocklist then allowlist, checks pipe/chain operators for injection, runs via `subprocess.run(shell=True)`, returns `ToolInvokeMessage` variants (variable, json, text).
- **`main.py`** — Entry point: `Plugin(DifyPluginEnv()).run()`

## Key Design Decisions

- **Security is credential-driven**: `allowed_commands`, `blocked_commands`, `working_directory`, `timeout` are all configured via `credentials_for_provider` in the Dify UI, not hardcoded. If `blocked_commands` is empty, `DEFAULT_BLOCKED_COMMANDS` (30+ dangerous commands) is used.
- **Blocklist takes priority over allowlist**: blocked commands are checked first, then allowlist (if configured). Pipe/chain injection (`|`, `&&`, `;`, `||`) is also scanned for blocked commands.
- **Triple output format**: each invocation yields `create_variable_message` (for downstream workflow variables), `create_json_message` (structured data), and `create_text_message` (human-readable with code blocks).

## Deployment

This plugin must run on a **Linux server** where the Dify plugin daemon is accessible. The `.env` file configures the remote debug connection (`REMOTE_INSTALL_HOST`, `REMOTE_INSTALL_PORT`, `REMOTE_INSTALL_KEY`). Running on Windows will cause shell command incompatibilities.
