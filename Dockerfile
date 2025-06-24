FROM denoland/deno:2.3.5

RUN apt-get update && \
    apt-get install -y python3.11 python3.11-venv python3.11-distutils python3-pip curl && \
    ln -sf /usr/bin/python3.11 /usr/bin/python3 && \
    python3 -m venv /opt/venv && \
    /opt/venv/bin/pip install uv && \
    rm -rf /var/lib/apt/lists/*

ENV PATH="/opt/venv/bin:$PATH"

WORKDIR /app

ENV DENO_DIR=/deno-dir
RUN mkdir -p $DENO_DIR && chmod -R 777 $DENO_DIR
RUN deno cache jsr:@pydantic/mcp-run-python

WORKDIR /app

COPY pyproject.toml uv.lock ./
# RUN uv venv
RUN uv pip install --no-cache-dir .

COPY src ./src
COPY tests ./tests
COPY .env pytest.ini ./

EXPOSE 3000

CMD ["python", "src/main.py"]