from bs4 import BeautifulSoup, Tag, ResultSet

from main.extract.rawpost import RawPost
from main.utils import Optional


class PostExtractor():

    def __init__(self, source: str):
        self.parser = BeautifulSoup(source, 'html.parser')

    def extract(self):
        op = self.__extractOriginalPost()
        replies = self.__extractReplies()
        messages = []

        messages.extend(self.__extractPosts(op, self.__extractPost))
        messages.extend(self.__extractPosts(replies, self.__extractPost))

        return messages

    def __extractPosts(self, tags: ResultSet, func):
        posts = []
        for tag in tags:
            posts.append(func(tag))
        return posts

    def __extractOriginalPost(self):
        return self.parser.find_all("li", class_="entry")

    def __extractReplies(self):
        return Optional.of(self.parser.find("ul", class_="sub")) \
            .map(lambda entry: entry.find_all("li")) \
            .get()

    def __extractPost(self, entry: Tag):
        content = self.__extractContent(entry)
        author = self.__extractAuthorUrl(entry)
        publishDate = self.__extractPublishDate(entry)
        postId = self.__extractPostId(entry)
        postUrl = self.__extractPostUrl(entry)
        upvotes = self.__extractUpvotesCount(entry)
        imageUrl = self.__extractImageUrl(entry)
        votersUrl = self.__extractVotersUrl(entry)

        return RawPost(content, author, publishDate, postId, postUrl, upvotes, imageUrl, votersUrl)

    def __extractContent(self, entry: Tag):
        return entry.find("div", class_="text")

    def __extractAuthorUrl(self, entry: Tag):
        return Optional.of(entry.find("a", class_="profile")) \
            .map(lambda entry: entry.get("href")) \
            .get()

    def __extractPublishDate(self, entry: Tag):
        return Optional.of(entry.find("time")) \
            .map(lambda entry: entry.get('datetime')) \
            .get()

    def __extractPostId(self, entry: Tag):
        return Optional.of(entry.find("div", class_="wblock")) \
            .map(lambda entry: entry.get("data-id")) \
            .get()

    def __extractPostUrl(self, entry: Tag):
        return Optional.of(entry.find("time")) \
            .map(lambda entry: entry.parent) \
            .map(lambda entry: entry.parent) \
            .map(lambda entry: entry.get("href")) \
            .get()

    def __extractUpvotesCount(self, entry: Tag):
        return Optional.of(entry.find('p', class_="vC")) \
            .map(lambda entry: entry.get("data-vc")) \
            .get()

    def __extractImageUrl(self, entry):
        return Optional.of(entry.find("div", class_="media-content")) \
            .map(lambda entry: entry.find("a", class_="ajax")) \
            .map(lambda entry: entry.get("data-ajaxurl")) \
            .get()

    def __extractVotersUrl(self, entry):
        return Optional.of(entry.find("div", class_='voters-list')) \
            .map(lambda entry: entry.find("a", class_="showVoters")) \
            .map(lambda entry: entry.get("data-ajaxurl")) \
            .get()
