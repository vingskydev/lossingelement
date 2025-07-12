from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time
import os

TEXT_TO_POST = "Тест"  # Текст для публикации
ELEMSOCIAL_URL = "https://elemsocial.com"
DELAY = 5
ATTEMPTS = 3  # Количество повторений
PAUSE_BETWEEN_POSTS = 16  # Пауза между постами в секундах (НЕ МЕНЯТЬ! В ELEMENT ОГРАНИЧЕНИЕ 15 СЕК НА КАЖДЫЙ ПОСТ)

ATTACH_PHOTO = True  # True = включить прикрепление фото, False = выключить
PHOTO_PATH = "C:/Users/typeermain/Downloads/photo_2025-07-12_13-24-34.jpg"

def post_to_elemsocial():
    driver = webdriver.Chrome()
    
    try:
        print(f"Открываю {ELEMSOCIAL_URL} - пожалуйста, авторизуйтесь...")
        driver.get(ELEMSOCIAL_URL)
        input("После авторизации нажмите Enter в этом окне, чтобы продолжить...")
        
        for i in range(1, ATTEMPTS + 1):
            try:
                print(f"\nПопытка публикации #{i} из {ATTEMPTS}...")
                
                driver.refresh()
                
                textarea = WebDriverWait(driver, DELAY).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "textarea.UI-Input"))
                )

                textarea.clear()
                textarea.send_keys(TEXT_TO_POST)
                
                if ATTACH_PHOTO and PHOTO_PATH and os.path.exists(PHOTO_PATH):
                    try:
                        print("Пытаюсь прикрепить изображение...")
                        file_input = driver.find_element(By.CSS_SELECTOR, 'input[type="file"]')
                        file_input.send_keys(PHOTO_PATH)
                        print("Изображение успешно прикреплено")
                        time.sleep(3)
                    except Exception as e:
                        print(f"Ошибка при прикреплении фото: {str(e)}")
                
                send_button = WebDriverWait(driver, DELAY).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, "button.UI-FormButton.Send"))
                )
                send_button.click()
                
                print(f"Публикация #{i} успешно отправлена!")
                
                if i < ATTEMPTS:
                    print(f"Ожидание {PAUSE_BETWEEN_POSTS} секунд перед следующим постом...")
                    time.sleep(PAUSE_BETWEEN_POSTS)
                    
            except Exception as e:
                print(f"Ошибка при попытке #{i}: {str(e)}")
                time.sleep(5)
        
        print("\nВсе публикации завершены!")
        
    except Exception as e:
        print(f"Критическая ошибка: {str(e)}")
    finally:
        driver.quit()

if __name__ == "__main__":
    if ATTACH_PHOTO and (not PHOTO_PATH or not os.path.exists(PHOTO_PATH)):
        print("Ошибка: Указан неверный путь к изображению или файл не существует!")
    else:
        post_to_elemsocial()