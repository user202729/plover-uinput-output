# plover-uinput-output

Use uinput to emulate keyboard, instead of xtest, which might conflict with some applications.

Requires root privilege.

(uses `sudo`. It might fail silently if `sudo` prompts)

**Note**: the current (as of the time of writing) version of Plover does not support
output plugins, you can enable it by enabling the corresponding extension plugin.
The internal API are used, it might breaking at any time.

