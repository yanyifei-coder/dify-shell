# Privacy Policy - Shell Plugin

This plugin executes shell commands as specified by the user through Dify applications.

## Data Collection

- The plugin does not collect, store, or transmit any personal data to external services.
- Command execution occurs locally on the server where the plugin is running.
- Command outputs (stdout, stderr) are returned only to the Dify application that invoked the tool.

## Data Storage

- The plugin may use persistent storage to save user configuration (allowed/blocked commands, working directory, timeout settings).
- No command history is stored by default.

## Security

- The plugin implements a blocklist/allowlist mechanism to prevent execution of dangerous commands.
- Users are responsible for configuring appropriate security settings (allowed commands, blocked commands, working directory, timeout).
- The plugin executes commands with the same permissions as the plugin runtime process.

## Third-Party Services

- This plugin does not communicate with any third-party services or APIs.