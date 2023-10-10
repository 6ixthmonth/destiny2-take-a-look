# 게임 'Destiny 2' 상인 판매 아이템 조회 및 인공지능 기반 구매 추천 사이트, Destiny 2 - Take A Look

![overview](https://user-images.githubusercontent.com/42332051/232289232-0e53c843-edca-4dd0-9427-dd212386fa8e.png)

*Bungie*의 1인칭 슈팅 온라인 게임 *Destiny 2*에서는 일부 상인들이 특정한 주기마다 임의의 아이템을 판매한다. 이 웹 사이트는 *Bungie.net Platform API*를 사용하여 판매 아이템 정보를 가져와서 데이터베이스에 기록, 조회할 수 있으며, 나아가 인공지능을 기반으로 구매를 추천하는 기능을 제공한다.

---

## 개발 환경

### Python library

- Django
- django-environ
- django-sslserver
- requests-oauthlib

- gunicorn
- psycopg
- mysqlclient

- pandas
- scikit-learn
- tensorflow

### Database

- PostgreSQL
- MySQL

### Service

- Nginx
- AWS LightSail
- AWS RDS
- AWS Route 53

---

## 주요 기능

### 'Destiny 2' 상인 판매 아이템 데이터 수집

- *Bungie.net Platform API*를 통해 OAuth2.0 방식으로 데이터를 가져온다.
- 가져온 데이터를 모델로 가공 처리하여 Django ORM을 통해 연결된 데이터베이스에 저장한다.

### 'Destiny 2' 상인 판매 아이템 조회

- 메인 페이지에 접속하면 데이터베이스에 저장된 데이터를 출력한다.
- 페이징 기능을 제공한다.
- ![filter](https://user-images.githubusercontent.com/42332051/232289667-2dc186c4-ba45-4ce0-8270-ba712a5ae714.png)
- 필터 기능을 통해 원하는 아이템을 골라 조회할 수 있다.

### 인공지능 기반 구매 추천

- 방어구 아이템이 가지는 능력치 값을 분석해서 구매 추천도를 계산한다.
- *Destiny 2*에서 어느 하나의 방어구 아이템은 총 여섯 종류의 능력치를 가지는데, 그중 세 종류는 플레이어 캐릭터의 직업에 따라 선호도가 다르고, 나머지 세 종류는 직업에 상관 없이 선호도가 비슷하다.
- 각각의 학습 모델은 다음과 같은 구조를 가진다.
  - 3개의 뉴런을 가지는 input layer(각각의 능력치에 대응).
  - 200개의 뉴런을 가지는 첫 번째 hidden layer.
  - 500개의 뉴런을 가지는 두 번째 hidden layer.
  - 300개의 뉴런을 가지는 세 번째 hidden layer.
  - 2개의 뉴런을 가지는 output layer(PVE 및 PVP 추천도에 대응).
