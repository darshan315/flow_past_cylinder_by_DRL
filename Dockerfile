# use Ubuntu 20.04 as base
FROM ubuntu:20.04

# argument to avoid user interaction during installation
ARG DEBIAN_FRONTEND=noninteractive

# install pip (python 3)
RUN apt-get update && apt-get install -y  \
  dvipng \
  ffmpeg \
  pandoc \
  python3-matplotlib \
  python3-numpy \
  python3-pandas \
  python3-pip \
  python3-scipy \
  python3-tqdm \
  python3-tabulate \
  texlive-latex-extra \
  texlive-fonts-recommended && \
  rm -rf /var/lib/apt/lists/*

# update pip and install scikit learn and pytorch
RUN pip3 install \
  jupyter \
  jupyterlab \
  scikit-learn \
  torch==1.6.0+cpu torchvision==0.7.0+cpu -f https://download.pytorch.org/whl/torch_stable.html

# expose port to run in browser
EXPOSE 8888
