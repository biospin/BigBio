Jupyter와 R 연동방법
=====================

# Jupyter 설치
- http://jupyter.org/
- Jupyter는 data scientists, researchers, and analysts 들이 널리 사용되고 있으며 , Jupyter’s notebook은 실행코드와 결과값들, 그래프, 이미지들이 혼재된 인터페이스를 제공하고, reproducible research 와 training을 쉽게 하거나 팀단위 협동에 도움이 됨.
- Jupyter는 python으로 개발된 개발 도구로 하나씩 설치시 어려움이 따르므로, 한번에 전체를 설치해주는 Anaconda를 이용함.
- [윈도우즈용 conda설치파일 - Anaconda2-4.0.0-Windows-x86_64.exe](https://3230d63b5fc54e62148e-c95ac804525aac4b6dba79b00b39d1d3.ssl.cf1.rackcdn.com/Anaconda2-4.0.0-Windows-x86_64.exe)
- Anaconda2-4.0.0-Windows-x86_64.exe 파일은 받고 필히 **관리자 권한**으로 실행시킴

# Jupyer와 R 연동방법
- conda설치후에 커맨트창에서 아래와 같이 명령어를 실행시킴.
```
conda install -c r r-essentials  # 3.1.x   
or 
conda install -c r r=3.3.1
```

# 실행방법 
- 커맨트창에서 아래와 같이 명령어를 실행시킴.
```
jupyter notebook
```

- jupyter.bat 라는 배치파일로 만들어 놓으면 편리함.
```
d:
cd D:/작업디렉토리
jupyter notebook
```