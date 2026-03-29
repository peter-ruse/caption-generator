#!/bin/bash

OS_TYPE=$(uname -s)
case "${OS_TYPE}" in
    Linux*)     BINARY="tailwindcss-linux-x64";;
    Darwin*)    BINARY="tailwindcss-macos-arm64";; # or x64 if on Intel
    *)          echo "Unsupported OS"; exit 1;;
esac

if [ ! -f "./tailwind" ]; then
    echo "Downloading Tailwind binary for ${OS_TYPE}..."
    curl -sLO "https://github.com/tailwindlabs/tailwindcss/releases/latest/download/${BINARY}"
    mv "${BINARY}" tailwind
    chmod +x tailwind
fi

echo "Preparing Tailwind source..."
mkdir -p static/src

cat <<EOF > ./static/src/input.css
@import "tailwindcss";

@source "./templates/**/*.html";

@variant dark (&:where(.dark, .dark *));

@layer base {
  button, 
  [type='button'], 
  [type='reset'], 
  [type='submit'] {
    cursor: pointer;
  }
}
EOF

echo "Building CSS..."
./tailwind -i ./static/src/input.css -o ./static/dist/main.css --minify

pip install -r requirements.txt