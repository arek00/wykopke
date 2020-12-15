import requests

from main.extract.post_extractor import PostExtractor

if __name__ == '__main__':
    response = requests.get("https://www.wykop.pl/i/wpis/54222021/zomowcy-znow-to-zrobili-xdddd-ponad-120-milicyjnyc")
    responseBody = response.text
    extractor = PostExtractor(responseBody)

    extracted = extractor.extract()

    for post in extracted:
        print(post.print())