# MongoDB 설치하기
## Mac
### 1. download & install
- Mac의 경우, Homebrew를 사용하여 install을 할 수 있었지만, <b>현재 mongodb 설치를 지원하지 않습니다</b>
- 따라서 아래 커맨드 명령어가 되지 않는 경우는 직접 mongodb를 설치해야 합니다.
~~~shell
$ brew update && brew install mongodb
$ mongo -version
~~~
#### 설치파일 다운로드 받기
- 먼저 다음의 링크로 접속합니다.  
  [mongoDB 다운로드](https://www.mongodb.com/try/download/community)  
- MongoDB Community Server에 접속하고 다음을 선택해 줍니다
  - <b>Server를 선택</b> 
  - <b>Version(Current release. 2021.04.06 기준 4.4.4)</b>
  - <b>OS: macOS x64</b>
  - <b>Package: TGZ</b>  

![img](https://github.com/koni114/Toy-Project-01/blob/master/img/mongoDB_03.JPG)

#### 설치하기
- 터미널을 열어줍니다
- 다운로드 파일이 있는 곳으로 이동합니다
- 이동했을 때 권한 허가 관련 팝업창이 뜬다면 OK를 눌러줍니다
~~~shell
$ cd downloads
~~~
- 다운로드 받은 tgz 파일을 아래의 명령어로 압축을 풀어줍니다
~~~shell
$ tar xvfz mongodb-macos-x86_64-4.4.4.tgz
~~~
- 그러면 Download 디렉터리에 mongodb-macos-x86_64-4.4.4이 생성됩니다
- 이 디렉터리를 /usr/local/mongodb 위치로 이동시켜줍니다.
- password을 입력하라고 한다면, booting password를 입력해 주면 됩니다.
~~~shell
$ sudo mv mongodb-osx-x86-64_4.2.0 /usr/local/mongodb
~~~

### 2. /data/db 폴더 만들기
- db를 관리하고자 하는 디렉터리로 이동합니다

~~~shell
$ cd ~
~~~
~~~shell
$ sudo mkdir -p data/db
~~~
- 만들어준 디렉터리는 다음 명령어로 권한을 변경하여 줍니다
~~~shell
$ sudo chmod 776 ./data/db
~~~
- 변경된 권한을 확인해 줍니다
~~~shell
$ ls -al
~~~

### 3. MongoDB 환경변수 Path 설정하기
- 터미널을 열고 명령어를 사용하여 vi 편집기로 bash_profile을 열어 줍니다  

![img](https://github.com/koni114/Toy-Project-01/blob/master/img/mongoDB_04.JPG)
- 여기에 맨 아래에 다음의 두줄을 입력해 줍니다
- 위의 이미지에서는 제가 이미 입력했기 때문에 보입니다(^^)
~~~shell
export MONGO_PATH=/usr/local/mongodb
export PATH=$PATH:$MONGO_PATH/bin
~~~
- 입력하는 방법은 bash_profile에 들어간 상태에서 i를 누르면 INSERT 상태로 들어갑니다
- 두줄을 입력해 준 뒤, `:wq` 를 입력해주면 정상적으로 빠져나오게 됩니다
- 변경한 정보를 반영하기 위하여 다음의 명령어를 마지막으로 입력해 줍니다
~~~shell 
$ source ~/.bash_profile
~~~

### 4. 제대로 설치가 되었는지 확인하기
- 아래 명령어를 통해 정상적으로 버전이 나오는지 확인합니다
- 만약 '확인되지 않는 개발자의 앱 열기'가 나타난다면 [다음의 블로그](https://support.clo3d.com/hc/ko/articles/115005385707--Mac-%ED%99%95%EC%9D%B8%EB%90%98%EC%A7%80-%EC%95%8A%EC%9D%80-%EA%B0%9C%EB%B0%9C%EC%9E%90%EC%9D%98-%EC%95%B1%EC%97%B4%EA%B8%B0-%ED%95%B4%EA%B2%B0-%EB%B0%A9%EB%B2%95)를 참조해 주세요
~~~shell
$ mongo -version
~~~
- 정상적이라면, 다음과 같은 화면이 나타날 것입니다

![img](https://github.com/koni114/Toy-Project-01/blob/master/img/mongoDB_05.JPG)

### 5. 서버 / 클라이언트 실행
- 먼저 아래의 명령어를 사용하여 서버를 실행시킵니다
~~~shell
$ mongod
~~~
- 다음과 같이 나오면 정상입니다.(shell이 자동으로 빠져나와진다면, 문제가 발생한 것입니다) 

![img](https://github.com/koni114/Toy-Project-01/blob/master/img/mongoDB_06.JPG)


- 그 다음 새로운 터미널을 열어 아래의 명령어를 실행하여 클라이언트를 실행시켜 봅니다
- 만약 <b>command not found: mongo</b>라고 뜬다면, .bash_profile을 실행시켜 줍니다
~~~shell
$ source ~/.bash_profile
~~~
~~~shell
$ mongo
~~~
- 다음과 같이 뜨면 정상입니다  

![img](https://github.com/koni114/Toy-Project-01/blob/master/img/mongoDB_07.JPG)


## 참고사항
### Data directory /data/db not found 에러
- mongod 실행시 다음과 같은 Error 발생
~~~
$ mongod
...
"error":"NonExistentPath: Data directory /data/db not found. Create the missing directory or specify another path using (1) the --dbpath command line option, or (2) by adding the 'storage.dbPath' option in the configuration file."
...
~~~
- root directory로 넘어가 /data/db 디렉토리 생성을 시도했으나, 아래 문구가 뜨면서 실패하였다
~~~
$ sudo mkdir -p /data/db
mkdir: /data/db: Read-only file system
~~~
- 다음의 에러는 <b>Mac Catalina(10.15이상)</b> 부터는 root폴더에 Writing이 불가능해졌다고 함
- 디렉토리 설정을 다르게 하여 실행해야 함!
~~~
$ mkdir -p ./data/db
$ mongod --dbpath=/Users/{username}/data/db
~~~