import time
from selenium.webdriver import Chrome
from selenium.webdriver import ChromeOptions

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from bs4 import BeautifulSoup
# 브라우저 띄우지 않고 하기
options = ChromeOptions()
options.add_argument('headless')

driver = Chrome()
driver.get('https://prod.danawa.com/list/?cate=112782&15main_11_02')

# 없는것을 만들어야할때.
# 제조사별 검색 (XPATH 경로 찾는 방법은 이미지 참조)
# 옵션 더보기
WebDriverWait(driver,30).until(EC.presence_of_element_located((By.XPATH,'//*[@id="dlMaker_simple"]/dd/div[2]/button[1]'))).click()

# 앱코 등등 클릭
driver.find_element(By.CSS_SELECTOR, 'dl#dlMaker_simple > dd > ul:nth-of-type(2) > li:nth-child(68)').click()
time.sleep(2)

WebDriverWait(driver,30).until(EC.presence_of_element_located((By.XPATH,'//*[@id="productListArea"]/div[2]/div[2]/div[2]/select'))).click()
WebDriverWait(driver,30).until(EC.presence_of_element_located((By.XPATH,'//*[@id="productListArea"]/div[2]/div[2]/div[2]/select/option[3]'))).click()
time.sleep(1)

soup = BeautifulSoup(driver.page_source)
product_li_tags = soup.select('li.prod_item.prod_layer')

print(len(product_li_tags))
# url 리스트 만들기
url_list = []
for li in product_li_tags:
    k = li.select_one('p.prod_name a').get('href')
    if k:
        url_list.append(k)
a = [[] for _ in range(len(url_list))]
for sub_url in range(len(url_list)):
	driver.get(url_list[sub_url])
	time.sleep(0.5)
	name = driver.find_element(By.CSS_SELECTOR, '.prod_tit>.title').text.strip()
	driver.find_element(By.CSS_SELECTOR, '.photo_w').click()
	time.sleep(2)

	driver.find_element(By.CSS_SELECTOR, '.va_top').click()
	time.sleep(1)
	imgs = driver.find_element(By.CSS_SELECTOR, '.big_img > img').get_attribute('src')
	time.sleep(1)

	WebDriverWait(driver,30).until(EC.presence_of_element_located((By.XPATH,'//*[@id="closeImgExpandLayer"]'))).click()
	driver.find_element(By.CSS_SELECTOR, '#bookmark_product_information_item').click()
	time.sleep(0.5)
	# 키압, 무게, 배열, 소리, 브랜드, 축
	spec_table = driver.find_element(By.CSS_SELECTOR, ".spec_tbl tbody").text
	brand, keys, connet = '', '', ''
	m = ''
	for i in spec_table:
		if i == " ":
			print(m)
			m = ''
		else:
			m += i
	# print(spec_table)
	# print(imgs)
	# print(spec_table)
	# print("-----")
