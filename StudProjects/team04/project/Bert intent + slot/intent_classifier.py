import numpy as np
import pandas as pd
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem.lancaster import LancasterStemmer
import nltk
import re
from sklearn.preprocessing import OneHotEncoder
from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences
from keras.utils import to_categorical
from keras.models import Sequential, load_model
from keras.layers import Dense, LSTM, Bidirectional, Embedding, Dropout
from keras.callbacks import ModelCheckpoint
from sklearn.model_selection import train_test_split
from nltk.stem import WordNetLemmatizer

NUM_CLASSES = 5
TRAIN_DIR = "intents.csv"

class IntentClassifier:
    def __init__(self, train=True):
        self.lemmatizer = WordNetLemmatizer()
        self.intent, self.unique_intent, self.sentences = self.load_dataset(TRAIN_DIR)
        nltk.download("stopwords")
        nltk.download("punkt")
        stemmer = LancasterStemmer()
        self.cleaned_words = self.cleaning(self.sentences)
        self.word_tokenizer = self.create_tokenizer(self.cleaned_words)
        self.vocab_size = len(self.word_tokenizer.word_index) + 1
        self.max_length = self.max_length(self.cleaned_words)
        print("Vocab Size = %d and Maximum length = %d" % (self.vocab_size, self.max_length))
        encoded_doc = self.encoding_doc(self.word_tokenizer, self.cleaned_words)
        self.padded_doc = self.padding_doc(encoded_doc, self.max_length)
        print("Shape of padded docs = ", self.padded_doc.shape)

        # tokenizer with filter changed
        self.output_tokenizer = self.create_tokenizer(self.unique_intent, filters='!"#$%&()*+,-/:;<=>?@[\]^`{|}~')

        if train:
            self.train()
        else:
            self.model = load_model("model.h5")

    def train(self):

        encoded_output = self.encoding_doc(self.output_tokenizer, self.intent)
        encoded_output = np.array(encoded_output).reshape(len(encoded_output), 1)
        output_one_hot = self.one_hot(encoded_output)

        train_X, val_X, train_Y, val_Y = train_test_split(self.padded_doc, output_one_hot, shuffle=True, test_size=0.2)

        print("Shape of train_X = %s and train_Y = %s" % (train_X.shape, train_Y.shape))
        print("Shape of val_X = %s and val_Y = %s" % (val_X.shape, val_Y.shape))

        self.model = self.create_model(self.vocab_size, self.max_length)

        self.model.compile(loss="categorical_crossentropy", optimizer="adam", metrics=["accuracy"])
        self.model.summary()

        filename = 'model.h5'
        checkpoint = ModelCheckpoint(filename, monitor='val_loss', verbose=1, save_best_only=True, mode='min')

        hist = self.model.fit(train_X, train_Y, epochs=100, batch_size=32, validation_data=(val_X, val_Y), callbacks=[checkpoint])

    def load_dataset(self, filename):
        df = pd.read_csv(filename, encoding="latin1", names=["Sentence", "Intent"])
        print(df.head())
        intent = df["Intent"]
        unique_intent = list(set(intent))
        sentences = list(df["Sentence"])
        print(intent, unique_intent, sentences)
        return intent, unique_intent, sentences

    def cleaning(self, sentences):
        words = []
        for s in sentences:
            clean = re.sub(r'[^ a-z A-Z 0-9]', " ", s)
            w = word_tokenize(clean)
            # stemming
            words.append([i.lower() for i in w])
        return words

    def create_tokenizer(self, words, filters = '!"#$%&()*+,-./:;<=>?@[\]^_`{|}~'):
        token = Tokenizer(filters=filters)
        token.fit_on_texts(words)
        return token

    def max_length(self, words):
        return len(max(words, key = len))

    def encoding_doc(self, token, words):
        return token.texts_to_sequences(words)

    def padding_doc(self, encoded_doc, max_length):
        print(encoded_doc, max_length)
        return pad_sequences(encoded_doc, maxlen=max_length, padding="post")

    def one_hot(self, encode):
        o = OneHotEncoder(sparse=False)
        return o.fit_transform(encode)

    def create_model(self, vocab_size, max_length):
        model = Sequential()
        model.add(Embedding(vocab_size, 128, input_length=max_length, trainable=False))
        model.add(Bidirectional(LSTM(128)))
        # model.add(LSTM(128))
        model.add(Dense(32, activation="relu"))
        model.add(Dropout(0.5))
        model.add(Dense(NUM_CLASSES, activation="softmax"))

        return model

    def predictions(self, text):
        clean = re.sub(r'[^ a-z A-Z 0-9]', " ", text)
        test_word = word_tokenize(clean)
        test_word = [w.lower() for w in test_word]
        test_ls = self.word_tokenizer.texts_to_sequences(test_word)
        print(test_word)
        # Check for unknown words
        if [] in test_ls:
            test_ls = list(filter(None, test_ls))

        test_ls = np.array(test_ls).reshape(1, len(test_ls))

        x = self.padding_doc(test_ls, self.max_length)

        print(x)
        pred = self.model.predict_proba(x)
        print(pred)
        return pred

    def predictions2(self, text):
        clean = re.sub(r'[^ a-z A-Z 0-9]', " ", text)
        test_word = word_tokenize(clean)
        test_word = [self.lemmatizer.lemmatize(w.lower()) for w in test_word]
        test_ls = self.word_tokenizer.texts_to_sequences(test_word)

        # Check for unknown words
        if [] in test_ls:
            test_ls = list(filter(None, test_ls))

        test_ls = np.array(test_ls).reshape(1, len(test_ls))

        x = self.padding_doc(test_ls, self.max_length)

        pred = self.model.predict_classes(x)
        print(pred)
        return pred

    def get_final_output(self, pred, classes):
        predictions = pred[0]
        print(predictions)

        classes = np.array(classes)
        ids = np.argsort(-predictions)
        classes = classes[ids]
        predictions = -np.sort(-predictions)

        for i in range(pred.shape[1]):
            print("%s has confidence = %s" % (classes[i], (predictions[i])))
            print(classes[i])
            if predictions[i] < 0.5:
                return None
            return classes[i]

    # map an integer to a word
    def word_for_id(self, integer, tokenizer):
        for word, index in tokenizer.word_index.items():
            if index == integer:
                return word
        return None

    def predict(self, text):
        pred = self.predictions(text)
        # pred2 = self.predictions2(text)
        return self.get_final_output(pred, self.unique_intent)
        # return self.word_for_id(pred2, self.output_tokenizer)



