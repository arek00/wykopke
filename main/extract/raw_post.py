class RawPost:
    def __init__(self,
                 content: str,
                 author: str,
                 publishDate: str,
                 postId: str,
                 postUrl: str,
                 upvotesCount: str,
                 imageUrl: str,
                 votersUrl: str):
        self.content = content
        self.author = author
        self.publishDate = publishDate
        self.postId = postId
        self.postUrl = postUrl
        self.upvotesCount = upvotesCount
        self.imageUrl = imageUrl
        self.votersUrl = votersUrl

    def print(self):
        return """Entry id:{}
            Published: {}
            Original poster: {}
            Upvotes: {}
            imageUrl: {}
            votersUrl: {}
            postUrl: {}""" \
            .format(self.postId,
                    self.publishDate,
                    self.author,
                    self.upvotesCount,
                    self.imageUrl,
                    self.votersUrl,
                    self.postUrl)


    def setOriginalPostId(self, originalPostId: str):
        self.opId = originalPostId

    def setIsOriginalPost(self, isOriginalPost: bool):
        self.isOp = isOriginalPost