# https://hub.docker.com/r/cwaffles/openpose
FROM nvidia/cuda:10.0-cudnn7-devel

MAINTAINER StevenNguyen<stevennguyenusa19@gmail.com>

#get deps
RUN apt-get update && \
DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
python3-dev python3-pip git g++ wget make libprotobuf-dev protobuf-compiler libopencv-dev \
libgoogle-glog-dev libboost-all-dev libcaffe-cuda-dev libhdf5-dev libatlas-base-dev

#for python api
RUN pip3 install numpy opencv-python 

#replace cmake as old version has CUDA variable bugs
RUN wget https://github.com/Kitware/CMake/releases/download/v3.14.2/cmake-3.14.2-Linux-x86_64.tar.gz && \
tar xzf cmake-3.14.2-Linux-x86_64.tar.gz -C /opt && \
rm cmake-3.14.2-Linux-x86_64.tar.gz
ENV PATH="/opt/cmake-3.14.2-Linux-x86_64/bin:${PATH}"

# Copy SSH keys to docker
# WORKDIR /root
# RUN mkdir -p /root/.ssh
# COPY keys .ssh
# RUN chmod 600 /root/.ssh
# Copy openpose
WORKDIR /openpose
# RUN git clone https://github.com/StevenNguyen050196/openpose

ADD . /openpose

#build it
WORKDIR /openpose/build
RUN cmake -DBUILD_PYTHON=ON .. && make -j8
WORKDIR /openpose

ENV PYTHONPATH="/openpose/build/python":"/openpose/"

RUN pip3 install -r requirements.txt
