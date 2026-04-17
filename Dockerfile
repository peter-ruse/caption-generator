FROM python:3.13-slim

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends curl && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ARG TARGETPLATFORM
RUN if [ "$TARGETPLATFORM" = "linux/arm64" ]; \
    then BINARY="tailwindcss-linux-arm64"; else BINARY="tailwindcss-linux-x64"; fi && \
    curl -sLO "https://github.com/tailwindlabs/tailwindcss/releases/latest/download/${BINARY}" && \
    mv "${BINARY}" tailwind && \
    chmod +x tailwind && \
    mkdir -p static/src && printf '%s\n' \
    '@import "tailwindcss";' \
    '' \
    '@source "./templates/**/*.html";' \
    '' \
    '@variant dark (&:where(.dark, .dark *));' \
    '' \
    '@layer base {' \
    '  button,' \
    '  [type="button"],' \
    '  [type="reset"],' \
    '  [type="submit"] {' \
    '    cursor: pointer;' \
    '  }' \
    '}' > ./static/src/input.css && \
    ./tailwind -i ./static/src/input.css -o ./static/dist/main.css --minify

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
