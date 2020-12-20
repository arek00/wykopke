import json

import requests
from bs4 import BeautifulSoup, Tag

from main.extract.raw_post import RawPost


class ParsedContent():
    def __init__(self, rawContent, calls, hashtags, links, quotes):
        self.rawContent = rawContent
        self.calls = calls
        self.hashtags = hashtags
        self.links = links
        self.quotes = quotes

    def print(self):
        return """Post content:
        {}
        
        Number of calls within post: {}
        Hashtags used: {}
        Links posted: {}
        quotes used: {}
        Hashtags: {}
        quotes: {}    
        calls: {}    
        links: {}    
        
        """.format(self.rawContent,
                   len(self.calls),
                   len(self.hashtags),
                   len(self.links),
                   len(self.quotes),
                   str(self.hashtags),
                   str(self.quotes),
                   str(self.calls),
                   str(self.links))


class ParsedContentFactory():
    @staticmethod
    def fromRawPost(rawPost: RawPost) -> ParsedContent:
        return ParsedContentFactory.parseContent(rawPost.content)

    @staticmethod
    def parseContent(content: str):
        parser = BeautifulSoup(content, 'html.parser')
        textParagraph = parser.find("p")

        calls = ParsedContentFactory.findAllCalls(textParagraph)
        hashtags = ParsedContentFactory.findAllHashtags(textParagraph)
        links = ParsedContentFactory.findAllLinks(textParagraph)
        ParsedContentFactory.unwrapLinks(textParagraph)
        quotes = ParsedContentFactory.findAllQuotations(textParagraph)
        ParsedContentFactory.unwrapQuotes(textParagraph)

        rawContent = textParagraph.getText()

        return ParsedContent(rawContent=rawContent, calls=calls, hashtags=hashtags, links=links, quotes=quotes)

    @staticmethod
    def findAllCalls(textParagraph: Tag):
        calls = []
        for call in textParagraph.find_all("a", class_="showProfileSummary"):
            calls.append(call.getText())

        return calls

    @staticmethod
    def findAllHashtags(textParagraph: Tag):
        hashtags = []
        for tag in textParagraph.find_all("a", class_="showTagSummary"):
            hashtags.append(tag.getText())

        return hashtags

    @staticmethod
    def findAllQuotations(textParagraph: Tag):
        quotes = []
        for quote in textParagraph.find_all("cite"):
            quotes.append(quote.getText())
        return quotes

    @staticmethod
    def findAllLinks(textParagraph: Tag):
        links = []
        for link in textParagraph.find_all("a", class_=None):
            links.append(link.getText())
        return links

    @staticmethod
    def unwrapLinks(textParagraph: Tag):
        for link in textParagraph.find_all("a"):
            link = link.unwrap()

    @staticmethod
    def unwrapQuotes(textParagraph: Tag):
        for quote in textParagraph.find_all("cite"):
            quote = quote.unwrap()


class AuthorExtractor():
    @staticmethod
    def extractAuthorFromLink(authorProfileLink: str):
        if (authorProfileLink.endswith("/")):
            authorProfileLink = authorProfileLink[0:-1]

        return authorProfileLink.split("/")[-1]


class LinksGenerator():
    __imageUrlPattern = "https://www.wykop.pl/i/ajax2/embed/html/type/entry{}/id/{}"
    __votersUrlPattern = "https://www.wykop.pl/i/ajax2/wpis/{}/{}"

    def imageAjaxCallLink(self, isOp: bool, commentId: str):
        entryTypeStr = ""

        if(not isOp):
            entryTypeStr = "comment"

        return self.__imageUrlPattern.format(entryTypeStr, commentId)

    def votersAjaxCallLink(self, isOp: bool, commentId: str):
        type = "upvoters"

        if(not isOp):
            type = "commentUpvoters"

        return self.__votersUrlPattern.format(type, commentId)


class AjaxCallParser():
    def __removeForLoop(self, responseText: str):
        loopText = "for(;;);"

        if (responseText.startswith(loopText)):
            return responseText.replace(loopText, "")
        else:
            return responseText

    def __extractOperations(self, loadedJson):
        return list(map(lambda operation: operation['html'], loadedJson['operations']))

    def parseFromLink(self, link: str, extractFunc):
        if(link):
            print("Get ajax call data from: {}".format(link))
            response = requests.get(link)
            jsonString = self.__removeForLoop(response.text)
            operations = self.__extractOperations(json.loads(jsonString))

            return extractFunc(operations)
        else:
            return None

class VotersParser:
    @staticmethod
    def extractFromOperations(operations):
        voters = []
        for operation in operations:
            parser = BeautifulSoup(operation, 'html.parser')
            links = parser.find_all('a', class_="link")

            for link in links:
                voters.append(link.getText())

        return voters

class ImageUrlParser:
    @staticmethod
    def extractFromOperations(operations):
        imageUrls = []

        for operation in operations:
            parser = BeautifulSoup(operation, 'html.parser')
            imageUrls.append(parser.find('a', class_="").get("href"))
        return imageUrls
