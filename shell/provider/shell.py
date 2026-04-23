from typing import Any

from dify_plugin import ToolProvider
from dify_plugin.errors.tool import ToolProviderCredentialValidationError
from tools.shell_command import ShellCommandTool


class ShellProvider(ToolProvider):
    def _validate_credentials(self, credentials: dict[str, Any]) -> None:
        try:
            for _ in ShellCommandTool.from_credentials(credentials).invoke(
                tool_parameters={"command": "echo", "args": "hello"},
            ):
                pass
        except Exception as e:
            raise ToolProviderCredentialValidationError(str(e))
