from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from bs4 import BeautifulSoup
import os
import time

def StartCrawl():
    # 設定起始年月和終止年月
    start_year = 103
    start_month = 1
    end_year = 109  # 假設這是最終的年份
    end_month = 12  # 假設這是最終的月份
    
    url = 'https://www.taiwanlottery.com.tw/lotto/Lotto649/history.aspx'
    chrome_options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(options=chrome_options)
    driver.get(url)

    # 遍歷年份和月份
    for year in range(start_year, end_year + 1):
        for month in range(1, 13):
            if year == end_year and month > end_month:
                break  # 如果超出終止月份，停止迭代
            
            # 切換到 "按年月查詢" 選項
            WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.ID, "Lotto649Control_history_radYM"))
            ).click()
            
            # 接下來等待年份和月份的選擇器可用
            WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.NAME, 'Lotto649Control_history$dropYear'))
            )
            WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.NAME, 'Lotto649Control_history$dropMonth'))
            )

            # 選擇年份和月份
            select_year = Select(driver.find_element(By.NAME, 'Lotto649Control_history$dropYear'))
            select_month = Select(driver.find_element(By.NAME, 'Lotto649Control_history$dropMonth'))
            select_year.select_by_value(str(year))
            select_month.select_by_value(str(month))

            # 提交查詢
            submit_button = driver.find_element(By.NAME, 'Lotto649Control_history$btnSubmit')
            submit_button.click()
            
            # 等待結果加載
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, '#right .table_gre, #right .table_org'))
            )

            # 獲取頁面源代碼並解析
            html_source = driver.page_source
            soup = BeautifulSoup(html_source, 'html.parser')
            
            # 解析并写入数据到文件
            output_directory = f'./crawl_data/{year}'
            if not os.path.exists(output_directory):
                os.makedirs(output_directory)  # 如果目录不存在，创建它

            # 解析並寫入數據到文件
            with open(f'{output_directory}/lottery_results_{year}_{month}.txt', 'w', encoding='utf-8') as file:
                draw_details = soup.find_all('table', class_=['table_gre', 'table_org'])
                for detail in draw_details:
                    # ...提取和寫入開獎資料的代碼（與之前相同）...
                                # 提取开奖日期
                    draw_date_cells = detail.find_all('td', class_='td_w')
                    draw_date = draw_date_cells[1].text.strip() if len(draw_date_cells) > 1 else 'N/A'
                    # 提取开奖号码
                    numbers = [num.text for num in detail.select('.td_w.font_black14b_center')[:6]]
                    # 提取特别号码
                    special_number = detail.select_one('.td_w.font_red14b_center').text.strip() if detail.select_one('.td_w.font_red14b_center') else 'N/A'

                    # 写入文件
                    file.write(f"Open_Date: {draw_date}\n")
                    file.write(f"Number: {', '.join(numbers)}\n")
                    file.write(f"Special: {special_number}\n")
                    file.write("-" * 40 + "\n")
            # 等待兩秒鐘以避免過快請求
                time.sleep(2)

    # 關閉瀏覽器
    driver.quit()

if __name__ == "__main__":
    StartCrawl()
