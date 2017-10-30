MicroBot
===================


Open API for Microbot.

----------


Enviroment
-------------
- **Raspbian**: [Download](https://www.raspberrypi.org/downloads/raspbian/)
- **Python 3.5**
- **pip3**

> **Note:**
> - Recommend to Download **RASPBIAN STRETCH LITE** version
> - Python3 is now built-in in Raspbian


Installation
-------------
#### <i class="icon-file"></i> Copy Raspbian to MicroSD Card

[Use Etcher.](https://etcher.io/)
 You can use this tool whatever your operation system is. (eg. Windows, MacOS, Linux)

![Tuto](https://etcher.io/static/screenshot.gif)

#### <i class="icon-pencil"></i> Setting Raspbian
You have to change default Hostname, Password, Timezone.
```bash
$ sudo raspi-config
```

#### <i class="icon-folder-open"></i> Install Dependencies
```bash
$ sudo apt-get install -y python3-pip git-core
$ sudo pip3 install requests Beautifulsoup4
```

#### <i class="icon-refresh"></i> Get Source

```bash
$ git clone https://github.com/robincloud/microbot.git ~/Microbot
```

----------


Specification
-------------------

**HTTP GET**

JSON Type
|Field Name       | Type       | EXP|
|-----------------|------------|----------|
|id               |  string    | 상품 아이디|
|mid              |  string    | 상품 mid|


----------

**HTTP POST**

JSON Type
|Field Name       | Type       | EXP|
|-----------------|------------|----------|
|id               |  string    | 상품 아이디|
|mid              |  string    | 상품 mid|
|data             |  list      | 크롤링한 데이터|

data field
Dict Type
|Field Name       | Type       | EXP|
|-----------------|------------|----------|
|id               |  string    | 상품 아이디|
|mid              |  string    | 상품 mid|
|pkey             |  int       | 옵션에 대한 고유값|
|cat              |  string    | 카테고리|
|count            |  int       | 판매몰 수|
|item_name        |  string    | 상품명|
|option_name      |  string    | 옵션명|
|nods             |  list      | 판매몰에대한 정보|

nods field
Dict Type
|Field Name       | Type       | EXP|
|-----------------|------------|----------|
|id               |  string    | 판매몰 아이디|
|name             |  string    | 판매몰 상품명|
|mall             |  string    | 판매몰 업체명|
|price            |  int       | 판매몰에서 올린 가격|
|delivery         |  int       | 판매몰의 배송비|
|npay             |  int       | 네이버 패이 지원여부<br>0: False, 1: True|
