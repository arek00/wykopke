from datetime import datetime
import time

from main.extract.parsed_content import ParsedContent, ParsedContentFactory, AuthorExtractor, VotersParser, \
    AjaxCallParser, ImageUrlParser, LinksGenerator
from main.extract.raw_post import RawPost
import random

class Post():
    def __init__(self,
                 commentId: str,
                 isOriginalPost: bool,
                 originalPostId: str,
                 author: str,
                 publishDate: datetime,
                 content: str,
                 voters: iter,
                 calls: iter,
                 links: iter,
                 quotes: iter,
                 imageUrl: iter,
                 votesNumber: int):
        self.commentId = commentId
        self.isOp = isOriginalPost
        self.originalPostId = originalPostId
        self.author = author
        self.publishDate = publishDate
        self.postContent = content
        self.voters = voters
        self.calls = calls
        self.links = links
        self.quotes = quotes
        self.imageUrl = imageUrl
        self.votesNumber = votesNumber


def fromRawPosts(rawPosts: list):
    return [fromRawPost(x) for x in rawPosts]

def fromRawPost(post: RawPost) -> Post:
    ajaxParser = AjaxCallParser()

    publishDate = datetime.fromisoformat(post.publishDate)
    parsedContent = ParsedContentFactory.fromRawPost(post)
    author = AuthorExtractor.extractAuthorFromLink(post.author)
    linksGenerator = LinksGenerator()

    linksGenerator.imageAjaxCallLink(post.isOp, post.postId)
    linksGenerator.votersAjaxCallLink(post.isOp, post.postId)


    voters = ajaxParser.parseFromLink(post.votersUrl, VotersParser.extractFromOperations)
    imageUrl = ajaxParser.parseFromLink(post.imageUrl, ImageUrlParser.extractFromOperations)

    sleepTime = random.uniform(0.1, 2.0)
    print("Sleep time: {}".format(sleepTime))
    time.sleep(sleepTime)

    return Post(commentId=post.postId,
                isOriginalPost=post.isOp,
                originalPostId=post.opId,
                author=author,
                publishDate=publishDate,
                content=parsedContent.rawContent,
                calls=parsedContent.calls,
                links=parsedContent.links,
                quotes=parsedContent.quotes,
                votesNumber=int(post.upvotesCount),
                voters=voters,
                imageUrl=imageUrl)
