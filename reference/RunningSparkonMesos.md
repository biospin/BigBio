
# Running Spark on Mesos

# Mesos 설치

## Debian / Ubuntu에 설치

- 참고 : https://open.mesosphere.com/getting-started/install/

> sudo add-apt-repository ppa:webupd8team/java

> sudo apt-get -y update

> sudo apt-get install  -y  oracle-java8-installer

> sudo apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv E56151BF

> DISTRO=$(lsb_release -is | tr '[:upper:]' '[:lower:]')

> CODENAME=$(lsb_release -cs)

> echo "deb http://repos.mesosphere.com/${DISTRO} ${CODENAME} main" | sudo tee /etc/apt/sources.list.d/mesosphere.list

> sudo apt-get -y update

> sudo apt-get -y install mesos marathon

## Zookeeper 구동

- vi /etc/zookeeper/conf/myid

- vi /etc/zookeeper/conf/zoo.cfg
```
server.1=darwin:2888:3888
server.2=babelpish:2888:3888
server.3=psygrammer:2888:3888
```

> sudo service zookeeper restart

- vi /etc/mesos/zk
```
zk://darwin:2181,babelpish:2181,psygrammer:2181/mesos
```

- vi /etc/mesos-master/quorum
```
1
```



## Mesos Cluster 구동

### Master 구동 

> sudo service mesos-master restart

> sudo service marathon restart

### Slave  구동 

> sudo service mesos-slave restart


## 도커 설치

- 메인서버에만.

> sudo apt-get update -y

> sudo apt-get install apt-transport-https ca-certificates  -y

> sudo apt-key adv --keyserver hkp://p80.pool.sks-keyservers.net:80 --recv-keys 58118E89F3A912897C070ADBF76221572C52609D

- vi /etc/apt/sources.list.d/docker.list
```
deb https://apt.dockerproject.org/repo ubuntu-trusty main
```

> sudo apt-get update -y

> sudo apt-get purge lxc-docker -y

> apt-cache policy docker-engine

> sudo apt-get update -y

> sudo apt-get install linux-image-extra-$(uname -r) -y

> sudo apt-get install docker-engine -y

> sudo service docker start

### Adjust memory and swap accounting 

vi /etc/default/grub
```
GRUB_CMDLINE_LINUX="cgroup_enable=memory swapaccount=1"
```

## docker-stacks/all-spark-notebook  설치 

- 참고 : https://github.com/jupyter/docker-stacks/tree/master/all-spark-notebook

> sudo docker pull jupyter/all-spark-notebook

### Connecting to a Spark Cluster on Mesos

- Configure each mesos slave with the [--no-switch_user](https://open.mesosphere.com/reference/mesos-slave/) flag or create the jovyan user on every slave node.
- Run the Docker container with --net=host in a location that is network addressable by all of your Spark workers

> docker run -it --rm  -p 8888:8888 --net=host --pid=host -e TINI_SUBREAPER=true jupyter/all-spark-notebook



