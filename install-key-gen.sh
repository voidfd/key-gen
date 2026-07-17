#!/usr/bin/env sh
usage() {
    cat <<'EOF'
Usage: ./install-key-gen.sh [--user | --system | --uninstall]

  --user       Install to ~/.local/bin/key-gen (no root access required).
  --system     Install to /usr/local/bin/key-gen (default; requires root/sudo).
  --uninstall  Remove key-gen from the selected location.

Examples:
  ./install-key-gen.sh --user
  sudo ./install-key-gen.sh --system
  ./install-key-gen.sh --user --uninstall
EOF
}

[ "$(uname -s)" = "Linux" ] || { echo "This installer supports Linux only." >&2; exit 1; }

MODE=system
REMOVE=0
for arg in "$@"; do
    case "$arg" in
        --user) MODE=user ;;
        --system) MODE=system ;;
        --uninstall) REMOVE=1 ;;
        -h|--help) usage; exit 0 ;;
        *) echo "Unknown option: $arg" >&2; usage >&2; exit 2 ;;
    esac
done

SCRIPT_DIR=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
SOURCE="$SCRIPT_DIR/key-gen.py"

if [ "$MODE" = "user" ]; then
    DEST_DIR="${HOME}/.local/bin"
else
    DEST_DIR="/usr/local/bin"
fi
DEST="$DEST_DIR/key-gen"

if [ "$REMOVE" -eq 1 ]; then
    if [ -e "$DEST" ]; then
        if [ "$MODE" = "system" ] && [ "$(id -u)" -ne 0 ]; then
            echo "Run this command with sudo to remove the system installation:" >&2
            echo "  sudo $0 --system --uninstall" >&2
            exit 1
        fi
        rm -f "$DEST"
        echo "Removed $DEST"
    else
        echo "No key-gen command found at $DEST"
    fi
    exit 0
fi

command -v python3 >/dev/null 2>&1 || {
    echo "python3 is required. Install Python 3 with your Linux distribution's package manager." >&2
    exit 1
}
[ -f "$SOURCE" ] || { echo "Cannot find key-gen.py next to this installer." >&2; exit 1; }

if [ "$MODE" = "system" ] && [ "$(id -u)" -ne 0 ]; then
    echo "System installation requires administrator privileges." >&2
    echo "Run: sudo ./install-key-gen.sh --system" >&2
    echo "Or:  ./install-key-gen.sh --user" >&2
    exit 1
fi

mkdir -p "$DEST_DIR"
install -m 0755 "$SOURCE" "$DEST"
echo "Installed: $DEST"

if [ "$MODE" = "user" ]; then
    case ":${PATH}:" in
        *":${DEST_DIR}:"*) ;;
        *)
            echo
            echo "Note: $DEST_DIR is not currently in PATH. Add this line to ~/.profile, then open a new terminal:"
            echo "  export PATH=\"\$HOME/.local/bin:\$PATH\""
            ;;
    esac
fi

echo "Run: key-gen"
