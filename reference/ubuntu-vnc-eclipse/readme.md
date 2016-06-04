
# 우분투에서 하둡 mapreduce 개발환경 만들기


## Docker에 VNC와 이클립스 설치

- 주의) 모든 환경을 설정하고 도커를 commit할때 에러가 계속 발생해서 설정이 다 날아갔음. 
- 주의) 그냥 virtualbox에서 우분투에서 하는것이 좋을것 같음.
- 주의) 용자여~~  몇시간을 낭비할 생각하고 아래와 같이 해보자..
- 주의) 운이 좋으면 잘 되겠지..~~~



- https://hub.docker.com/r/kaixhin/vnc/  이것을 이용함.
- kaixhin/vnc  Docker 이미지 설치 및 실행
- VNC의 디폴트 패스워드는 password,  변경도 가능함.
```
docker pull kaixhin/vnc
docker run -d -p 5901:5901 kaixhin/vnc
```

- TightVNC 클라이언트 설치 
```
http://www.tightvnc.com/download/2.7.10/tightvnc-2.7.10-setup-64bit.msi
```

- TightVNC 서버는 설치하지 말고 클라이언트만 설치후에 실행
- remote server : 192.168.xxx.xxx:5901

## VNC로 Docker 내부로 접속해서 설정하기
- virtualbox의 우분투에서도 이와 동일하게 설정함.


- 자바, 이클립스, git, wget 설치하기
```
apt-get install wget git openjdk-7-jdk  eclipse  -y
```

- Maven 설치( 의존성 관리 및 빌드도구 )
```
cd ~/
wget  https://archive.apache.org/dist/maven/maven-3/3.2.5/binaries/apache-maven-3.2.5-bin.tar.gz
tar xvf apache-maven-3.2.5-bin.tar.gz

cat <<EOT >> ~/.bashrc
JAVA_HOME=/usr/lib/jvm/java-7-openjdk-amd64
MAVEN_HOME=/root/apache-maven-3.2.5

export PATH=$JAVA_HOME/bin:$MAVEN_HOME/bin:$PATH
EOT

source ~/.bashrc
```

- 예제소스 받기
```
cd ~/

git clone https://github.com/mahmoudparsian/data-algorithms-book/
```
