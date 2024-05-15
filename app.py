from bs4 import BeautifulSoup
import requests
import pandas as pd
import warnings
warnings.filterwarnings("ignore")

User_Agent = "" #  Add you user agent

headers = ({'User-Agent': User_Agent, 'Accept-Language': 'en-US, en;q=0.5'})

df = pd.DataFrame(columns=["product_name", "main_category", "sub_category_1", "sub_category_2", "product_price", "product_rating", "user_rating", "comment_title", "comment_content"])

for i in range(1, 2):
        
    url = 'https://www.jumia.com.eg/phones-tablets/?sort=rating&page=' + str(i) + '#catalog-listing'

    webpage = requests.get(url, headers=headers)

    if webpage.status_code == 200:
        soup = BeautifulSoup(webpage.content, "html.parser")
        links = soup.find_all("a", class_="core")

        for link in links:
            link = link.get("href")
            product_url = "https://www.jumia.com.eg" + link
            product_page = requests.get(product_url, headers=headers)

            if product_page.status_code == 200:
                product_website_name = "Jumia"
                product_soup = BeautifulSoup(product_page.content, "html.parser")
                product_name = product_soup.find("h1", class_="-fs20 -pts -pbxs").get_text().strip()
                product_price = product_soup.find("span", class_="-b -ubpt -tal -fs24 -prxs").get_text().strip()
                product_categorys = product_soup.find_all("a", class_="cbs")
                main_category = product_categorys[1].get_text().strip()
                sub_category_1 = product_categorys[2].get_text().strip()
                if len(product_categorys) >= 4:
                    sub_category_2 = product_categorys[3].get_text().strip()
                else:
                    sub_category_2 = None
                product_rating = product_soup.find("div", class_="stars _m _al").get_text().strip()

                rev_element = product_soup.find("a", class_="btn _def _ti -mhs -fsh0")
                if rev_element is not None:
                    rev = rev_element.get('href')
                    reviews_url = "https://www.jumia.com.eg" + rev
                    reviews_page = requests.get(reviews_url, headers=headers)

                    if reviews_page.status_code == 200:
                        reviews_soup = BeautifulSoup(reviews_page.content, "html.parser")
                        articles = reviews_soup.find_all("article", class_="-pvs -hr _bet")

                        for article in articles:    
                            user_rating = None
                            comment_content = None
                            comment_title = None
                            user_rating = article.find("div", class_="stars _m _al -mvs").get_text().strip()
                            comment_title = article.find("h3", class_="-m -fs16 -pvs").get_text().strip()
                            comment_content = article.find("p", class_="-pvs").get_text().strip()
                        
                            df = df.append({
                                "product_name": product_name,
                                "main_category": main_category,
                                "sub_category_1": sub_category_1,
                                "sub_category_2": sub_category_2,
                                "product_price": product_price,
                                "product_rating": product_rating,
                                "user_rating": user_rating,
                                "comment_title": comment_title,
                                "comment_content": comment_content
                            }, ignore_index=True)

df.to_csv("jumia_reviews.csv", mode="a", header=False)
print("Done")
