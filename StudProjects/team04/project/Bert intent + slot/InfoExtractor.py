class SearchParams:
    def __init__(self):
        self.location = None
        self.price = None
        self.date = None

    def extractSearchParams(self, NERdoc):
        for X in NERdoc:
            text, label = X
            print("extract--", text, label)
            if label == "LOCATION":
                self.location = text
            elif label == "MONEY":
                self.price = text
            elif label == "DATE":
                self.date = text

    def getSearchQuery(self):
        ans = [self.location, self.date, self.price]
        return ans

    def resetParams(self): 
        self.location = None
        self.price = None
        self.date = None

    def missingTags(self):
        resp = []
        if self.location is None:
            resp.append("LOCATION")
        if self.price is None:
            resp.append("MONEY")
        if self.date is None:
            resp.append("DATE")

        print(resp)
        return resp

    def printExisting(self):
        answer = "Ok, here's what I understood: "
        if self.location:
            answer += self.location
            if self.price or self.date:
                answer += ", "
        if self.price:
            answer += self.price
            if self.date:
                answer += ", "
        if self.date:
            answer += self.date

        print(answer)

    def get_search_answer(self):
        answer = "Ok, I'm searching for hotels in " + self.location + " in the period " + self.date + " and for the budget of " + self.price
        return answer
