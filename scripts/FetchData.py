import requests
from bs4 import BeautifulSoup
import os
from selenium import webdriver
import urllib.parse
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys


USER_NAME = "Knut Knutsen"
INSTITUTION = "Høgskulen på vestlandet"


def download_png_images(url, save_folder="images"):
    os.makedirs(save_folder, exist_ok=True)
    driver = webdriver.Chrome()
    # Vet ikke helt hvor lovlig dette er ^.-
    try:
        driver.get(url)
        time.sleep(2)

        username_field = driver.find_element(By.ID, "name")
        username_field.send_keys(USER_NAME)

        institution_field = driver.find_element(By.ID, "institution")
        institution_field.send_keys(INSTITUTION)

        institution_field.send_keys(Keys.RETURN)
        time.sleep(2)
        page_source = driver.page_source
    finally:
        driver.quit()
    soup = BeautifulSoup(page_source, "html.parser")

    keogramDiv = soup.find("div", {"id": "keogramDiv"})
    if not keogramDiv:
        print(f"No such div found")
        return

    table = keogramDiv.find("table")
    if not table:
        print(f"No table found")
        return

    for row in table.find_all("tr"):
        img = row.find("img")
        if img and img.get("src"):
            imgUrl = urllib.parse.urljoin(url, img["src"])
            imgData = requests.get(imgUrl).content
            imgName = os.path.join(save_folder, os.path.basename(imgUrl))
            with open(imgName, "wb") as imgFile:
                imgFile.write(imgData)
                print(f"Downloaded {imgName}")


download_png_images("http://tid.uio.no/plasma/aurora/data.php")
