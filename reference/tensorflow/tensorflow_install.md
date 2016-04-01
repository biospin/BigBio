
# 텐서플로우 - 분산버전 설치

## 우분투에 docker 설치

sudo apt-get update -y
sudo apt-get install curl -y
curl -fsSL https://get.docker.com/ | sh
curl -fsSL https://get.docker.com/gpg | sudo apt-key add -

## 이미지 저장 위치를 /home/docker로 변경
sudo vi /etc/default/docker
DOCKER_OPTS="-dns 8.8.8.8 -dns 8.8.4.4 -g /home/docker

sudo stop docker
tar -zcC /var/lib docker > /home/var_lib_docker-backup-$(date +%s).tar.gz
sudo mv /var/lib/docker /home/docker
sudo start docker
docker info  # 확인

# docker에 텐서플로우용 이미지 만들기
Dockerfile을 작업위치에 만들고 내용을 넣어줌.
```
FROM ubuntu:14.04
MAINTAINER YONGI JI <braveji@hanmail.net>

RUN apt-get update && apt-get install -y openssh-server
RUN mkdir /var/run/sshd
RUN echo 'root:bigbio' | chpasswd
RUN sed -i 's/PermitRootLogin without-password/PermitRootLogin yes/' /etc/ssh/sshd_config

# SSH login fix. Otherwise user is kicked off after login
RUN sed 's@session\s*required\s*pam_loginuid.so@session optional pam_loginuid.so@g' -i /etc/pam.d/sshd

ENV NOTVISIBLE "in users profile"
RUN echo "export VISIBLE=now" >> /etc/profile

EXPOSE 22
CMD ["/usr/sbin/sshd", "-D"]

ENTRYPOINT service ssh restart && bash
```
 
docker build -t unbuntu/bigbio   . 
docker run -i -t  -p 1022:22 --name bigbio unbuntu/bigbio /bin/bash 


 
# 텐서플로우 설치

## 준비
sudo apt-get update -y
sudo apt-get install git python-numpy swig python-dev libc6-dev g++ zlib1g-dev unzip -y
sudo apt-get install software-properties-common python-software-properties -y


## Installation for Linux

### Install Bazel

http://bazel.io/docs/install.html

sudo add-apt-repository ppa:webupd8team/java
sudo apt-get -y update
sudo apt-get -y install oracle-java8-installer

wget https://github.com/bazelbuild/bazel/releases/download/0.2.0/bazel-0.2.0-installer-linux-x86_64.sh
chmod +x bazel-0.2.0-installer-linux-x86_64.sh
./bazel-0.2.0-installer-linux-x86_64.sh --user
vi ~/.bashrc 
export PATH="$PATH:$HOME/bin"

source ~/.bashrc 


### Installing from sources
git clone --recurse-submodules https://github.com/tensorflow/tensorflow

### Configure the installation
cd ./tensorflow
./configure

### 단일버전 설치 빌드
bazel build -c opt  //tensorflow/cc:tutorials_example_trainer ## CPU
bazel build -c opt --config=cuda //tensorflow/cc:tutorials_example_trainer ## GPU

bazel-bin/tensorflow/cc/tutorials_example_trainer ## test 


### 분산버전 설치 빌드

http://qiita.com/ashitani/items/2e48729e78a9f77f9790

bazel build --jobs 2 -c opt //tensorflow/core/distributed_runtime/rpc:grpc_tensorflow_server
