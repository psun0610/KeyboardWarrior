# 키보드워리어

> 키보드 중고 거래, 사용자 맞춤형 키보드 추천 서비스, 검색 서비스, 키보드 후기 제공 해주는 사이트

![logo](https://user-images.githubusercontent.com/97274144/203568268-5300330b-7be5-48c7-9d93-98cfc596ed82.jpg)

# Contributor

<div style="display:flex; justify-content:center;">
<a href="https://github.com/caretim"><img src="https://avatars.githubusercontent.com/u/108650777?v=4" style="border-radius: 50%;" width="150" height="150"/></a>
<a href="https://github.com/yoosoonil"><img src="https://avatars.githubusercontent.com/u/97111793?v=4" style="border-radius: 50%;" width="150" height="150"/></a>
<a href="https://github.com/tenedict"><img src="https://avatars.githubusercontent.com/u/108652767?v=4" style="border-radius: 50%;" width="150" height="150"/></a>
<a href="https://github.com/psun0610"><img src="https://avatars.githubusercontent.com/u/97274144?v=4" style="border-radius: 50%;" width="150" height="150"/></a>
<a href="https://github.com/HYUNSIK-JI"><img src="https://avatars.githubusercontent.com/u/59475851?v=4" style="border-radius: 50%;" width="150" height="150"/></a>
</div>


&nbsp;

# 프로젝트 소개

- 🗓**프로젝트 기간**
  - 2022.11.09 (수) ~ 2022.11.21 (월)
- 💻**사용 기술**
  - ![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54) ![Django](https://img.shields.io/badge/django-%23092E20.svg?style=for-the-badge&logo=django&logoColor=white) ![HTML5](https://img.shields.io/badge/html5-%23E34F26.svg?style=for-the-badge&logo=html5&logoColor=white)![CSS3](https://img.shields.io/badge/css3-%231572B6.svg?style=for-the-badge&logo=css3&logoColor=white) ![JavaScript](https://img.shields.io/badge/javascript-%23323330.svg?style=for-the-badge&logo=javascript&logoColor=%23F7DF1E) ![Bootstrap](https://img.shields.io/badge/bootstrap-%23563D7C.svg?style=for-the-badge&logo=bootstrap&logoColor=white) ![Selenium](https://img.shields.io/badge/-selenium-%43B02A?style=for-the-badge&logo=selenium&logoColor=white) Beautifulsoup4
- ⭐**개발 역할 분담**
  - 팀장: 하승찬/ 발표자: 유순일/ PPT 제작자: 박선영, 문재윤, 지현식
  - **백엔드**: 지현식, 하승찬, 유순일
  - **프론트엔드**: 박선영, 문재윤

&nbsp;
- 프로젝트시 팀원들과의 규칙
1. 커밋 메세지는 앱이름:개발내용  한글로 작성한다.
    - articles: 메인 페이지 구현
2. 브랜치 기능이름 앱이름/기능  
    - accounts/login 
3. 하는 동안 팀원 모두 디스코드 화면공유 켜놓기
4. 템플릿 css 단위는 웬만하면 px 사용 (이유: 나중에 제가 조금씩 고칠 경우가 있을 것으로 예상돼서)

# 🚩목적

Django를 통해 

내가 이 기능에 어떻게 접근, 그 과정에서 이슈들을 해결
ex) 무한스크롤, 레디스 소켓 사용

&nbsp;

# 모델 구조, ERD 작성
![키보드워리어 최종 ERD](https://user-images.githubusercontent.com/97111793/203498672-67c14351-a903-4e81-95e2-619f43b4203d.png)

## app별 모델

<details>
<summary>accounts app</summary>

**class User:**
 - naver_id = models.CharField(null=True, unique=True, max_length=100)
 - goo_id = models.CharField(null=True, unique=True, max_length=50)
 - followings = models.ManyToManyField("self", symmetrical=False, related_name="followers")
 - press = MultiSelectField(choices=Key_Press, null=True)
 - weight = MultiSelectField(choices=Weight, null=True)
 - array = MultiSelectField(choices=Array, null=True)
 - sound = MultiSelectField(choices=Sound, null=True)
 - rank = models.IntegerField(default=0)
 - connect = MultiSelectField(choices=connect, null=True)
 - image = ProcessedImageField(blank=True, processors=[Thumbnail(300, 300)], format="jpeg", options={"quality": 90})
 - is_social = models.IntegerField(default=0)

**class Notification:**
 - message = models.CharField(max_length=100)
 - check = models.BooleanField(default=False)
 - user = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE)
 - category = models.CharField(max_length=10)
 - nid = models.IntegerField(default=0)

</details>

<details>
<summary>articles app</summary>

**class Keyboard:**
 - name = models.CharField(max_length=80, blank=True)
 - img = models.CharField(max_length=300, blank=True)
 - brand = models.CharField(max_length=50, blank=True)
 - connect = models.CharField(max_length=50, blank=True)
 - array = models.CharField(max_length=50, blank=True)
 - switch = models.CharField(max_length=50, blank=True)
 - key_switch = models.CharField(max_length=50, blank=True)
 - press = models.IntegerField(blank=True)
 - weight = models.CharField(max_length=50, blank=True)
 - kind = models.CharField(max_length=50, blank=True)
 - bluetooth = models.CharField(max_length=50, blank=True)

**class Visit:**
 - visit_date = models.CharField(max_length=30)
 - visit_count = models.IntegerField(default=0)

</details>

<details>
<summary>reviews app</summary>

**class Reviews:**
 - user = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE)
 - title = models.CharField(max_length=80)
 - content = models.TextField(max_length=500)
 - grade = models.IntegerField(choices=grade_)
 - like_users = models.ManyToManyField(AUTH_USER_MODEL, related_name="like_review")
 - created_at = models.DateTimeField(auto_now_add=True)
 - updated_at = models.DateTimeField(auto_now=True)
 - hits = models.PositiveIntegerField(default=0, verbose_name="조회수")
 - bookmark_users = models.ManyToManyField(AUTH_USER_MODEL, related_name="bookmark_reivew")
 - keyboard = models.ForeignKey(Keyboard, on_delete=models.CASCADE)

**class Photo:**
 - review = models.ForeignKey(Review, on_delete=models.CASCADE)
 - image = models.ImageField(upload_to="images/", blank=True)

**class Comment:**
 - content = models.CharField(max_length=80)
 - user = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE)
 - review = models.ForeignKey(Review, on_delete=models.CASCADE)
 - created_at = models.DateTimeField(auto_now_add=True)
 - updated_at = models.DateTimeField(auto_now=True)
 - like_users = models.ManyToManyField(AUTH_USER_MODEL, related_name="like_comment")

</details>

<details>
<summary>trade app</summary>

**class Trades:**
 - user = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE)
    Trade_type = models.IntegerField(choices=tradeType)
 - title = models.CharField(max_length=80)
 - content = models.TextField(max_length=500)
 - keyboard = models.ForeignKey(Keyboard, on_delete=models.CASCADE)
 - price = models.IntegerField(default=0)
 - marker = models.ManyToManyField(
        AUTH_USER_MODEL, symmetrical=False, related_name="jjim"
    )
 - status_type = models.IntegerField(choices=statusType, default=1)

**class Photo:**
 - trade = models.ForeignKey(Trades, on_delete=models.CASCADE)
 - image = models.ImageField(upload_to="images/", blank=True)

**class Trade_Comment:**
 - user = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE)
 - trade = models.ForeignKey(Trades, on_delete=models.CASCADE)
 - content = models.CharField(max_length=100)
 - create_at = models.DateTimeField(auto_now_add=True)

</details>

&nbsp;&nbsp;

# 🧾기능 소개

## 제품 정보 수집

- Selenium, BeautifulSoup4를 이용하여 `다나와` 페이지 크롤링

&nbsp;

## Articles/main
- 게시글에 댓글이 달릴 때, 채팅이 올 때 알림 기능
- 전체 방문자 수, 오늘 방문자 수 표시
![articles_main(알림,방문자수)-min](https://user-images.githubusercontent.com/108650777/203498719-73da91bd-bc40-40d6-8747-ae6ee5819746.gif)

- 사용자 맞춤형 키보드 추천
  - 사용자가 회원가입시 입력한 정보를 기반으로 키보드를 추천하는 기능
  ![키보드추천](https://user-images.githubusercontent.com/108650777/203497876-23d077cb-d4da-4428-8814-a0ae4e15485f.gif)

&nbsp;

## Articles/all

- 비동기 무한 스크롤
- 비동기 키보드 필터링
- 비동기 키보드 검색 기능
![aritcles_all](https://user-images.githubusercontent.com/108650777/203497932-65b5749c-9ee2-4e11-8106-1d6f6586f04f.gif)

&nbsp;

## Articles/detail 

- 키보드 후기 평균 별점을 보여줌
- 댓글 욕설 필터링
![articles_detail (1)](https://user-images.githubusercontent.com/108650777/203498069-165cb150-b14a-46d0-bfe3-1b82496fff57.gif)

&nbsp;

## Trade/index

- 키보드 이름, 리뷰 제목 검색 기능
- 라디오 버튼을 통해 판매글만, 구매글만 선택 가능
- 키보드, 판매글 검색
![trade_index-min](https://user-images.githubusercontent.com/108650777/203499220-65e889b3-aa1b-4c54-8c31-dbc849b8a0ab.gif)

&nbsp;

## Trade/detail

- 비동기 게시글 찜하기
- 비동기 댓글 생성 및 삭제
- 게시글 사진 여러 장
- 채팅 (비동기 채팅, DB저장)
![trade_detail](https://user-images.githubusercontent.com/108650777/203499830-7b8cb0f3-20e4-4aae-9756-c8e91599d9c8.gif)

&nbsp;

## Trade/create

- 등록된 키보드 모델명 검색
- 사진 여러 장 추가 가능
  ![trade_create](https://user-images.githubusercontent.com/108650777/203498331-c31b9a0c-4e5a-4d5b-abf2-80b8263b2067.gif)

&nbsp;

## Reviews/index
![reviews_index](https://user-images.githubusercontent.com/108650777/203577486-0b31951a-fb44-4faf-bdb2-41a0ed6e4d18.gif)

- 후기글, 키보드 검색 기능

&nbsp;


## Reviews/detail

- 비동기 글 좋아요
- 비동기 댓글 생성 및 삭제
- 비동기 댓글 좋아요
- 댓글 욕설 필터링
  ![reviews_detail-min](https://user-images.githubusercontent.com/108650777/203500064-3c043c2a-af19-4d2b-83e8-d30cc648d101.gif)



&nbsp;

## Reviews/create

- 등록된 키보드 모델명 검색
- 별점 기능
- 이미지 여러 개 등록 가능
- ![reviews_create](https://user-images.githubusercontent.com/108650777/203500675-05282a42-8cf0-4a32-84ea-f3f28fdf5eaf.gif)

&nbsp;

## Accounts/signup, login

![accounts_signup](https://user-images.githubusercontent.com/97111793/203580708-d367f2dd-4302-4753-8954-072b2465f1b3.gif)

### Accounts/signup, login

- 소셜 계정 로그인
- 로그인 시 선호 키보드 정보 가져오기

&nbsp;

## Accounts/detail
- 라디오 버튼 메뉴
- 컬렉션 모달로 띄움
- 비동기 팔로우
  ![accounts_detail](https://user-images.githubusercontent.com/108650777/203498275-89efa132-36ab-44e0-bc30-99fe4c86685e.gif)

&nbsp;

## Chat

- 로컬에서 레디스를 사용하여 채팅 기능 구현
- 배포 후 서버에서는 레디스 채팅 배포 실패
- => 비동기로 1초마다 새로고침하여 반실시간으로 채팅 구현

![chat](https://user-images.githubusercontent.com/108650777/203498212-d7c228ae-2e7c-451d-827a-1697f541c8b7.gif)
![chat1](https://user-images.githubusercontent.com/108652767/203585681-b31a84b7-74b8-467a-9c0e-a65867313570.gif)


13. 기타 중요기능
알림기능


14. 이슈 
  

  <details>

<summary>1.셀레니움 비동기 pagenation 크롤링 이슈</summary>

  다나와에서 제품 크롤링 시, pagenation에서의 비동기로 인해 다음페이지 url을 받아오지 못해 다음페이지의 제품리스트를 크롤링 할 수 없었다. 그래서 한 페이지에 대해서만 크롤링을 반복해서 수행하였다.

![Untitled](https://s3-us-west-2.amazonaws.com/secure.notion-static.com/93f02441-5339-45a7-abda-e8636cfcd34b/Untitled.png)



[[Crawling] 다나와(danawa) 제품 리스트 크롤링](https://ysyblog.tistory.com/58)

[[파이썬] selenium 크롤링, 데이터 수집 ID, TAG, href 찾기](https://hellodoor.tistory.com/148)

[WWW.PHPSCHOOL.COM](https://www.phpschool.com/gnuboard4/bbs/board.php?bo_table=qna_html&wr_id=168862)

### 해결 방법

  다음 페이지로 넘어가는 해결법은 찾지 못했다. 다만, 다나와 사이트에서 의도적으로 크롤링을 막기위해, pagenav탭에서 a태그의 `href` 을 `href='#'` 으로 작성한 것으로 추측된다. `href='#'` 작성하면 a태그 클릭 시, 다음페이지로 넘어가지 못하고 최상단으로 올라가게 된다. 그래서 같은 페이지만 계속 반복하게 되고, 긁어오는 데이터가 반복될 수 밖에 없다.
</details>

<details>

<summary>2.셀레니움 형제 요소 찾기 / 테이블 추출</summary>

  

![Untitled](https://s3-us-west-2.amazonaws.com/secure.notion-static.com/e34e86d4-083f-4f91-8f32-f9faa1320a7f/Untitled.png)

![Untitled](https://s3-us-west-2.amazonaws.com/secure.notion-static.com/802f6010-f75a-41a5-a653-d1405c354cb1/Untitled.png)

```python
# url 리스트 만들기
url_list = []
for li in product_li_tags:
    url_list.append(li.select_one('p.prod_name a').get('href'))

for sub_url in url_list:
    driver.get(sub_url)
    time.sleep(0.5)
    name = driver.find_element(By.CSS_SELECTOR, '.prod_tit>.title').text.strip()
    img_link = driver.find_element(By.CSS_SELECTOR, '.photo_w img').get_attribute('src')
    print(name, img_link)
    # 상세정보 클릭
    driver.find_element(By.CSS_SELECTOR, '#bookmark_product_information_item').click()
    time.sleep(0.5)
    # 키압, 무게, 배열, 소리, 브랜드, 축
    spec_table = driver.find_elements(By.XPATH, '//*[@id="productDescriptionArea"]/div/div[1]/table/tbody')
    brand, keys, connet = '', '', ''
    for specs in spec_table:
        ths = specs.find_elements(By.XPATH, '/tr[1]/th[1]')
        for th in ths:
            if th.text == '제조회사':
                try:
                    # brand = th.find_element(By.CSS_SELECTOR, '+td').text
                    # brand = th.find_elements(By.CSS_SELECTOR, '~td').text
                    
                    brand = th.find_element(By.XPATH, '/following-sibling::*').text
                except:
                    brand = th.find_element(By.XPATH, '/following-sibling::*/a').text
                print(brand)

            # elif th.find_elements(By.CSS_SELECTOR, 'a').text == '키 배열':
            #     try:
            #         keys = th.find_element(By.CSS_SELECTOR, '+td').text
            #     except:
            #         th.find_element(By.CSS_SELECTOR, '+td a').text

            # elif th.find_elements(By.CSS_SELECTOR, 'a').text == '연결 방식':
            #     connet = th.find_element(By.CSS_SELECTOR, '+td a').text
    print(brand, keys, connet)
```

다나와 사이트를 크롤링을 하면서 문제가 발생하였다.

테이블 `tr` 에서 `th` 값을 찾은 다음, 형제 요소인 `td`를 찾아서 그에 대한 text 값을 찾으려고 했다.

처음에는 `CSS_SELECTOR` 로 인접 형제 선택자인 `+td` 를 사용해보았는데 값을 찾지 못했다.

두번째 시도는 `XPATH`를 이용했다. `following-sibling::*` 을 사용하였더니 요소 자체는 선택을 잘 했지만 print되는 값이 없었다. (아직 이 이유는 알 수 없음)

### 참고 자료


⭐컨트리뷰터: 7조 이태극⭐

[XPATH란? 셀레니움(Sellenium) XPath로 쉽게 요소 선택하기!](https://aplab.tistory.com/entry/XPATH%EB%9E%80-%EC%85%80%EB%A0%88%EB%8B%88%EC%9B%80Sellenium-XPath%EB%A1%9C-%EC%89%BD%EA%B2%8C-%EC%9A%94%EC%86%8C-%EC%84%A0%ED%83%9D%ED%95%98%EA%B8%B0)

[XPath Contains, Following Sibling, Ancestor & Selenium AND/OR](https://www.guru99.com/using-contains-sbiling-ancestor-to-find-element-in-selenium.html)

### 해결 방법

```python
# url 리스트 만들기
url_list = []
for li in product_li_tags:
    url_list.append(li.select_one('p.prod_name a').get('href'))

for sub_url in url_list:
    driver.get(sub_url)
    time.sleep(0.5)
    name = driver.find_element(By.CSS_SELECTOR, '.prod_tit>.title').text.strip()
    img_link = driver.find_element(By.CSS_SELECTOR, '.photo_w img').get_attribute('src')
    print(name, img_link)
    # 상세정보 클릭
    driver.find_element(By.CSS_SELECTOR, '#bookmark_product_information_item').click()
    time.sleep(0.5)
    # 키압, 무게, 배열, 소리, 브랜드, 축
    spec_table = driver.find_element(By.CSS_SELECTOR, ".spec_tbl tbody").text
    brand, keys, connet = '', '', ''
    print(spec_table)
```

  해결 방법은 아주아주 간단했다😥 그냥 `table`의 `tbody` 자체에서 text를 뽑으면 되는 것이었다…

  ![Untitled](https://s3-us-west-2.amazonaws.com/secure.notion-static.com/1591e2f5-d884-4201-845a-068b02882dfb/Untitled.png)

  결과가 아주아주 잘 뽑히는 것을 볼 수 있었다 ㅠㅠ

  나는 원래 뽑을 때부터 내가 원하는 것만 뽑고 싶다는 생각으로 위와 같이 코드를 짰었는데

  그렇게 하는 것도 좋긴 하지만 아예 문자열을 모두 가져와서 문자열을 조작하는 것이 더 쉬울 수도 있겠구나 생각했다

</details>



<details>

<summary>3.KMP 알고리즘을 이용한 비속어 텍스트 찾기 이슈</summary>


  텍스트 내에 해당 문자열이 존재 유무 찾기에 대한 시간복잡도 이슈


  ### 해결 방법

❗ KMP 알고리즘으로 시간복잡도 이슈 해결



```python

def maketable(p):
	table = [0] * len(p)
	i = 0
	for j in range(1, len(p)):
		while i > 0 and p[i] != p[j]:
			i = table[i - 1]
		if p[i] == p[j]:
			i += 1
			table[j] = i
	return table
def KMP(p, t):
	ans = []
	table = maketable(p)

	i = 0
	for j in range(len(t)):
		while i > 0 and p[i] != t[j]:
			i = table[i - 1]
		if p[i] == t[j]:
			if i == len(p) - 1:
				ans.append(j - len(p) + 2)
				i = table[i]
			else:
				i += 1
	return ans
```

KMP 알고리즘을 활용한 해결.


</details>

<details>

<summary>4.크롤링 데이터 정제 작업 이슈</summary>

  
  ### 이슈 내용



처음에는 데이터 크롤링 할 때 데이터를 가져오고 정제하고 ORM으로 데이터를 삽입하는 것을 하나의 파이썬 파일 안에서 끝내는 것이 더 좋을 것이라고 생각했었다.

비모쌤이 말씀해주셨는데 `JSON` 파일로 만든 후, 정제하고, 마지막에 쿼리문으로 데이터를 삽입하는 세 과정으로 나누어서 하면 시간을 더 효율적으로 쓸 수 있다고 하셨다.

왜 그런지 생각해보니까 데이터를 가져오는 작업은 셀레니움 특성상 데이터가 많아질 수록 오래걸릴 수 밖에 없다. 그런데 이런식으로 한 파일에 모든 작업을 하려고 하면, 파일에 오타라도 있다면 제일 처음으로 돌아가서 다시 데이터를 가져오는 작업을 해야한다. 우리는 데이터를 가져오고 나서 `.replace` 로 모든 예외사항과 이상한 구문이 붙은 데이터들을 처리중이었는데 만약 우리가 예상하지 못한 이상한 데이터가 생긴다면 그 데이터를 처리하는 구문도 추가한 후 다시 데이터를 가져오는 것부터 시작했다.

그래서 정제하는 작업은 이미 끝나서 세 과정으로 나누진 못했지만 정제 후 바로 DB에 저장하지 않고 `JSON`파일로 저장하였다.

저장한 `JSON` 파일은 검토 완료 후 DB에 넣는 작업인 `loaddata` 를 해줬다. 이렇게 하니 시간이 엄청나게 단축되었다. 다음에 크롤링 할 때에는 꼭 과정을 쪼개서 해봐야겠다.

### 참고 자료


[코드공부방](https://code-study.tistory.com/58)


</details>

<details>

<summary> 5.Django/SQLite DB에 크롤링한 데이터를 넣을 때 JSON 작성 형식</summary>

 
  ```json
[
	{
			"name": "레오폴드 FC980C 영문 화이트 (30g, 균등)",
			"img": "https://img.danawa.com/prod_img/500000/167/670/img/7670167_1.jpg?shrink=500:500&_v=20200107112457",
			"brand": "레오폴드",
			"connect": "무접점(정전용량)",
			"weight": "1100g",
			"array": "98",
			"switch": "Topre",
			"key_switch": "기타",
			"press": "기타",
			"kind": "기타"
	},
	{
			"name": "레오폴드 FC980C 영문 블랙 (45g, 균등)",
			"img": "https://img.danawa.com/prod_img/500000/741/875/img/4875741_1.jpg?shrink=500:500&_v=20200107111839",
			"brand": "레오폴드",
			"connect": "무접점(정전용량)",
			"weight": "1100g",
			"array": "98",
			"switch": "Topre",
			"key_switch": "기타",
			"press": "기타",
			"kind": "기타"
	},
]
```

처음에는 JSON 파일 형식을 위와 같이 필드만 넣은 리스트>딕셔너리 형식으로 넣었었다.

이런 식으로 넣으니 다음과 같은 에러가 나왔다.

```bash
$ python manage.py loaddata keyboard.json
Traceback (most recent call last):
  File "C:\Users\TFX255GS\Desktop\프로젝트\키보드워리어\venv\lib\site-packages\django\core\serializers\json.py", line 70, in Deserializer
    yield from PythonDeserializer(objects, **options)
  File "C:\Users\TFX255GS\Desktop\프로젝트\키보드워리어\venv\lib\site-packages\django\core\serializers\python.py", line 93, in Deserializer
    Model = _get_model(d["model"])
KeyError: 'model'

The above exception was the direct cause of the following exception:

Traceback (most recent call last):
  File "C:\Users\TFX255GS\Desktop\프로젝트\키보드워리어\keyboard-warrior\manage.py", line 22, in <module>
    main()
  File "C:\Users\TFX255GS\Desktop\프로젝트\키보드워리어\keyboard-warrior\manage.py", line 18, in main
    execute_from_command_line(sys.argv)
  File "C:\Users\TFX255GS\Desktop\프로젝트\키보드워리어\venv\lib\site-packages\django\core\management\__init__.py", line 419, in execute_from_command_line
    utility.execute()
  File "C:\Users\TFX255GS\Desktop\프로젝트\키보드워리어\venv\lib\site-packages\django\core\management\__init__.py", line 413, in execute
    self.fetch_command(subcommand).run_from_argv(self.argv)
  File "C:\Users\TFX255GS\Desktop\프로젝트\키보드워리어\venv\lib\site-packages\django\core\management\base.py", line 354, in run_from_argv
    self.execute(*args, **cmd_options)
  File "C:\Users\TFX255GS\Desktop\프로젝트\키보드워리어\venv\lib\site-packages\django\core\management\base.py", line 398, in execute
    output = self.handle(*args, **options)
  File "C:\Users\TFX255GS\Desktop\프로젝트\키보드워리어\venv\lib\site-packages\django\core\management\commands\loaddata.py", line 78, in handle
    self.loaddata(fixture_labels)
  File "C:\Users\TFX255GS\Desktop\프로젝트\키보드워리어\venv\lib\site-packages\django\core\management\commands\loaddata.py", line 123, in loaddata
    self.load_label(fixture_label)
  File "C:\Users\TFX255GS\Desktop\프로젝트\키보드워리어\venv\lib\site-packages\django\core\management\commands\loaddata.py", line 181, in load_label
    for obj in objects:
  File "C:\Users\TFX255GS\Desktop\프로젝트\키보드워리어\venv\lib\site-packages\django\core\serializers\json.py", line 74, in Deserializer
    raise DeserializationError() from exc
django.core.serializers.base.DeserializationError: Problem installing fixture 'C:\Users\TFX255GS\Desktop\프로젝트\키보드워리어\keyboard-warrior\keyboard.json':
(venv)
```

잘 읽어 보니 `model`이라는 key가 없어서 어쩔 줄 몰라 하는 것 같았다.

다시 구글링을 통해 JSON 파일을 만들어서 `loaddata` 하는 것을 찾아보니 JSON이 아래와 같은 형식으로 짜여있는 것을 볼 수 있었다.

field

`pk` 도 함께 넣은 사람들도 많았는데 pk는 넣든 안넣든 똑같은 결과가 나왔다.

### 참고 자료


[](https://velog.io/@iris/JSON-%ED%8C%8C%EC%9D%BC%EC%9D%84-DB%EC%97%90-%EC%A0%80%EC%9E%A5%ED%95%98%EA%B8%B0-with-Django-SQLite)

[장고(Django) :: dumpdata와 loaddata를 활용해서 데이터 옮기기](https://realcoding.tistory.com/2)

### 해결 방법


```bash
[
	{
		"model": "articles.Keyboard",
		"pk": 1,
		"fields": {
			"name": "레오폴드 FC980C 영문 화이트 (30g, 균등)",
			"img": "https://img.danawa.com/prod_img/500000/167/670/img/7670167_1.jpg?shrink=500:500&_v=20200107112457",
			"brand": "레오폴드",
			"connect": "무접점(정전용량)",
			"weight": "1100g",
			"array": "98",
			"switch": "Topre",
			"key_switch": "기타",
			"press": "기타",
			"kind": "기타"
		}
	},
	{
		"model": "articles.Keyboard",
		"fields": {
			"name": "레오폴드 FC980C 영문 블랙 (45g, 균등)",
			"img": "https://img.danawa.com/prod_img/500000/741/875/img/4875741_1.jpg?shrink=500:500&_v=20200107111839",
			"brand": "레오폴드",
			"connect": "무접점(정전용량)",
			"weight": "1100g",
			"array": "98",
			"switch": "Topre",
			"key_switch": "기타",
			"press": "기타",
			"kind": "기타"
		}
	},
]
```

</details>

<details>

<summary> 6.JS를 통해 DIV태그  display조작 </summary>


 
  ```jsx
<script src="https://cdn.jsdelivr.net/npm/axios/dist/axios.min.js"></script>
<script>
  const search_input = document.querySelector('#search_input');
  const search_box = document.querySelector('#search_box');
  const input = document.createElement('input');
  const side = document.querySelector('#side');
  const box_open = false;

  search_input.addEventListener('click', function (event) {
    console.log("검색클릭");
    search_box.classList.remove('search-off');
    search_box.classList.add('search-on');
    const box_open = true;
    console.log("검색 열림");

  });

  document.addEventListener('click', function (e) {
    console.log(e.target)
    console.log(search_box.id)
    if (box_open === true); {
      if (e.target !== search_input) {
        search_box.classList.remove('search-on');
        search_box.classList.add('search-off');
        console.log("검색디브 닫힘")
      }
    }
  });
```

```html
<input id="search_input" class="form-control me-2" name="search" type="search" placeholder="Search"
      aria-label="Search">
    <!-- <input창> -->
    <div class="search-off search-div " id="search_box" >
      <!-- 여기가 제품 검색 결과 나오는 디브  -->
    </div>
```

스크립트 변수 명에 넣은 ID의 위치를 잘 확인 할 것.

`search_box`  div와  `search_input` input창의 고유값은 각각 다름 같은 디브로 묶어주거나

위치를 명시한 곳이 정확한지 확인할 것 .


</details>

<details>

<summary> 7. views.py에서 form.errors 와 views.create에서 키보드저장방법 </summary>

 
  폼 에러 확인법  →  print(review_form.errors) 

form 뒤에 errors를 찍어서 오류 찾기 

```html
review_form = ReviewForm()
    print(review_form.errors)
```

```
def create(request):
    if request.method == "POST":
        review_form = ReviewForm(request.POST, request.FILES)
        kb = Keyboard.objects.get(name=request.POST["keyboard"])
        print(kb, 1)
        if review_form.is_valid():
            print("유효성검사")
            review = review_form.save(commit=False)
            review.user = request.user
            print("키보드 저장전")
            review.keyboard = kb
            review.save()
            print("저장")
            return redirect("reviews:index")
    else:
        review_form = ReviewForm()
    print(review_form.errors)
    context = {
        "review_form": review_form,
    }
    return render(request, "reviews/create.html", context)
```

필드에 설정했지만, 값을 미리 받지 않음 

발단

form.py → forms 필드에 테이블을 지정해서 폼을 보낼 때 값을 받아온다고 지정해놔서 오류 발생 

원인

save(commit=false)를 하고 값을 나중에 넣어줘서 오류가 났음 

forms.py  → fields에서 keyborad 테이블에 빼줘서 고쳐짐

</details>

<details>


<summary> 8.쿠키생성이슈</summary>


  ### 이슈 내용

  ❗ 쿠키 생성 하는 로직을 다시 되돌아보아서 문제점을 발견


  쿠키생성할때 return값을 response로 주어야한다.


  
</details>


<details>

<summary>9.인코딩오류 </summary>


  ```python
  # 오류구문메세지
  UnicodeEncodeError: 'latin-1' codec can't encode characters in position 202-203: ordinal not in range(256)
  C:\Users\82107\Desktop\키보드워리어\keyboard-warrior\articles\views.py changed, reloading.
  ```

  발생 사례 - > 아이디가 한글로 들어갔을 때, 인코딩 오류가 발생 → 원인 (쿠키처리하며 `request.user` 를 넣으며 한글처리가 안되었음 )

  해결방법 -> `encode('utf8')` 메소드를 `request.user` 뒤에 붙여줘서 인코딩처리 바꿔주며 해결

  10.insertAdjacentHTML
    ### 이슈 내용


  자바스크립트 insertAdjacentHTML를 이용하여 html 구문을 넣었는데 뒤에 닫는 태그를 평소처럼 마지막에 연달아서 닫아버리니까 작동이 안됐다.

  닫는 `/div` 가 제대로 insert 되지 않았기 때문에 아래와 같이 구조가 깨졌다.

  ![Untitled](https://s3-us-west-2.amazonaws.com/secure.notion-static.com/dca56929-e294-4a83-832e-09733f0dfa4a/Untitled.png)

  ![Untitled](https://s3-us-west-2.amazonaws.com/secure.notion-static.com/942b754c-ca88-412b-a490-8c2f3eb0681e/Untitled.png)

  ```jsx
  const comment_data = response.data.comment_data
                  const user = response.data.user
                  for (let i = 0; i < comment_data.length; i++) {
                    const review_pk = response.data.review_pk
                    console.log(comment_data[i].id, user)
                    comments.insertAdjacentHTML('beforeend', `
                      <div class="comment">
                        <div class="keyboard-comment">`);
                    // 기본 계정이면
                    if(comment_data[i].image) {
                      if(comment_data[i].is_social === 0) {
                        document.querySelector('.keyboard-comment').insertAdjacentHTML('beforeend', `
                        <a href="/accounts/${comment_data[i].id}/detail">
                          <img class="comment-profile-img" src="/media/${comment_data[i].image}">
                        </a>
                        `);
                      }
                      // 소셜 로그인 계정이면
                      else {
                        document.querySelector('.keyboard-comment').insertAdjacentHTML('beforeend', `
                        <a href="/accounts/${comment_data[i].id}/detail">
                          <img class="comment-profile-img" src="${comment_data[i].image}">
                        </a>
                        `);
                      }
                    }
                    else {
                      document.querySelector('.keyboard-comment').insertAdjacentHTML('beforeend', `
                      <a href="/accounts/${comment_data[i].id}/detail">
                        <img class="comment-profile-img" src="{% static 'images/logo_png.png' %}">
                      </a>
                      `);
                    }
                    document.querySelector('.keyboard-comment').insertAdjacentHTML('beforeend', `
                    <div class="keyboard-comment-box">
                      <a href="/accounts/${comment_data[i].id}/detail">
                        <p class="keyboard-comment-user">${comment_data[i].userName}</p>
                      </a>
                    `);
                    // 내가 좋아요를 누른 댓글이면
                    if(comment_data[i].islike) {
                      document.querySelector('.keyboard-comment-box').insertAdjacentHTML('beforeend', `
                        <i class="bi bi-heart-fill" onclick="likecomment(this)" data-review-id="{{ review.pk }}" data-comment-id="${comment_data[i].id}" id="commentlike"></i>
                      `);
                    }
                    else {
                      document.querySelector('.keyboard-comment-box').insertAdjacentHTML('beforeend', `
                        <i class="bi bi-heart" onclick="likecomment(this)" data-review-id="{{ review.pk }}" data-comment-id="${comment_data[i].id}" id="commentlike"></i>
                      `);
                    }
                    // 내가 댓글 작성자면
                    if(user === comment_data[i].id) {
                      document.querySelector('.keyboard-comment-box').insertAdjacentHTML('beforeend', `
                      <button class="comment-delete-btn" onclick="delete_comment(this)" id="comment-delete-${comment_data[i].id}" data-reviewdel-id="{{ review.pk }}" data-commentdel-id="${comment_data[i].id}">삭제</button>
                      `)
                    }
                    document.querySelector('.keyboard-comment-box').insertAdjacentHTML('beforeend', `
                    <div>${comment_data[i].content}</div>
                      </div>
                    </div>
                    </div>
                    `)
                  } commentForm.reset()
              }).catch(console.log(1))
          })
  ```

  ### 참고 자료

  [Consolidate Duplicate Conditional Fragments](https://refactoring.guru/ko/consolidate-duplicate-conditional-fragments)

  [Extract Variable](https://refactoring.guru/ko/extract-variable)

  ### 해결 방법

  ```jsx
      // 프로필 이미지
      let profile_src = "";
      if (comment_data[i].image) {
        if (comment_data[i].is_social === 0) {
          profile_src = `/media/${comment_data[i].image}`;
        }
        else {
          profile_src = `${comment_data[i].image}`;
        }
      }
      else {
        profile_src = `{% static 'images/logo_png.png' %}`;
      }

      // 내가 좋아요를 누른 댓글이면
      let like = "";
      if (comment_data[i].islike) {
        like = "bi-heart-fill";
      }
      else {
        like = "bi-heart";
      }

      // 내가 댓글 작성자면
      let writer = "";
      if(user === comment_data[i].id) {
        writer = `<button class="comment-delete-btn" onclick="delete_comment(this)" id="comment-delete-{{ comment.pk }}" data-reviewdel-id="{{ review.pk }}" data-commentdel-id="{{ comment.pk }}">삭제</button>`
      }

      let html = `
        <div class="comment">
          <div class="keyboard-comment">
        
            <a href="/accounts/${comment_data[i].id}/detail">
            <img class="comment-profile-img" src="${profile_src}">
          </a>
          <div class="keyboard-comment-box">
            <a href="/accounts/${comment_data[i].id}/detail">
              <p class="keyboard-comment-user">${comment_data[i].userName}</p>
            </a>
            <i class="bi ${like}" onclick="likecomment(this)" data-review-id="{{ review.pk }}" data-comment-id="{{ comment.pk }}" id="commentlike"></i>
            ${writer}
            <div>${comment_data[i].content}</div>
          </div>
        </div>
      </div>`
      document.querySelector('#comments').insertAdjacentHTML('beforeend', `${html}`)
  ```

  if 문으로 분기해서 달라지는 부분만 변수로 처리해주고,

  문자열로 모든 html 문서를 만들어서 마지막에 한번만 `insertAdjacentHTML` 을 해준다.

  댓글 삭제에도 같은 로직이 쓰이므로 함수로 만들어주면 편할 것 같은데 일단 시간 관계상 이렇게 해결했으니까 다른 것들을 다 한 후에 다시 해보기로 했다.

  참고: view 에서는 img src를 보낼 때 문자열 처리를 해줘야함 만약에 안해주면 image field 객체라서 json에는 객체가 못들어가기 때문에 오류가 난다.


</details>

<details>


<summary>10.찾는 요소가 없어서 에러가 뜰 때 무시하는 방법</summary>

  

   ### 참고 자료
  [Optional chaining (?.) - JavaScript | MDN](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Operators/Optional_chaining)

  11.코드를 간결하게 하는 법 (classlist toggle, conditional operator)
  [Element.classList - Web APIs | MDN](https://developer.mozilla.org/en-US/docs/Web/API/Element/classList)

  [Conditional (ternary) operator - JavaScript | MDN](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Operators/Conditional_Operator)

</details>



  


&nbsp;

# 칸반보드

## 11월8일
- 기획안 작성
- 모델 생성
- 피그마 작성

&nbsp;

## 11월9일
- Django 기본 세팅
- ERD 작성
- 피그마 작성

&nbsp;

## 11월10일
- 피그마 완성
- 다나와 사이트 데이터 크롤링
- 크롤링 데이터 정제 작업
- `accounts` 회원가입 기능 완성
- `accounts` 로그인 기능 완성
- `base.html` nav바 완성
- `articles/main.html` 구조 완성
- `reviews/detail.html` 비동기 댓글 생성
- `trade/detail.html` 비동기 댓글생성
- `reviews/detail.html` 즐겨찾기
- 회원가입,로그인,회원정보수정 폼
- `articles/all` 무한 스크롤
- `trade`앱 CRUD

&nbsp;

## 11월11일
- `accounts/deatail.html`
- `reviews/create.html`
- `articles/all.html` 구조 및 애니메이션 넣기
- `trade/keyboard_search` 키보드 비동기 검색
- `trade/detail` 비동기 댓글 생성 및 삭제
- `trade/detail` 찜하기
- 데이터 json파일 DB저장 (python manage.py loaddata)

&nbsp;

## 11월12일
- `reviews`, `trade` 댓글 욕설, 비속어 필터링
- `reviews/create`,`trade/create` 다중 이미지
- `main`페이지 오늘 방문자 수 및 누적 방문자수 완료
- reviews/detail 조회수

&nbsp;

## 11월13일
accounts/social login 구현

방문자 수

accounts/detail 페이지

articles 반응형

trade 키보드 search 기능

review 조회수, 좋아요

&nbsp;


## 11월14일
중고 거래글 폼 작성
trade 게시글 작성 폼
keyboard_search_fix
trade/index 페이지 완성하기
accounts/social login redirect를 통해 유저 정보 넣기
회원상세정보(수정하나씩)

&nbsp;

## 11월15일
trade/index 라디오 동작시키기
review/index 페이지
articles/all 애니메이션 수정하기
main/유저 선호도 기반 키보드 추천
review/댓글 좋아요 비동기
articles/detail/키보드 평점
trade/detail/ 댓글,댓글창

&nbsp;

## 11월16일
모든 키보드 검색기능
광고 비동기
trade, reviews 검색기능 구현
키보드 detail과 중고 거래게시판 연결
모든 키보드 비동기 스크롤 픽스
소셜로그인 시 추가정보 기입
reviews/detail

&nbsp;

## 11월17일
accounts/메세지함
후기 거래게시글 수정
로그인 폼 변경

&nbsp;

## 11월18일
팔로우기능, 꾸미기

&nbsp;



# 개발 이슈 정리


<details>
<summary>1.셀레니움 비동기 pagenation 크롤링 이슈</summary>
    

다나와에서 제품 크롤링 시, pagenation에서의 비동기로 인해 다음페이지 url을 받아오지 못해 다음페이지의 제품리스트를 크롤링 할 수 없었다. 그래서 한 페이지에 대해서만 크롤링을 반복해서 수행하였다.
    
![Untitled](https://s3-us-west-2.amazonaws.com/secure.notion-static.com/93f02441-5339-45a7-abda-e8636cfcd34b/Untitled.png)

[[Crawling] 다나와(danawa) 제품 리스트 크롤링](https://ysyblog.tistory.com/58)
    
[[파이썬] selenium 크롤링, 데이터 수집 ID, TAG, href 찾기](https://hellodoor.tistory.com/148)
    
[WWW.PHPSCHOOL.COM](https://www.phpschool.com/gnuboard4/bbs/board.php?bo_table=qna_html&wr_id=168862)
    
### 해결 방법
    
다음 페이지로 넘어가는 해결법은 찾지 못했다. 다만, 다나와 사이트에서 의도적으로 크롤링을 막기위해, pagenav탭에서 a태그의 `href` 을 `href='#'` 으로 작성한 것으로 추측된다. `href='#'` 작성하면 a태그 클릭 시, 다음페이지로 넘어가지 못하고 최상단으로 올라가게 된다. 그래서 같은 페이지만 계속 반복하게 되고, 긁어오는 데이터가 반복될 수 밖에 없다.

</details>

<details> 
<summary>2.셀레니움 형제 요소 찾기 / 테이블 추출</summary>


![Untitled](https://s3-us-west-2.amazonaws.com/secure.notion-static.com/e34e86d4-083f-4f91-8f32-f9faa1320a7f/Untitled.png)
    
![Untitled](https://s3-us-west-2.amazonaws.com/secure.notion-static.com/802f6010-f75a-41a5-a653-d1405c354cb1/Untitled.png)
    
```python
# url 리스트 만들기
url_list = []
for li in product_li_tags:
url_list.append(li.select_one('p.prod_name a').get('href'))

for sub_url in url_list:
driver.get(sub_url)
time.sleep(0.5)
name = driver.find_element(By.CSS_SELECTOR, '.prod_tit>.title').text.strip()
img_link = driver.find_element(By.CSS_SELECTOR, '.photo_w img').get_attribute('src')
print(name, img_link)
# 상세정보 클릭
driver.find_element(By.CSS_SELECTOR, '#bookmark_product_information_item').click()
time.sleep(0.5)
# 키압, 무게, 배열, 소리, 브랜드, 축
spec_table = driver.find_elements(By.XPATH, '//*[@id="productDescriptionArea"]/div/div[1]/table/tbody')
brand, keys, connet = '', '', ''
for specs in spec_table:
    ths = specs.find_elements(By.XPATH, '/tr[1]/th[1]')
    for th in ths:
        if th.text == '제조회사':
            try:
                # brand = th.find_element(By.CSS_SELECTOR, '+td').text
                # brand = th.find_elements(By.CSS_SELECTOR, '~td').text
                
                brand = th.find_element(By.XPATH, '/following-sibling::*').text
            except:
                brand = th.find_element(By.XPATH, '/following-sibling::*/a').text
            print(brand)

        # elif th.find_elements(By.CSS_SELECTOR, 'a').text == '키 배열':
        #     try:
        #         keys = th.find_element(By.CSS_SELECTOR, '+td').text
        #     except:
        #         th.find_element(By.CSS_SELECTOR, '+td a').text

        # elif th.find_elements(By.CSS_SELECTOR, 'a').text == '연결 방식':
        #     connet = th.find_element(By.CSS_SELECTOR, '+td a').text
print(brand, keys, connet)
```
    
다나와 사이트를 크롤링을 하면서 문제가 발생하였다.

테이블 `tr` 에서 `th` 값을 찾은 다음, 형제 요소인 `td`를 찾아서 그에 대한 text 값을 찾으려고 했다.

처음에는 `CSS_SELECTOR` 로 인접 형제 선택자인 `+td` 를 사용해보았는데 값을 찾지 못했다.

두번째 시도는 `XPATH`를 이용했다. `following-sibling::*` 을 사용하였더니 요소 자체는 선택을 잘 했지만 print되는 값이 없었다. (아직 이 이유는 알 수 없음)

### 참고 자료

[XPATH란? 셀레니움(Sellenium) XPath로 쉽게 요소 선택하기!](https://aplab.tistory.com/entry/XPATH%EB%9E%80-%EC%85%80%EB%A0%88%EB%8B%88%EC%9B%80Sellenium-XPath%EB%A1%9C-%EC%89%BD%EA%B2%8C-%EC%9A%94%EC%86%8C-%EC%84%A0%ED%83%9D%ED%95%98%EA%B8%B0)

[XPath Contains, Following Sibling, Ancestor & Selenium AND/OR](https://www.guru99.com/using-contains-sbiling-ancestor-to-find-element-in-selenium.html)

### 해결 방법

```python
# url 리스트 만들기
url_list = []
for li in product_li_tags:
  url_list.append(li.select_one('p.prod_name a').get('href'))

for sub_url in url_list:
  driver.get(sub_url)
  time.sleep(0.5)
  name = driver.find_element(By.CSS_SELECTOR, '.prod_tit>.title').text.strip()
  img_link = driver.find_element(By.CSS_SELECTOR, '.photo_w img').get_attribute('src')
  print(name, img_link)
  # 상세정보 클릭
  driver.find_element(By.CSS_SELECTOR, '#bookmark_product_information_item').click()
  time.sleep(0.5)
  # 키압, 무게, 배열, 소리, 브랜드, 축
  spec_table = driver.find_element(By.CSS_SELECTOR, ".spec_tbl tbody").text
  brand, keys, connet = '', '', ''
  print(spec_table)
```

해결 방법은 아주아주 간단했다😥 그냥 `table`의 `tbody` 자체에서 text를 뽑으면 되는 것이었다…

![Untitled](https://s3-us-west-2.amazonaws.com/secure.notion-static.com/1591e2f5-d884-4201-845a-068b02882dfb/Untitled.png)

결과가 아주아주 잘 뽑히는 것을 볼 수 있었다 ㅠㅠ

나는 원래 뽑을 때부터 내가 원하는 것만 뽑고 싶다는 생각으로 위와 같이 코드를 짰었는데

그렇게 하는 것도 좋긴 하지만 아예 문자열을 모두 가져와서 문자열을 조작하는 것이 더 쉬울 수도 있겠구나 생각했다

</details>

<details>
<summary>3.KMP 알고리즘을 이용한 비속어 텍스트 찾기 이슈</summary>


텍스트 내에 해당 문자열이 존재 유무 찾기에 대한 시간복잡도 이슈

### 해결 방법
❗ KMP 알고리즘으로 시간복잡도 이슈 해결


```python
def maketable(p):
  table = [0] * len(p)
  i = 0
  for j in range(1, len(p)):
    while i > 0 and p[i] != p[j]:
      i = table[i - 1]
    if p[i] == p[j]:
      i += 1
      table[j] = i
  return table
def KMP(p, t):
  ans = []
  table = maketable(p)

  i = 0
  for j in range(len(t)):
    while i > 0 and p[i] != t[j]:
      i = table[i - 1]
    if p[i] == t[j]:
      if i == len(p) - 1:
        ans.append(j - len(p) + 2)
        i = table[i]
      else:
        i += 1
  return ans
```

KMP 알고리즘을 활용한 해결.
</details>
    
<details>

<summary>4.크롤링 데이터 정제 작업 이슈</summary>


  ### 이슈 내용


​    

처음에는 데이터 크롤링 할 때 데이터를 가져오고 정제하고 ORM으로 데이터를 삽입하는 것을 하나의 파이썬 파일 안에서 끝내는 것이 더 좋을 것이라고 생각했었다.

비모쌤이 말씀해주셨는데 `JSON` 파일로 만든 후, 정제하고, 마지막에 쿼리문으로 데이터를 삽입하는 세 과정으로 나누어서 하면 시간을 더 효율적으로 쓸 수 있다고 하셨다.

왜 그런지 생각해보니까 데이터를 가져오는 작업은 셀레니움 특성상 데이터가 많아질 수록 오래걸릴 수 밖에 없다. 그런데 이런식으로 한 파일에 모든 작업을 하려고 하면, 파일에 오타라도 있다면 제일 처음으로 돌아가서 다시 데이터를 가져오는 작업을 해야한다. 우리는 데이터를 가져오고 나서 `.replace` 로 모든 예외사항과 이상한 구문이 붙은 데이터들을 처리중이었는데 만약 우리가 예상하지 못한 이상한 데이터가 생긴다면 그 데이터를 처리하는 구문도 추가한 후 다시 데이터를 가져오는 것부터 시작했다.

그래서 정제하는 작업은 이미 끝나서 세 과정으로 나누진 못했지만 정제 후 바로 DB에 저장하지 않고 `JSON`파일로 저장하였다.

저장한 `JSON` 파일은 검토 완료 후 DB에 넣는 작업인 `loaddata` 를 해줬다. 이렇게 하니 시간이 엄청나게 단축되었다. 다음에 크롤링 할 때에는 꼭 과정을 쪼개서 해봐야겠다.

### 참고 자료


[코드공부방](https://code-study.tistory.com/58)


</details>

<details>

<summary> 5.Django/SQLite DB에 크롤링한 데이터를 넣을 때 JSON 작성 형식</summary>


  ```json
[
  {
      "name": "레오폴드 FC980C 영문 화이트 (30g, 균등)",
      "img": "https://img.danawa.com/prod_img/500000/167/670/img/7670167_1.jpg?shrink=500:500&_v=20200107112457",
      "brand": "레오폴드",
      "connect": "무접점(정전용량)",
      "weight": "1100g",
      "array": "98",
      "switch": "Topre",
      "key_switch": "기타",
      "press": "기타",
      "kind": "기타"
  },
  {
      "name": "레오폴드 FC980C 영문 블랙 (45g, 균등)",
      "img": "https://img.danawa.com/prod_img/500000/741/875/img/4875741_1.jpg?shrink=500:500&_v=20200107111839",
      "brand": "레오폴드",
      "connect": "무접점(정전용량)",
      "weight": "1100g",
      "array": "98",
      "switch": "Topre",
      "key_switch": "기타",
      "press": "기타",
      "kind": "기타"
  },
]
  ```

처음에는 JSON 파일 형식을 위와 같이 필드만 넣은 리스트>딕셔너리 형식으로 넣었었다.

이런 식으로 넣으니 다음과 같은 에러가 나왔다.

```bash
$ python manage.py loaddata keyboard.json
Traceback (most recent call last):
  File "C:\Users\TFX255GS\Desktop\프로젝트\키보드워리어\venv\lib\site-packages\django\core\serializers\json.py", line 70, in Deserializer
    yield from PythonDeserializer(objects, **options)
  File "C:\Users\TFX255GS\Desktop\프로젝트\키보드워리어\venv\lib\site-packages\django\core\serializers\python.py", line 93, in Deserializer
    Model = _get_model(d["model"])
KeyError: 'model'

The above exception was the direct cause of the following exception:

Traceback (most recent call last):
  File "C:\Users\TFX255GS\Desktop\프로젝트\키보드워리어\keyboard-warrior\manage.py", line 22, in <module>
    main()
  File "C:\Users\TFX255GS\Desktop\프로젝트\키보드워리어\keyboard-warrior\manage.py", line 18, in main
    execute_from_command_line(sys.argv)
  File "C:\Users\TFX255GS\Desktop\프로젝트\키보드워리어\venv\lib\site-packages\django\core\management\__init__.py", line 419, in execute_from_command_line
    utility.execute()
  File "C:\Users\TFX255GS\Desktop\프로젝트\키보드워리어\venv\lib\site-packages\django\core\management\__init__.py", line 413, in execute
    self.fetch_command(subcommand).run_from_argv(self.argv)
  File "C:\Users\TFX255GS\Desktop\프로젝트\키보드워리어\venv\lib\site-packages\django\core\management\base.py", line 354, in run_from_argv
    self.execute(*args, **cmd_options)
  File "C:\Users\TFX255GS\Desktop\프로젝트\키보드워리어\venv\lib\site-packages\django\core\management\base.py", line 398, in execute
    output = self.handle(*args, **options)
  File "C:\Users\TFX255GS\Desktop\프로젝트\키보드워리어\venv\lib\site-packages\django\core\management\commands\loaddata.py", line 78, in handle
    self.loaddata(fixture_labels)
  File "C:\Users\TFX255GS\Desktop\프로젝트\키보드워리어\venv\lib\site-packages\django\core\management\commands\loaddata.py", line 123, in loaddata
    self.load_label(fixture_label)
  File "C:\Users\TFX255GS\Desktop\프로젝트\키보드워리어\venv\lib\site-packages\django\core\management\commands\loaddata.py", line 181, in load_label
    for obj in objects:
  File "C:\Users\TFX255GS\Desktop\프로젝트\키보드워리어\venv\lib\site-packages\django\core\serializers\json.py", line 74, in Deserializer
    raise DeserializationError() from exc
django.core.serializers.base.DeserializationError: Problem installing fixture 'C:\Users\TFX255GS\Desktop\프로젝트\키보드워리어\keyboard-warrior\keyboard.json':
(venv)
```

잘 읽어 보니 `model`이라는 key가 없어서 어쩔 줄 몰라 하는 것 같았다.

다시 구글링을 통해 JSON 파일을 만들어서 `loaddata` 하는 것을 찾아보니 JSON이 아래와 같은 형식으로 짜여있는 것을 볼 수 있었다.

field

`pk` 도 함께 넣은 사람들도 많았는데 pk는 넣든 안넣든 똑같은 결과가 나왔다.

### 참고 자료


[](https://velog.io/@iris/JSON-%ED%8C%8C%EC%9D%BC%EC%9D%84-DB%EC%97%90-%EC%A0%80%EC%9E%A5%ED%95%98%EA%B8%B0-with-Django-SQLite)

[장고(Django) :: dumpdata와 loaddata를 활용해서 데이터 옮기기](https://realcoding.tistory.com/2)

### 해결 방법


```bash
[
  {
    "model": "articles.Keyboard",
    "pk": 1,
    "fields": {
      "name": "레오폴드 FC980C 영문 화이트 (30g, 균등)",
      "img": "https://img.danawa.com/prod_img/500000/167/670/img/7670167_1.jpg?shrink=500:500&_v=20200107112457",
      "brand": "레오폴드",
      "connect": "무접점(정전용량)",
      "weight": "1100g",
      "array": "98",
      "switch": "Topre",
      "key_switch": "기타",
      "press": "기타",
      "kind": "기타"
    }
  },
  {
    "model": "articles.Keyboard",
    "fields": {
      "name": "레오폴드 FC980C 영문 블랙 (45g, 균등)",
      "img": "https://img.danawa.com/prod_img/500000/741/875/img/4875741_1.jpg?shrink=500:500&_v=20200107111839",
      "brand": "레오폴드",
      "connect": "무접점(정전용량)",
      "weight": "1100g",
      "array": "98",
      "switch": "Topre",
      "key_switch": "기타",
      "press": "기타",
      "kind": "기타"
    }
  },
]
```

</details>

<details>

<summary> 6.JS를 통해 DIV태그  display조작 </summary>


​    

  ```jsx
<script src="https://cdn.jsdelivr.net/npm/axios/dist/axios.min.js"></script>
<script>
  const search_input = document.querySelector('#search_input');
  const search_box = document.querySelector('#search_box');
  const input = document.createElement('input');
  const side = document.querySelector('#side');
  const box_open = false;

  search_input.addEventListener('click', function (event) {
    console.log("검색클릭");
    search_box.classList.remove('search-off');
    search_box.classList.add('search-on');
    const box_open = true;
    console.log("검색 열림");

  });

  document.addEventListener('click', function (e) {
    console.log(e.target)
    console.log(search_box.id)
    if (box_open === true); {
      if (e.target !== search_input) {
        search_box.classList.remove('search-on');
        search_box.classList.add('search-off');
        console.log("검색디브 닫힘")
      }
    }
  });
  ```

```html
<input id="search_input" class="form-control me-2" name="search" type="search" placeholder="Search"
      aria-label="Search">
    <!-- <input창> -->
    <div class="search-off search-div " id="search_box" >
      <!-- 여기가 제품 검색 결과 나오는 디브  -->
    </div>
```

스크립트 변수 명에 넣은 ID의 위치를 잘 확인 할 것.

`search_box`  div와  `search_input` input창의 고유값은 각각 다름 같은 디브로 묶어주거나

위치를 명시한 곳이 정확한지 확인할 것 .


</details>

<details>

<summary> 7. views.py에서 form.errors 와 views.create에서 키보드저장방법 </summary>


  폼 에러 확인법  →  print(review_form.errors) 

form 뒤에 errors를 찍어서 오류 찾기 

```html
review_form = ReviewForm()
    print(review_form.errors)
```

```
def create(request):
    if request.method == "POST":
        review_form = ReviewForm(request.POST, request.FILES)
        kb = Keyboard.objects.get(name=request.POST["keyboard"])
        print(kb, 1)
        if review_form.is_valid():
            print("유효성검사")
            review = review_form.save(commit=False)
            review.user = request.user
            print("키보드 저장전")
            review.keyboard = kb
            review.save()
            print("저장")
            return redirect("reviews:index")
    else:
        review_form = ReviewForm()
    print(review_form.errors)
    context = {
        "review_form": review_form,
    }
    return render(request, "reviews/create.html", context)
```

필드에 설정했지만, 값을 미리 받지 않음 

발단

form.py → forms 필드에 테이블을 지정해서 폼을 보낼 때 값을 받아온다고 지정해놔서 오류 발생 

원인

save(commit=false)를 하고 값을 나중에 넣어줘서 오류가 났음 

forms.py  → fields에서 keyborad 테이블에 빼줘서 고쳐짐

</details>

<details>


<summary> 8.쿠키생성이슈</summary>


  ### 이슈 내용

  ❗ 쿠키 생성 하는 로직을 다시 되돌아보아서 문제점을 발견


  쿠키생성할때 return값을 response로 주어야한다.


​    

</details>


<details>

<summary>9.인코딩오류 </summary>


  ```python
  # 오류구문메세지
  UnicodeEncodeError: 'latin-1' codec can't encode characters in position 202-203: ordinal not in range(256)
  C:\Users\82107\Desktop\키보드워리어\keyboard-warrior\articles\views.py changed, reloading.
  ```

  발생 사례 - > 아이디가 한글로 들어갔을 때, 인코딩 오류가 발생 → 원인 (쿠키처리하며 `request.user` 를 넣으며 한글처리가 안되었음 )

  해결방법 -> `encode('utf8')` 메소드를 `request.user` 뒤에 붙여줘서 인코딩처리 바꿔주며 해결

  10.insertAdjacentHTML
    ### 이슈 내용


  자바스크립트 insertAdjacentHTML를 이용하여 html 구문을 넣었는데 뒤에 닫는 태그를 평소처럼 마지막에 연달아서 닫아버리니까 작동이 안됐다.

  닫는 `/div` 가 제대로 insert 되지 않았기 때문에 아래와 같이 구조가 깨졌다.

  ![Untitled](https://s3-us-west-2.amazonaws.com/secure.notion-static.com/dca56929-e294-4a83-832e-09733f0dfa4a/Untitled.png)

  ![Untitled](https://s3-us-west-2.amazonaws.com/secure.notion-static.com/942b754c-ca88-412b-a490-8c2f3eb0681e/Untitled.png)

  ```jsx
  const comment_data = response.data.comment_data
                  const user = response.data.user
                  for (let i = 0; i < comment_data.length; i++) {
                    const review_pk = response.data.review_pk
                    console.log(comment_data[i].id, user)
                    comments.insertAdjacentHTML('beforeend', `
                      <div class="comment">
                        <div class="keyboard-comment">`);
                    // 기본 계정이면
                    if(comment_data[i].image) {
                      if(comment_data[i].is_social === 0) {
                        document.querySelector('.keyboard-comment').insertAdjacentHTML('beforeend', `
                        <a href="/accounts/${comment_data[i].id}/detail">
                          <img class="comment-profile-img" src="/media/${comment_data[i].image}">
                        </a>
                        `);
                      }
                      // 소셜 로그인 계정이면
                      else {
                        document.querySelector('.keyboard-comment').insertAdjacentHTML('beforeend', `
                        <a href="/accounts/${comment_data[i].id}/detail">
                          <img class="comment-profile-img" src="${comment_data[i].image}">
                        </a>
                        `);
                      }
                    }
                    else {
                      document.querySelector('.keyboard-comment').insertAdjacentHTML('beforeend', `
                      <a href="/accounts/${comment_data[i].id}/detail">
                        <img class="comment-profile-img" src="{% static 'images/logo_png.png' %}">
                      </a>
                      `);
                    }
                    document.querySelector('.keyboard-comment').insertAdjacentHTML('beforeend', `
                    <div class="keyboard-comment-box">
                      <a href="/accounts/${comment_data[i].id}/detail">
                        <p class="keyboard-comment-user">${comment_data[i].userName}</p>
                      </a>
                    `);
                    // 내가 좋아요를 누른 댓글이면
                    if(comment_data[i].islike) {
                      document.querySelector('.keyboard-comment-box').insertAdjacentHTML('beforeend', `
                        <i class="bi bi-heart-fill" onclick="likecomment(this)" data-review-id="{{ review.pk }}" data-comment-id="${comment_data[i].id}" id="commentlike"></i>
                      `);
                    }
                    else {
                      document.querySelector('.keyboard-comment-box').insertAdjacentHTML('beforeend', `
                        <i class="bi bi-heart" onclick="likecomment(this)" data-review-id="{{ review.pk }}" data-comment-id="${comment_data[i].id}" id="commentlike"></i>
                      `);
                    }
                    // 내가 댓글 작성자면
                    if(user === comment_data[i].id) {
                      document.querySelector('.keyboard-comment-box').insertAdjacentHTML('beforeend', `
                      <button class="comment-delete-btn" onclick="delete_comment(this)" id="comment-delete-${comment_data[i].id}" data-reviewdel-id="{{ review.pk }}" data-commentdel-id="${comment_data[i].id}">삭제</button>
                      `)
                    }
                    document.querySelector('.keyboard-comment-box').insertAdjacentHTML('beforeend', `
                    <div>${comment_data[i].content}</div>
                      </div>
                    </div>
                    </div>
                    `)
                  } commentForm.reset()
              }).catch(console.log(1))
          })
  ```

  ### 참고 자료

  [Consolidate Duplicate Conditional Fragments](https://refactoring.guru/ko/consolidate-duplicate-conditional-fragments)

  [Extract Variable](https://refactoring.guru/ko/extract-variable)

  ### 해결 방법

  ```jsx
      // 프로필 이미지
      let profile_src = "";
      if (comment_data[i].image) {
        if (comment_data[i].is_social === 0) {
          profile_src = `/media/${comment_data[i].image}`;
        }
        else {
          profile_src = `${comment_data[i].image}`;
        }
      }
      else {
        profile_src = `{% static 'images/logo_png.png' %}`;
      }

      // 내가 좋아요를 누른 댓글이면
      let like = "";
      if (comment_data[i].islike) {
        like = "bi-heart-fill";
      }
      else {
        like = "bi-heart";
      }

      // 내가 댓글 작성자면
      let writer = "";
      if(user === comment_data[i].id) {
        writer = `<button class="comment-delete-btn" onclick="delete_comment(this)" id="comment-delete-{{ comment.pk }}" data-reviewdel-id="{{ review.pk }}" data-commentdel-id="{{ comment.pk }}">삭제</button>`
      }

      let html = `
        <div class="comment">
          <div class="keyboard-comment">
        
            <a href="/accounts/${comment_data[i].id}/detail">
            <img class="comment-profile-img" src="${profile_src}">
          </a>
          <div class="keyboard-comment-box">
            <a href="/accounts/${comment_data[i].id}/detail">
              <p class="keyboard-comment-user">${comment_data[i].userName}</p>
            </a>
            <i class="bi ${like}" onclick="likecomment(this)" data-review-id="{{ review.pk }}" data-comment-id="{{ comment.pk }}" id="commentlike"></i>
            ${writer}
            <div>${comment_data[i].content}</div>
          </div>
        </div>
      </div>`
      document.querySelector('#comments').insertAdjacentHTML('beforeend', `${html}`)
  ```

  if 문으로 분기해서 달라지는 부분만 변수로 처리해주고,

  문자열로 모든 html 문서를 만들어서 마지막에 한번만 `insertAdjacentHTML` 을 해준다.

  댓글 삭제에도 같은 로직이 쓰이므로 함수로 만들어주면 편할 것 같은데 일단 시간 관계상 이렇게 해결했으니까 다른 것들을 다 한 후에 다시 해보기로 했다.

  참고: view 에서는 img src를 보낼 때 문자열 처리를 해줘야함 만약에 안해주면 image field 객체라서 json에는 객체가 못들어가기 때문에 오류가 난다.


</details>

<details>


<summary>10.찾는 요소가 없어서 에러가 뜰 때 무시하는 방법</summary>


​      

    ### 참고 자료
  [Optional chaining (?.) - JavaScript | MDN](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Operators/Optional_chaining)

  11.코드를 간결하게 하는 법 (classlist toggle, conditional operator)
  [Element.classList - Web APIs | MDN](https://developer.mozilla.org/en-US/docs/Web/API/Element/classList)

  [Conditional (ternary) operator - JavaScript | MDN](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Operators/Conditional_Operator)

</details>
