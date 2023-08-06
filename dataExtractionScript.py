import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import getpass
import json
import csv

# Created the object to use the webdriver's options
chrome_options = Options()

# Creates a Chrome Object
browser = webdriver.Chrome(options=chrome_options)
browser.set_window_size(1300, 1300)

# Opens the login page
browser.get("https://portal.brasiljunior.org.br/")

# Logs in
browser.find_element_by_name("emailOrCpf").send_keys("EMAIL")
browser.find_element_by_name("password").send_keys("SENHA")
browser.find_element_by_xpath("//button[contains(text(), 'Entrar')]").click()

time.sleep(3)

browser.find_element_by_xpath("//span[contains(text(), 'Portal')]").click()
time.sleep(2)

# Choose how many pages to extract from
pages = 50
itenspp = 20

EJs = {}
# Creates loop to write the CSV and extract data.
with open('EJs2.csv', 'w', newline='') as file:
    # Create Writer object to write lines
    writer = csv.writer(file)
    # Create headers
    writer.writerow(["Nome", "Faturamento", "Cluster","Federacao","Projetos"])
    for i in range(pages-1):
        # iterates through the pages
        browser.get(f"https://portal.brasiljunior.org.br/dados-da-rede/2021?page={i+1}&q%5Bs%5D=revenue+desc")
        time.sleep(1)
        for z in range(itenspp-1):
            # Iterates through the list inside page
            nome = browser.find_element_by_xpath(f"//*[@id='wrapper']/div[2]/div/div[2]/div/div/div/div[{2+z}]/div[1]/a").text
            Faturamento = browser.find_element_by_xpath(f"//*[@id='wrapper']/div[2]/div/div[2]/div/div/div/div[{2+z}]/div[2]/div[6]").text
            Federacao = browser.find_element_by_xpath(f"//*[@id='wrapper']/div[2]/div/div[2]/div/div/div/div[{2+z}]/div[2]/div[1]/strong").text
            Cluster = browser.find_element_by_xpath(f"//*[@id='wrapper']/div[2]/div/div[2]/div/div/div/div[{2+z}]/div[2]/div[2]").text
            Projetos = browser.find_element_by_xpath(f"//*[@id='wrapper']/div[2]/div/div[2]/div/div/div/div[{2+z}]/div[2]/div[5]").text

            Faturamento = Faturamento.replace("R$ ","")
            Faturamento = Faturamento.replace(".","")
            Faturamento = Faturamento.replace(",",".")
            nome = nome.replace("ú","u")
            # Adds line to file
            writer.writerow([nome, Faturamento, Cluster,Federacao,Projetos])

time.sleep(5)
browser.quit()