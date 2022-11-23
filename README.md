# 키보드워리어

> 키보드 중고 거래, 사용자 맞춤형 키보드 추천 서비스, 검색 서비스, 키보드 후기 제공 해주는 사이트



## 프로젝트 소개

- 🗓**프로젝트 기간**
  - 2022.11.09 (수) ~ 2022.11.21 (월)
- 💻**사용 기술**
  - Python, Django, HTML, CSS, Javascript, Bootstrap5, Selenium, Beautifulsoup4
- ⭐**개발 역할 분담**
  - 팀장: 하승찬, 발표자: 유순일, PPT 제작자: 박선영, 문재윤, 지현식
  - **백엔드**: 지현식, 하승찬, 유순일
  - **프론트엔드**: 박선영, 문재윤



## 🚩목적

Django를 통해 

내가 이 기능에 어떻게 접근, 그 과정에서 이슈들을 해결
ex) 무한스크롤, 레디스 소켓 사용



## 모델 구조, ERD 작성
![키보드워리어 최종 ERD](https://user-images.githubusercontent.com/97111793/203498672-67c14351-a903-4e81-95e2-619f43b4203d.png)

**App별 Model**
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


## 기능

### 제품 정보 수집

- 크롤링 



### Articles/main

- 전체 방문자 수, 오늘 방문자 수 표시
- 사용자 맞춤형 키보드 추천
  - 사용자가 회원가입시 입력한 정보를 기반으로 키보드를 추천하는 기능

### Articles/all

- 비동기 무한 스크롤
- 비동기 키보드 필터링
- 비동기 키보드 검색 기능



### Articles/detail 

- 키보드 후기 평균 별점을 보여줌



### Trade/index

- 키보드 이름, 리뷰 제목 검색 기능
- 라디오 버튼을 통해 판매글만, 구매글만 선택 가능
- 키보드, 판매글 검색



### Trade/detail

- 비동기 게시글 찜하기
- 비동기 댓글 생성 및 삭제
- 게시글 사진 여러 장
- 댓글 욕설 필터링
- 채팅 (비동기 채팅, DB저장)



### Trade/create

키보드모델명 쉽게검색
사진 여러장 추가 



### Reviews/index

비공기 글 좋아요
비동기 댓글 삭제, 생성
비동기 댓글 좋아요
닷글 욕설 필터링



### Reviews/detail

### Reviews/create

키보드 모델명 쉽게 검색
별점선택 



### Accounts/detail

10. 어카운트
    소셜계정로그인
    로그인시 선호 키보드정보 가져오기 

11. 마이페이지
    라디오버튼 메뉴
    비동기 팔로우

### Chat


12. 채팅 

배포시 반실시간 채팅구현
로컬시 채팅기능구현 

13. 기타 중요기능
알림기능
