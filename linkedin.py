from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import linkedin.cred as cred
import random, sheet.Sheets_Getter as SG
options = webdriver.ChromeOptions()
options.add_experimental_option("useAutomationExtension", False)
options.add_argument("--user-data-dir=chrome/~/Library/Application Support/Google/Chrome")
options.add_argument('--profile-directory=Étienne Giroux-Paquet')
options.add_experimental_option("excludeSwitches",["enable-automation"])
driver = webdriver.Chrome(options)
__UserState={"Adolf":0}
def First_Login():
    driver.get("https://www.linkedin.com/login")
    #print(driver.get_credentials())
    driver.find_element("id", "username").send_keys(cred.username)
    time.sleep(4)
    driver.find_element("id", "password").send_keys(cred.password)
    submit_button = driver.find_element(by="xpath", value="//*[@type=\"submit\"]")
    time.sleep(1)
    submit_button.click()
    time.sleep(10)
def get6thtype():
    a=driver.find_elements(By.CLASS_NAME, "artdeco-button")[6].accessible_name
    if(a.startswith("Follow")):
        return "Follow"
    elif(a.startswith("Invite")):
        return "Invite"
def isInvite( a):
    if(a.startswith("Invite")):
        return 1
    return 0
def write():
    f=open("linkedin/UserState","w+")
    for i in __UserState:
        f.write(str(__UserState[i])+" "+i+",")
def read():
    try:
        _strfirst,_strafter="",""
        state=0
        with open('linkedin/UserState') as openfileobject:
            for line in openfileobject:
                    for i in line:
                        if(i==' '):
                            state=1
                        elif (i==','):
                            __UserState[_strafter]=int(_strfirst)
                            _strafter=""
                            _strfirst=""
                            state=0
                        elif(state==1):
                            _strafter+=i
                        else:
                            _strfirst+=i
    except:
        print("creating state")
def contacting(url="https://www.linkedin.com/in/ravi-narayanan-0a235b58/",custom_message="hi!"):
    time.sleep(1)
    driver.get(url)
    #print(driver.get_cookies()[3])
    time.sleep(4)
    try:
        if(get6thtype()=="Invite"):
            driver.find_elements(By.CLASS_NAME, "artdeco-button")[6].click() #contact  button
            time.sleep(10)
        else:
            try:
                driver.find_elements(By.CLASS_NAME, "artdeco-dropdown__trigger--placement-bottom")[2].click()
                try:
                    for i in range(len( driver.find_elements(By.CLASS_NAME, "artdeco-dropdown__item"))):
                        if(isInvite(driver.find_elements(By.CLASS_NAME, "artdeco-dropdown__item")[i].accessible_name)):
                            driver.find_elements(By.CLASS_NAME, "artdeco-dropdown__item")[i].click()
                except Exception as e:
                    print(e)
            except:
                print("didnt.")
        time.sleep(2)
        try:
            driver.find_element(By.CLASS_NAME,"mr1").click() #send_custom message
            time.sleep(2)
            try:
                driver.find_element(By.ID,"custom-message").send_keys(custom_message)
                time.sleep(3)
                try:
                    driver.find_element(By.CLASS_NAME,"ml1").click()
                    __UserState[url]=1
                except Exception as e:
                    __UserState[url]=-1
            except Exception as e:
                print(e)
                __UserState[url]=1
        except Exception as e:
            print(e)
            __UserState[url]=-1
        
    except Exception as e:
        print("didn't find connect")
        print(e)
if __name__=="__main__":
    read()
    SG.Download()
    triedcounter=0
    for i in SG.__sheet:
        if not i[0] in __UserState:
            contacting(i[0],i[3])
            triedcounter+=1
            print("tried: "+i[0])
            time.sleep(random.randrange(2*60,15*60))
        else:
            print("already contacted: "+i[0])
        if(triedcounter>=20):
            break
    write()
driver.quit()