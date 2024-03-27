import pytest
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.action_chains import ActionChains

class Test_Sauce:   
     
    #pytest tarafından tanımlanan bir method 
    #her test öncesi otomatik olarak çalıştırılır
     def setup_method(self):
        self.driver = webdriver.Chrome(ChromeDriverManager().install())
        self.driver.maximize_window()
        self.driver.get("https://www.saucedemo.com/")

     #her test bitiminde çalışacak fonksiyon
     def teardown_method(self):
        self.driver.quit()

     
     @pytest.mark.parametrize("username,password",[("1","1"),("abc","123"),("deneme","secret_sauce")])
     def test_invalid_login(self,username,password):
        userNameInput = WebDriverWait(self.driver,5).until(ec.visibility_of_element_located((By.ID,"user-name")))
        passwordInput = WebDriverWait(self.driver,5).until(ec.visibility_of_element_located((By.ID,"password")))
        userNameInput.send_keys(username)
        passwordInput.send_keys(password)
        loginButton = WebDriverWait(self.driver,5).until(ec.visibility_of_element_located((By.ID,"login-button")))
        loginButton.click()
        errorMessage =WebDriverWait(self.driver,5).until(ec.visibility_of_element_located((By.XPATH,"//*[@id='login_button_container']/div/form/div[3]/h3")))
        assert errorMessage.text == "Epic sadface: Username and password do not match any user in this service"

     def test_empty_username_password(self):
         self.driver.get("https://www.saucedemo.com./")
         userNameInput = WebDriverWait(self.driver,5).until(ec.visibility_of_element_located((By.ID,"user-name")))
         passwordInput = WebDriverWait(self.driver,5).until(ec.visibility_of_element_located((By.ID,"password")))
         actions = ActionChains(self.driver)
         actions.send_keys_to_element(userNameInput,"")
         actions.send_keys_to_element(passwordInput,"")
         actions.perform() #depoladığım aksiyonları çalıştır
         loginButton = WebDriverWait(self.driver,5).until(ec.visibility_of_element_located((By.ID,"login-button")))
         loginButton.click()
         errorMessage = WebDriverWait(self.driver,5).until(ec.visibility_of_element_located((By.XPATH,"//*[@id='login_button_container']/div/form/div[3]/h3")))
         print(errorMessage.text)
         testResult = errorMessage.text == "Epic sadface: Username is required"
         print(f"TEST SONUCU: {testResult}")

     def test_empty_password(self):
         self.driver.get("https://www.saucedemo.com./")
         userNameInput = WebDriverWait(self.driver,5).until(ec.visibility_of_element_located((By.ID,"user-name")))
         passwordInput = WebDriverWait(self.driver,5).until(ec.visibility_of_element_located((By.ID,"password")))
         actions = ActionChains(self.driver)
         actions.send_keys_to_element(userNameInput,"1")
         actions.send_keys_to_element(passwordInput,"")
         actions.perform()
         loginButton = WebDriverWait(self.driver,5).until(ec.visibility_of_element_located((By.ID,"login-button")))
         loginButton.click()
         errorMessage = WebDriverWait(self.driver,5).until(ec.visibility_of_element_located((By.XPATH,"//*[@id='login_button_container']/div/form/div[3]/h3")))
         print(errorMessage.text)
         testResult = errorMessage.text == "Epic sadface: Password is required"
         print(f"TEST SONUCU: {testResult}")
    
     def test_user_locked_out(self):
         self.driver.get("https://www.saucedemo.com./")
         userNameInput = WebDriverWait(self.driver,5).until(ec.visibility_of_element_located((By.ID,"user-name")))
         passwordInput = WebDriverWait(self.driver,5).until(ec.visibility_of_element_located((By.ID,"password")))
         actions = ActionChains(self.driver)
         actions.send_keys_to_element(userNameInput,"locked_out_user")
         actions.send_keys_to_element(passwordInput,"secret_sauce")
         actions.perform()
         loginButton = WebDriverWait(self.driver,5).until(ec.visibility_of_element_located((By.ID,"login-button")))
         loginButton.click()
         errorMessage = WebDriverWait(self.driver,5).until(ec.visibility_of_element_located((By.XPATH,"//*[@id='login_button_container']/div/form/div[3]/h3")))
         print(errorMessage.text)
         testResult = errorMessage.text == "Epic sadface: Sorry, this user has been locked out."
         print(f"TEST SONUCU: {testResult}")

     def test_valid_login(self):
         self.driver.get("https://www.saucedemo.com./")
         userNameInput = WebDriverWait(self.driver,5).until(ec.visibility_of_element_located((By.ID,"user-name")))
         passwordInput = WebDriverWait(self.driver,5).until(ec.visibility_of_element_located((By.ID,"password")))
         actions = ActionChains(self.driver)
         actions.send_keys_to_element(userNameInput,"standard_user")
         actions.send_keys_to_element(passwordInput,"secret_sauce")
         actions.perform()
         loginButton = WebDriverWait(self.driver,5).until(ec.visibility_of_element_located((By.ID,"login-button")))
         loginButton.click()
         baslik = WebDriverWait(self.driver,5).until(ec.visibility_of_element_located((By.XPATH,"//*[@id='header_container']/div[1]/div[2]/div")))
         assert baslik.text == "Swag Labs"

     def add_to_basket(self):
         self.driver.get("https://www.saucedemo.com./")
         userNameInput = WebDriverWait(self.driver,5).until(ec.visibility_of_element_located((By.ID,"user-name")))
         passwordInput = WebDriverWait(self.driver,5).until(ec.visibility_of_element_located((By.ID,"password")))
         actions = ActionChains(self.driver)
         actions.send_keys_to_element(userNameInput,"standard_user")
         actions.send_keys_to_element(passwordInput,"secret_sauce")
         actions.perform()
         loginButton = WebDriverWait(self.driver,5).until(ec.visibility_of_element_located((By.ID,"login-button")))
         loginButton.click()
         addToCard = WebDriverWait(self.driver,5).until(ec.visibility_of_element_located((By.ID,"add-to-cart-sauce-labs-bike-light"))) 
         addToCard.click()
         basket_piece = WebDriverWait(self.driver,5).until(ec.visibility_of_element_located((By.CSS_SELECTOR,"span.shopping_cart_badge")))
         basket_piece.text > "0"
         print(f"Ürün başarıyla sepete eklendi")

     def remove_to_basket(self):
         self.driver.get("https://www.saucedemo.com./")
         userNameInput = WebDriverWait(self.driver,5).until(ec.visibility_of_element_located((By.ID,"user-name")))
         passwordInput = WebDriverWait(self.driver,5).until(ec.visibility_of_element_located((By.ID,"password")))
         actions = ActionChains(self.driver)
         actions.send_keys_to_element(userNameInput,"standard_user")
         actions.send_keys_to_element(passwordInput,"secret_sauce")
         actions.perform()
         loginButton = WebDriverWait(self.driver,5).until(ec.visibility_of_element_located((By.ID,"login-button")))
         loginButton.click()
         addToCard = WebDriverWait(self.driver,5).until(ec.visibility_of_element_located((By.ID,"add-to-cart-sauce-labs-bike-light"))) 
         addToCard.click()
         basket_piece = WebDriverWait(self.driver,5).until(ec.visibility_of_element_located((By.CSS_SELECTOR,"span.shopping_cart_badge")))
         basket_piece.text > "0"
         print(f"Ürün başarıyla sepete eklendi, sepetteki ürün sayısı: {basket_piece.text}")
         remove = WebDriverWait(self.driver,5).until(ec.visibility_of_element_located((By.ID,"remove-sauce-labs-bike-light"))) 
         remove.click()
         print(f"Ürün başarıyla sepetten çıkarıldı.")

     def product_details_page(self):
         self.driver.get("https://www.saucedemo.com./")
         userNameInput = WebDriverWait(self.driver,5).until(ec.visibility_of_element_located((By.ID,"user-name")))
         passwordInput = WebDriverWait(self.driver,5).until(ec.visibility_of_element_located((By.ID,"password")))
         actions = ActionChains(self.driver)
         actions.send_keys_to_element(userNameInput,"standard_user")
         actions.send_keys_to_element(passwordInput,"secret_sauce")
         actions.perform()
         loginButton = WebDriverWait(self.driver,5).until(ec.visibility_of_element_located((By.ID,"login-button")))
         loginButton.click()
         product = WebDriverWait(self.driver,5).until(ec.visibility_of_element_located((By.XPATH,"//*[@id='item_4_title_link']/div")))
         product.click()
         product_name = "Sauce Labs Backpack"
         product_details_name = WebDriverWait(self.driver,5).until(ec.visibility_of_element_located((By.XPATH,"//*[@id='inventory_item_container']/div/div/div[2]/div[1]")))
         product_details_name.text == product_name
         print(f"Erişilen ürün detay sayfasının adı: {product_details_name.text}")  




         
         
         
         

        



#testClass = Test_Sauce()
#testClass.setup_method()
#testClass.test_invalid_login()
#testClass.teardown_method()
#testClass.test_empty_password()
#testClass.test_user_locked_out()
#testClass.test_valid_login()
