import random
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from bs4 import BeautifulSoup
from pynput.keyboard import Key, Controller
from pyshadow.main import Shadow



def guessLetterCounter(word1,i): 
    sum=0
    for j in range(5):
        if word1[j]==word1[i] and feedback[j]!="absent" :
            sum=sum+1
    return sum

def wordletterCounter(word2,i):
    sum=0
    for j in range(5):
        if word2[j]==guess[i]:
            sum=sum+1
    return sum  



keyboard = Controller()
driver = webdriver.Chrome()
driver.get("https://www.powerlanguage.co.uk/wordle/")
assert "Wordle" in driver.title

driver.find_element(By.XPATH,"//html").click()#to close the tutorial window


f=open(r"words.txt")

words=[i.strip("\n") for i in f.readlines()]



tries=0
time.sleep(5)
control=1

shadow = Shadow(driver) # this is necesarry for shadow DOM elements
while tries<6 and control==1:
    control=0
    feedback=[]    
    guess=words[random.randint( 0,len(words)-1)]
    
    tries=tries+1
    
    keyboard.type(guess)
    keyboard.press(Key.enter)

    keyboard.release(Key.enter)
    
    time.sleep(7)
    try: 
        button=shadow.find_element("#share-button")
        button.click()
  
    except NoSuchElementException: # It gives us NoSuchElementException if there is no share button available yet, in another meaning if the game is still on
        control=1

        for j in range(5):
            elementss = shadow.find_elements("div > game-tile:nth-child("+str(j+1)+")") #selector for letters
            
            feedback.append(str(elementss[tries-1].get_attribute("evaluation"))) #basically color of letters (green,yelllow,black)
    


        for i in range(5):
            if feedback[i]=="correct": #Green letter
                words=[word for word in words if word[i]==guess[i]]

                
            elif feedback[i]=="present":        #yellow letter
                words=[word for word in words if guess[i] in word and word[i]!=guess[i]]
            
                
            
            elif feedback[i]=="absent": #black letter
                #this might need editing

                words=[word for word in words if guessLetterCounter(guess,i)==wordletterCounter(word,i)]
        
        
                
        

driver.close()