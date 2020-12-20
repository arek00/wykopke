import requests

from main.extract.post import fromRawPosts, Post
from main.extract.post_html_extractor import PostExtractor
from main.extract.parsed_content import ParsedContent, ParsedContentFactory

def printPost(post: Post):
    """
    ###
    Post id: {}
    Reply to post: {}
    Published at: {}
    Author: {}
    Upvotes: {}
    
    Post content: {}
    """.format(post.commentId,
               post.originalPostId,
               post.publishDate,
               post.author,
               post.votesNumber,
               post.postContent)



if __name__ == '__main__':
    response = requests.get("https://www.wykop.pl/i/wpis/54222021/zomowcy-znow-to-zrobili-xdddd-ponad-120-milicyjnyc")
    responseBody = response.text
    extractor = PostExtractor(responseBody)

    extracted = extractor.extract()

    posts = fromRawPosts(extracted)


