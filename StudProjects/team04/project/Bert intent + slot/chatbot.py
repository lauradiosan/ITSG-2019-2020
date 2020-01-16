from InfoExtractor import SearchParams
from Responses import getResponseForIntent
from intent_classifier import IntentClassifier
from pprint import pprint
from main import predict
from utils import MODEL_CLASSES, MODEL_PATH_MAP, extract_features

class ChatBot:
    def __init__(self):
        self.userMessages = []
        # self.intentClassifier = IntentClassifier(train=True)
        self.infoExtractor = SearchParams()
        # self.NER = NER()
        self.resp = None
        self.reset = None

    def simpleResponse(self, intent):
        return [getResponseForIntent(intent), False, ""]

    def initiatorResponse(self):
        return ["Maybe you can tell me where you want to go, for starters", False, ""]

    def complexResponse(self):
        self.infoExtractor.printExisting()
        missingTags = self.infoExtractor.missingTags()

        if missingTags:
            for x in missingTags:
                return ["I need information about the " + x, False, ""]
        else:
            self.reset = True
            return [self.infoExtractor.get_search_answer(), True, self.infoExtractor.getSearchQuery()]

    def main(self, query):
        # print("My name is Chatterbot and I'm a chatbot. If you want to exit, type Bye!")

        user_response = query.lower()
        print(user_response)

        # user_intent = self.intentClassifier.predict(user_response)
        # print("intent is: %s" % (user_intent))

        prediction = predict([query])
        user_intent = prediction[0][1]
        search_features = extract_features(prediction[0][0], prediction[0][1], prediction[0][2])
        # print(pprint([(X.text, X.label_) for X in search_features]))

        if search_features:
            self.infoExtractor.extractSearchParams(search_features)
            self.resp = self.complexResponse()
        elif user_intent:
            self.resp = self.simpleResponse(user_intent)
        else:
            self.resp = self.initiatorResponse()

        print("---------------" + self.resp[0])
        if self.reset:
            self.reset = None
            self.infoExtractor.resetParams()
        return self.resp
