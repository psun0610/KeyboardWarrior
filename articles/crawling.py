import time
from selenium.webdriver import Chrome
from selenium.webdriver import ChromeOptions

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from bs4 import BeautifulSoup
import json


def toJson(mnet_dict):
    with open("keyboard.json", "w", encoding="utf-8") as file:
        json.dump(mnet_dict, file, ensure_ascii=False, indent="\t")


# 브라우저 띄우지 않고 하기
options = ChromeOptions()
options.add_argument("headless")

driver = Chrome()
driver.get("https://prod.danawa.com/list/?cate=112782&15main_11_02")

# 없는것을 만들어야할때.
# 제조사별 검색 (XPATH 경로 찾는 방법은 이미지 참조)
# 옵션 더보기

WebDriverWait(driver, 30).until(
    EC.presence_of_element_located(
        (By.XPATH, '//*[@id="dlMaker_simple"]/dd/div[2]/button[1]')
    )
).click()

# 삼성전자
driver.find_element(
    By.CSS_SELECTOR, "dl#dlMaker_simple > dd > ul:nth-of-type(2) > li:nth-child(44)"
).click()

time.sleep(0.5)


# 앱코
# driver.find_element(
#     By.CSS_SELECTOR, "dl#dlMaker_simple > dd > ul:nth-of-type(2) > li:nth-child(68)"
# ).click()
# time.sleep(2)

# 엠스톤
driver.find_element(
    By.CSS_SELECTOR, "dl#dlMaker_simple > dd > ul:nth-of-type(2) > li:nth-child(77)"
).click()

time.sleep(0.5)


# 레오
driver.find_element(
    By.CSS_SELECTOR, "dl#dlMaker_simple > dd > ul:nth-of-type(2) > li:nth-child(26)"
).click()

time.sleep(0.5)


# 로지텍
driver.find_element(
    By.CSS_SELECTOR, "dl#dlMaker_simple > dd > ul:nth-of-type(2) > li:nth-child(182)"
).click()

time.sleep(0.5)


# 체리
driver.find_element(
    By.CSS_SELECTOR, "dl#dlMaker_simple > dd > ul:nth-of-type(2) > li:nth-child(145)"
).click()

time.sleep(0.5)



WebDriverWait(driver, 30).until(
    EC.presence_of_element_located(
        (By.XPATH, '//*[@id="productListArea"]/div[2]/div[2]/div[2]/select')
    )
).click()
WebDriverWait(driver, 30).until(
    EC.presence_of_element_located(

time.sleep(0.5)

        (By.XPATH, '//*[@id="productListArea"]/div[2]/div[2]/div[2]/select/option[3]')
    )
).click()
time.sleep(1)


driver.find_element(
    By.XPATH, '//*[@id="productListArea"]/div[2]/div[1]/ul/li[4]/a'
).click()

time.sleep(0.5)


soup = BeautifulSoup(driver.page_source)
product_li_tags = soup.select("li.prod_item.prod_layer")

print(len(product_li_tags))
# url 리스트 만들기
url_list = []
for li in product_li_tags:
    k = li.select_one("p.prod_name a").get("href")
    if k:
        url_list.append(k)
a = []
for _ in range(len(product_li_tags)):
    a.append([])

for sub_url in range(90):
    driver.get(url_list[sub_url])

    time.sleep(1)
    name = driver.find_element(By.CSS_SELECTOR, ".prod_tit>.title").text.strip()
    driver.find_element(By.CSS_SELECTOR, ".photo_w").click()
    time.sleep(1)

    

    driver.find_element(By.CSS_SELECTOR, ".va_top").click()
    time.sleep(1)
    imgs = driver.find_element(By.CSS_SELECTOR, ".big_img > img").get_attribute("src")
    time.sleep(1)
    WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="closeImgExpandLayer"]'))
    ).click()
    driver.find_element(By.CSS_SELECTOR, "#bookmark_product_information_item").click()

    time.sleep(0.5)
    # 키압, 무게, 배열, 소리, 브랜드, 축
    spec_table = driver.find_element(By.CSS_SELECTOR, ".spec_tbl tbody").text
    a[sub_url].append(imgs)
    a[sub_url].append(name)
    m = ""
    for i in spec_table:
        if i == " ":
            m = m.replace("\n", "")
            a[sub_url].append(m)
            m = ""
        else:
            m += i
print(a)
print("------------------------------------------")
result_list = []
for i in range(90):
    img, brand, connect, weight, array, switch, press, kind, key_switch = (
        "기타",
        "기타",
        "기타",
        "기타",
        "기타",
        "기타",
        "기타",
        "기타",
        "기타",
    )
    img = a[i][0]
    name = a[i][1]
    print(name)
    print(img)
    for j in range(len(a[i]) - 1):
        if a[i][j] == "제조회사":
            brand = a[i][j + 1]
            print(brand)
        elif a[i][j] == "방식":
            if a[i][j + 1] != "광":
                connect = (
                    a[i][j + 1]
                    .replace("크기(가로x세로x높이)가로", "")
                    .replace("기능응답속도", "")
                    .replace("외형비키스타일", "")
                )
            print(connect)
        elif a[i][j] == "무게":
            weight = (
                a[i][j + 1]
                .replace("케이블", "")
                .replace("마우스", "")
                .replace("제품", "")
                .replace("키", "")
                .replace("제품", "")
                .replace("KC인증적합성평가인증", "")
            )
            print(weight)
        elif a[i][j] == "배열":  # 몇 킨지
            array = (
                a[i][j + 1]
                .replace("인터페이스", "")
                .replace("용도사무용", "")
                .replace("키", "")
                .replace("개", "")
            )
            print(array)
        elif a[i][j] == "스위치":  # 스위치, 키 스위치(저소음 적축 등)
            if a[i][j + 1] != "교체":
                # 저소음만 들어오면 뒤에 있는 적축까지 붙임
                if a[i][j + 1] == "저소음":
                    key_switch = a[i][j + 1] + a[i][j + 2]
                    print(key_switch)
                elif "축" in a[i][j + 1]:
                    key_switch = (
                        a[i][j + 1]
                        .replace("키압", "")
                        .replace("키", "")
                        .replace("기능동시입력", "")
                    )
                else:
                    switch = (
                        a[i][j + 1]
                        .replace("키압", "")
                        .replace("키", "")
                        .replace("기능동시입력", "")
                    )
                    print(switch)
        elif a[i][j] == "키압":
            press = (
                a[i][j + 1]
                .replace("키보드형태", "")
                .replace("기능동시입력", "")
                .replace("기능키멀티미디어", "")
            )
            print(press)
        elif a[i][j] == "키보드형태":  # 텐키리스/ 풀배열
            kind = a[i][j + 1].replace("기능키멀티미디어", "")
            print(kind)
        # img, brand, connect, weight, array, switch, press, kind, key_switch
        result = {
            "name": name,
            "img": img,
            "brand": brand,
            "connect": connect,
            "weight": weight,
            "array": array,
            "switch": switch,
            "key_switch": key_switch,
            "press": press,
            "kind": kind,
        }
    result_list.append(result)
    print("------")
toJson(result_list)