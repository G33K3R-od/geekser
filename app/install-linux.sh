#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"
BIN_DIR="${HOME}/.local/bin"
DESKTOP_DIR="${XDG_DATA_HOME:-$HOME/.local/share}/applications"
mkdir -p "$BIN_DIR" "$DESKTOP_DIR"

# Generate an executable wrapper: GitHub's file API can leave the tracked
# app/geekser script non-executable after checkout/pull.
cat > "$BIN_DIR/geekser" <<EOF
#!/usr/bin/env bash
exec /usr/bin/env bash "$ROOT/app/geekser" "\$@"
EOF
chmod +x "$BIN_DIR/geekser"
cat > "$DESKTOP_DIR/geekser.desktop" <<EOF
[Desktop Entry]
Type=Application
Name=Geekser (Development)
Comment=Built by G33K. Made for geeks.
Exec=$BIN_DIR/geekser
Terminal=false
Categories=Network;WebBrowser;
Icon=firefox
StartupNotify=true
EOF
printf 'Geekser installed. Launch from applications or run: %s/geekser\n' "$BIN_DIR"
