# Search price for used apple goods

[당근마켓](https://www.daangn.com/), [중고나라](https://www.joongna.com/), [번개장터](https://m.bunjang.co.kr/)에 게시된 애플 제품을 크롤링하여 시세를 시각화 하고, 사용자에게 원하는 정보를 제공

`NOTE: robots.txt 확인 후 허용된 사이트만 크롤링합니다.`

## Goal

- 약 1TB정도의 데이터를 기반으로 data pipeline 설계 및 제작
- 스토리지에 저장된 데이터를 기술 통계 계산 및 데이터 시각화에 필요한 통계 데이터 생성
- MLlib을 이용한 ML 모델 구축
- github을 통한 소스 형상관리
- Data visualization

## Mission

- 분산 클러스터링을 위한 도커 서버 4대 생성 및 분산 클러스터링 수행
- spark framework를 통한 분산 클러스터링 컴퓨팅 수행
- data pipeline의 design pattern은 특정 소프트웨어 아키텍처 준수
- 데이터 시각화를 위한 기술 통계량 생성 후 스토리지에 저장

## Requirements knowledge

- Knowledge of [Docker](https://www.docker.com/)
- Knowledge of [Apache Spark](http://spark.apache.org/)

## TODO List

- Configure Spark cluster on Docker
- Select Database
  - How to save/inquiry data based on OLAP effectively?
  - What kind of way for saving data? streamming? batch?
  - Table structural design for historical data

## History

- 2021.04.06 - Start project with [JaeHun Hur](https://github.com/koni114)
- 2021.04.07 - Join [DongHoon Kang](https://github.com/donghoon-khan)
- 2021.04.07 - Join [taeWoong Kim](https://github.com/poi2507)
- 2021.04.08 - Join [sohee Han](https://github.com/sohee53)