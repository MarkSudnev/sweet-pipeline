FROM debian:bookworm-slim

RUN apt update
RUN apt install -y gcc g++ wget python3 python3-pip python3-venv git

WORKDIR /opt
RUN git clone https://github.com/karpathy/llama2.c.git
WORKDIR /opt/llama2.c
RUN wget https://huggingface.co/karpathy/tinyllamas/resolve/main/stories15M.bin
RUN make run

RUN mkdir -p /opt/api
COPY src /opt/api
WORKDIR /opt/api
RUN python3 -m venv venv
RUN /opt/api/venv/bin/python -m pip install --no-cache-dir -r requirements.txt

EXPOSE 8091

CMD ["/opt/api/venv/bin/python", "-m", "flask", "--app", "app", "run", "--host=0.0.0.0", "--port=8091"]
