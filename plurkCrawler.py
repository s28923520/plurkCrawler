#留言、喊單者名稱包含收
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import time

url = ''    #噗文網址
keyword = '收'  #欲爬取關鍵字

# 使用 Chrome 驅動程式
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver.implicitly_wait(10)

# 打開網頁
driver.get(url)

# 使用 WebDriverWait 等待動態載入完成
wait = WebDriverWait(driver, 10)

# 使用 execute_script 執行 JavaScript 代碼，模擬滾動到頁面底部觸發動態載入
driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

comments = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'plurk.cboxAnchor.response.clearfix.divresponse')))

# 取得包含指定關鍵字的留言
# comments = driver.find_elements(By.CLASS_NAME, 'text_holder')



# 印出符合關鍵字的留言和留言者ID
for comment in comments:
    if keyword in comment.text:
        try:
            actions = ActionChains(driver)
            # 找到包含 a.name 的元素
            a_tag = comment.find_element(By.CSS_SELECTOR, '.user a.name')
            
            # 模擬鼠標懸停在 a 標籤上，觸發浮動視窗顯示
            ActionChains(driver).move_to_element(a_tag).perform()
            
            # # 使用 WebDriverWait 等待浮動視窗內元素的可見性
            # pop_view = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, 'pop-view-content')))
            # 使用 WebDriverWait 等待浮動視窗內元素的可見性
            pop_view = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'pop-view-content')))
            
            # 再次等待一段時間，確保視窗內的元素完全載入
            time.sleep(0.1)  # 調整這裡的等待時間
            
            # 取得浮動視窗內的元素
            user_id = pop_view.find_element(By.CLASS_NAME, 'nick_name').text
            
            # 取得留言內容
            comment_content = comment.find_element(By.CLASS_NAME, 'text_holder').text
            
            print(f"留言內容: {comment_content}\n留言者ID: {user_id}\n")
            actions.move_to_element_with_offset(comment, 0, 0).perform()
        except Exception as e:
            print(f"無法取得浮動視窗內的元素: {e}")
    
        
# 關閉瀏覽器視窗
driver.quit()
