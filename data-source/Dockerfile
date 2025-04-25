FROM debian:bookworm-slim

RUN apt update
RUN apt install gcc g++ wget

WORKDIR /opt
RUN git clone https://github.com/karpathy/llama2.c.git
WORKDIR llama.c
RUN wget https://huggingface.co/karpathy/tinyllamas/resolve/main/stories15M.bin
RUN make run


