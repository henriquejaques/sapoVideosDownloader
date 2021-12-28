from selenium import webdriver
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
from bs4 import BeautifulSoup as bs
import requests
import time


def download_file(filename, download_link):
    path_benji = "Anime/Oliver e Benji/"
    path_samurai = "Anime/Samurai X/"
    payload = {}
    headers = {}
    with requests.request(
        "GET", download_link, headers=headers, data=payload, stream=True
    ) as r:
        r.raise_for_status()
        if "Oliver" in filename:
            path = path_benji + filename + ".mp4"
        else:
            path = path_samurai + filename + ".mp4"
        with open(path, "wb") as f:
            for chunk in r.iter_content(chunk_size=8192):
                # If you have chunk encoded response uncomment if
                # and set chunk_size parameter to None.
                # if chunk:
                f.write(chunk)


def main():
    options = Options()
    driver = webdriver.Firefox(
        options=options, executable_path=GeckoDriverManager().install()
    )
    driver.get("http://videos.sapo.pt/mariodgarces2/ultimos")
    wait = WebDriverWait(driver, 30).until(
        EC.element_to_be_clickable(
            (By.XPATH, "/html/body/div[5]/div/section/ul/li[1]/div/div/a[1]")
        )
    )
    body = driver.find_element(
        "xpath",
        '//*[@id="sapo"]',
    )
    # body.click()
    for i in range(25):
        time.sleep(0.5)
        body.send_keys(Keys.PAGE_DOWN)
    html = driver.page_source
    driver.quit()
    soup = bs(html, "html.parser")
    links = soup.find_all("a", attrs={"class": "title"})
    download_links = []
    for link in links:
        if "Oliver" in link.text or "Samurai" in link.text:
            download_links.append([link.attrs["title"], link.attrs["href"]])
    for link in download_links:
        download_link = f"http://rd.videos.sapo.pt{link[1]}/mov/1"
        filename = link[0]
        download_file(filename, download_link)


if __name__ == "__main__":
    main()
