from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
import os
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager as CM
from selenium.common.exceptions import NoSuchElementException
import time


Username = "214368912"
webdriver_path = r'C:\Users\Neria\Downloads\chromedriver_win32\chromedriver.exe'
options = webdriver.ChromeOptions()
driver = webdriver.Chrome(executable_path=CM().install(), options=options)
time.sleep(5)
url = "https://campus.geva.co.il/Login/Default.php?rp=/Home/router.php"
driver.get(url)

ListOfDataID = [1,19,28,16,12]
ListOfXPath = ['//*[@id="practiceTrees"]/div[1]/div/div[2]/div[1]/div[4]','//*[@id="practiceTrees"]/div[1]/div/div[2]/div[3]/div[4]','//*[@id="practiceTrees"]/div[1]/div/div[2]/div[5]/div[4]',
               '//*[@id="practiceTrees"]/div[2]/div/div[2]/div[1]/div[4]', '//*[@id="practiceTrees"]/div[2]/div/div[2]/div[3]/div[4]']
ListXPaths_Remain_Amount = ['//*[@id="practiceTrees"]/div[1]/div/div[2]/div[1]/div[7]','//*[@id="practiceTrees"]/div[1]/div/div[2]/div[3]/div[7]','//*[@id="practiceTrees"]/div[1]/div/div[2]/div[5]/div[7]',
                            '//*[@id="practiceTrees"]/div[2]/div/div[2]/div[1]/div[7]', '//*[@id="practiceTrees"]/div[2]/div/div[2]/div[3]/div[7]']
XPATH_AmountOfQuestions = '//*[@id="selQuestionCount"]'

XPATH_AmountOfQuestions_Remaining = ['//*[@id="practiceTrees"]/div[1]/div/div[2]/div[1]/div[7]/span','//*[@id="practiceTrees"]/div[1]/div/div[2]/div[3]/div[7]/span'
                                     ,'//*[@id="practiceTrees"]/div[1]/div/div[2]/div[5]/div[7]/span','//*[@id="practiceTrees"]/div[2]/div/div[2]/div[1]/div[7]/span',
                                     '//*[@id="practiceTrees"]/div[2]/div/div[2]/div[3]/div[7]/span']



               
def Login():
    Username_input = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'input[id="login-username"]')))
    Username_input.send_keys(Username)
    Password_input = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'input[id="login-password"]')))
    Password_input.send_keys(Username)
    Submit = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'span[class="newCampusYellowButton"]')))
    Submit.click()
    time.sleep(3)
    Questions()


def Questions():
    i = 0
    while i < len(ListXPaths_Remain_Amount[i]):
        url = "https://campus.geva.co.il/ExtraPractice/DefaultPro.php"
        driver.get(url)
        time.sleep(3)
        #
        Element_Amount = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, XPATH_AmountOfQuestions_Remaining[i])))
        Element_Amount = int(Element_Amount.text)
        CheckBox_element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, ListOfXPath[i])))
        CheckBox_element.click()
        if(Element_Amount == 0):
            i+=1
            continue
        Amount_Questions = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, XPATH_AmountOfQuestions)))
        select = Select(Amount_Questions)
        select.select_by_value('20')
        Submit_Element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="actionOptionsContainer"]/div[1]/div[2]/div/div')))
        Submit_Element.click()
        time.sleep(5)
        ScrapingQuestions_Answers_RightOnes()

#'(נותרו 481 מתוך 541)'
        
def ScrapingQuestions_Answers_RightOnes():
    try:
        for i in range(20):
            try:
                Question = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="imgPracticeQuestion"]')))
                Link = f"{Question.get_attribute('src')}"
                time.sleep(1)
                #//*[@id="btnExplanation"]/div
                Show_Solution_Click = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="btnExplanation"]/div')))
                Show_Solution_Click.click()
                time.sleep(1)
                #//*[@id="dialog-loadexplanation"]/div[3]/div[1]
                Do_It = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="dialog-loadexplanation"]/div[3]/div[1]')))
                Do_It.click()
                Right_Solution_Picture = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="imgPracticeExplanation"]')))
                Right_Solution_Picture = f"{Right_Solution_Picture.get_attribute('src')}"
                time.sleep(1)
                #/html/body/div[3]/div/div[2]/div[2]/div[2]/div[4]/div[1]
                time.sleep(1)
                #//*[@id="btnCheckAnswer"]/div
                ShowRightAnswer = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="btnShowAnswer"]/div')))
                ShowRightAnswer.click()
                time.sleep(1)
                #Right Solution Wihtout pressing
                Right_Solution = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div[class="practice-control-answer answer-state-correct"]')))
                Right_Solution = Right_Solution.text
                with open("Questions_Link.txt", "a") as file:
                    file.write(str(Link) + '\n')
                with open("Right_Solution_Picture.txt", "a") as file:
                    file.write(str(Right_Solution_Picture) + '\n')
                with open("Right_Solution_Number.txt", "a") as file:
                    file.write(str(Right_Solution) + '\n')
                Next_Question = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH,'//*[@id="btnJustNext"]/div')))
                Next_Question.click()
                time.sleep(4)
            except Exception as ex:
                continue
    except Exception as ex: 
        return

Login()






    





