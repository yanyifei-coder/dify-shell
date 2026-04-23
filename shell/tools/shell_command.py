import shlex
import subprocess
from collections.abc import Generator
from typing import Any

from dify_plugin import Tool
from dify_plugin.entities.tool import ToolInvokeMessage

DEFAULT_BLOCKED_COMMANDS = {
    "rm", "rmdir", "mv", "sudo", "su", "chmod", "chown", "chgrp",
    "dd", "mkfs", "format", "shutdown", "reboot", "halt", "poweroff",
    "kill", "pkill", "killall",
    "fdisk", "parted", "mkswap", "mount", "umount",
    "iptables", "ip6tables", "systemctl", "service",
    "crontab", "at", "batch",
    "passwd", "useradd", "userdel", "usermod", "groupadd", "groupdel",
}


class ShellCommandTool(Tool):
    def _parse_command_list(self, raw: str) -> set[str]:
        """Parse comma-separated command list into a set of stripped, lowercased names."""
        if not raw or not raw.strip():
            return set()
        return {cmd.strip().lower() for cmd in raw.split(",") if cmd.strip()}

    def _get_base_command(self, full_command: str) -> str:
        """Extract the base command name from a full command string."""
        try:
            parts = shlex.split(full_command)
            return parts[0].lower() if parts else ""
        except ValueError:
            # Fallback: split by whitespace if shlex fails
            parts = full_command.strip().split()
            return parts[0].lower() if parts else ""

    def _check_dangerous_in_chain(self, full_command: str, blocked: set[str]) -> str | None:
        """Check if any dangerous command appears in pipe/chain operators."""
        # Split by common chain operators
        for sep in ["|", "&&", ";", "||"]:
            parts = full_command.split(sep)
            for part in parts:
                base = self._get_base_command(part)
                if base in blocked:
                    return base
        return None

    def _invoke(self, tool_parameters: dict[str, Any]) -> Generator[ToolInvokeMessage]:
        command = (tool_parameters.get("command") or "").strip()
        args = (tool_parameters.get("args") or "").strip()

        if not command:
            yield self.create_text_message("Error: No command specified.")
            return

        # Build full command string
        full_command = f"{command} {args}".strip() if args else command
        base_command = self._get_base_command(full_command)

        # Get security config from credentials
        credentials = self.runtime.credentials or {}
        allowed = self._parse_command_list(credentials.get("allowed_commands", ""))
        blocked = self._parse_command_list(credentials.get("blocked_commands", ""))
        if not blocked:
            blocked = DEFAULT_BLOCKED_COMMANDS

        working_dir = credentials.get("working_directory", "/tmp").strip() or "/tmp"
        timeout_str = credentials.get("timeout", "30").strip() or "30"
        try:
            timeout = int(timeout_str)
        except ValueError:
            timeout = 30

        # Security check: blocked commands (highest priority)
        if base_command in blocked:
            yield self.create_json_message({
                "stdout": "",
                "stderr": f"Command '{base_command}' is blocked for security reasons.",
                "exit_code": -1,
                "command": full_command,
            })
            yield self.create_text_message(f"Error: Command '{base_command}' is blocked for security reasons.")
            return

        # Check for dangerous commands in pipe/chain
        dangerous = self._check_dangerous_in_chain(full_command, blocked)
        if dangerous:
            yield self.create_json_message({
                "stdout": "",
                "stderr": f"Command '{dangerous}' is blocked in command chain for security reasons.",
                "exit_code": -1,
                "command": full_command,
            })
            yield self.create_text_message(f"Error: Command '{dangerous}' is blocked in command chain for security reasons.")
            return

        # Security check: whitelist mode
        if allowed and base_command not in allowed:
            yield self.create_json_message({
                "stdout": "",
                "stderr": f"Command '{base_command}' is not in the allowed list. Allowed: {', '.join(sorted(allowed))}",
                "exit_code": -1,
                "command": full_command,
            })
            yield self.create_text_message(f"Error: Command '{base_command}' is not in the allowed list.")
            return

        # Execute the command
        try:
            result = subprocess.run(
                full_command,
                shell=True,
                capture_output=True,
                text=True,
                timeout=timeout,
                cwd=working_dir,
            )

            stdout = result.stdout
            stderr = result.stderr
            exit_code = result.returncode

        except subprocess.TimeoutExpired:
            yield self.create_json_message({
                "stdout": "",
                "stderr": f"Command timed out after {timeout} seconds.",
                "exit_code": -1,
                "command": full_command,
            })
            yield self.create_text_message(f"Error: Command timed out after {timeout} seconds.")
            return
        except FileNotFoundError:
            yield self.create_json_message({
                "stdout": "",
                "stderr": f"Command '{base_command}' not found.",
                "exit_code": -1,
                "command": full_command,
            })
            yield self.create_text_message(f"Error: Command '{base_command}' not found.")
            return
        except Exception as e:
            yield self.create_json_message({
                "stdout": "",
                "stderr": f"Execution error: {str(e)}",
                "exit_code": -1,
                "command": full_command,
            })
            yield self.create_text_message(f"Error: {str(e)}")
            return

        # Return structured output
        yield self.create_variable_message("stdout", stdout)
        yield self.create_variable_message("stderr", stderr)
        yield self.create_variable_message("exit_code", exit_code)
        yield self.create_variable_message("command", full_command)

        yield self.create_json_message({
            "stdout": stdout,
            "stderr": stderr,
            "exit_code": exit_code,
            "command": full_command,
        })

        # Human-readable text output
        output_parts = []
        if stdout:
            output_parts.append(f"```\n{stdout}```")
        if stderr:
            output_parts.append(f"[stderr]\n```\n{stderr}```")
        output_parts.append(f"Exit code: {exit_code}")
        yield self.create_text_message("\n".join(output_parts))
