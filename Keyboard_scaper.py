import pandas as pd
from requests_html import HTMLSession
from tqdm import tqdm


page_urls = []
for x in range(1,4):
    page_url = f"https://hacom.vn/ban-phim-co/{x}/?p=399ngan-999ngan&sort=view"
    page_urls.append(page_url)

#Getting links
def get_links(s,page_url):
    page_r = s.get(page_url)
    page_data = page_r.html
    page_data.render(sleep=1,timeout=0)
    container = page_data.find("div.p-component.item.loaded")
    links = []
    for item in tqdm(container):
        link = "https://hacom.vn/" + item.find("h3.p-name",first=True).find("a",first=True).attrs["href"]
        links.append(link)
    return links

#Getting links of each product
def get_product_links(s,page_urls):
    product_links = []
    response = [get_links(s,page_url) for page_url in tqdm(page_urls)]
    for data_list in response:
        product_links = product_links + data_list

    return product_links

#Getting data of product
def get_data(s,url):
    r = s.get(url)
    data = r.html
    title = data.find("div.product_detail-title", first=True).text
    brand = data.find(".p-detail-brand", first=True).find("img", first=True).attrs["alt"]
    Og_price_element = data.find(".price-2021", first=True).find(".giany", first=True)
    Og_price = Og_price_element.text if Og_price_element else None
    Sold_price = data.find(".price-2021", first=True).find(".giakm", first=True).text
    Info = data.find(".product-summary-item-ul.d-flex.flex-wrap.mb-0", first=True).text

    image_src = data.find("div.img-item", first=True).find("img", first=True).attrs["src"]
    header = title.replace("/", "_")
    image_tails = f"\Keyboard_{header}.jpg"
    image_path = r"C:\Users\steph\Desktop\File imagesw" + image_tails
    source = requests.get(image_src)
    with open(image_path, "wb") as f:
        f.write(source.content)

    product = {"Title":title,"Brand":brand,"Original Price": Og_price, "Sold price": Sold_price, "Info": Info, "Image Path":image_path}
    return product


def main():
    s = HTMLSession()
    products_links = get_product_links(s,page_urls)
    products = [get_data(s,url) for url in tqdm(products_links)]
    return products


response = main()

#Saving data
df = pd.DataFrame(response)
df.to_excel(r"C:\Users\steph\Desktop\Practice for Pandas\Keyboard_data.xlsx", index=False)
print("Saved successfully!")
