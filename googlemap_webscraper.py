from playwright.sync_api import sync_playwright
from selectolax.parser import HTMLParser
import time
import pandas as pd

search_info = input("What do you want to search for? ")
url = f"https://www.google.com/maps/search/{search_info}/data=!3m1!4b1?entry=ttu"

def get_data(html):
    data = HTMLParser(html)
    container = data.css("div.Nv2PK.THOPZb.CpccDe")
    products = []
    for item in container:
        title = item.css_first("a.hfpxzc").attributes["aria-label"]
        link = item.css_first("a.hfpxzc").attributes["href"]
        rating_element = item.css_first("span.MW4etd")
        rating = rating_element.text() if rating_element else "No reviews"
        info = item.css("div.W4Efsd")[1].css("div.W4Efsd")[1].text()
        products.append({"Title": title, "Link": link, "Rating": rating, "Info": info})
    return products

def scroll_me(url):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        page.set_viewport_size({'width': 1200, 'height': 1000})
        page.goto(url)
        time.sleep(1)
        page.wait_for_load_state("networkidle")
        for i in range(1,12):
            page.click('a[class=hfpxzc]')
            time.sleep(1)
            page.keyboard.press("End")
        html = page.inner_html('#content-container')

        return get_data(html)

def main():
    response = scroll_me(url)
    df = pd.DataFrame(response)
    df.to_excel(r'C:\Users\steph\Desktop\Practice for Pandas\{user_input}.xlsx')
    print("Saved successfully!")

main()
