![Key-Gen Repository Banner](banner.png)
# Key-Gen (Linux)

`key-gen` is an interactive, dependency-free Python 3 password and memorable-key generator. It uses Python's `secrets` module rather than `random` and provides conventional passwords with lengths from **8–32**, security levels **1–25**, and batches of **1–75** results.

## Files

- `key-gen.py` — the program.
- `install-key-gen.sh` — installer/uninstaller for the `key-gen` terminal command.

## Customize the banner

Open `key-gen.py` and edit these values near the beginning:

```python
ASCII_ART = r"""
Your ASCII art here
""".strip("\n")
ASCII_SIGNATURE = "@your_handle"
```

The art and signature are automatically centered at the top of the loading screen and interactive screens.

## Install on Linux

Open a terminal in the directory containing both files.

### Per-user installation (recommended; no sudo)

```bash
chmod +x install-key-gen.sh
./install-key-gen.sh --user
```

If the installer says `~/.local/bin` is not in your `PATH`, add this line to `~/.profile`:

```bash
export PATH="$HOME/.local/bin:$PATH"
```

Then close and reopen the terminal (or run `source ~/.profile`).

### System-wide installation

This places the command in `/usr/local/bin`:

```bash
chmod +x install-key-gen.sh
sudo ./install-key-gen.sh --system
```

This approach works on most Linux distributions because it needs only a POSIX shell, Python 3, and the standard `install` command. It does not depend on a particular package manager.

## Use

Start the TUI:

```bash
key-gen
```

It first asks you to choose a mode:

1. **Secure password** — choose password length (8–32), security level (1–25), and result count (1–75).
2. **Memorable key** — choose 4–12 randomly selected words, a separator (`-`, `.`, or `_`), and result count (1–75).

A memorable key looks similar to:

```text
snow-rabbit-tulip-bluebird-daisy-dawn-citrus-stone
```

The words are chosen with cryptographically secure randomness. Use **8 or more words** for important accounts. A conventional high-level random password is usually the better choice when a website accepts it and a password manager is available.

At any input prompt, type `/exit`, or press **Ctrl+C**, to quit.

Show the full table describing all 25 levels:

```bash
key-gen --help
```

Disable colors if needed:

```bash
key-gen --no-color
```

## Uninstall

For a user installation:

```bash
./install-key-gen.sh --user --uninstall
```

For a system-wide installation:

```bash
sudo ./install-key-gen.sh --system --uninstall
```

## Notes

Passwords are printed to the terminal. Do not run the tool in a shared terminal session or leave generated passwords visible on screen. Store important passwords in a reputable password manager.
