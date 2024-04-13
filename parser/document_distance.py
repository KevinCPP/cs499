# By Athan Johnson

#from parser.parser import get_patients
import re
import math

class Sentiment_Analysis:
    def parse_document(self, document):
        """
        Parse the document word by word.
        """
        # Use regular expression to split the document into words
        words = re.findall(r'\b\w+\b', document)
        return words

    def distance(self, doc1, doc2):
        wordset = set()
        dict1 = {}
        magnitude_d1 = 0
        dict2 = {}
        magnitude_d2 = 0

        # get vector representation of document 1
        for word in doc1:
            if word in dict1:
                dict1[word] += 1
            else:
                dict1[word] = 1
          
            if word not in dict2:
                dict2[word] = 0

            wordset.add(word)

        # calculate magnitude of document 1
        for word in doc1:
            magnitude_d1 += math.sqrt(dict1[word] ** 2)

        magnitude_d1 = math.sqrt(magnitude_d1)

        # make vector for document 2
        for word in doc2:
            if word in dict2:
                dict2[word] += 1
            else:
                dict2[word] = 1
          
            if word not in dict1:
                dict1[word] = 0

            wordset.add(word)

        # calculate magnitude of document 2
        for word in doc2:
            magnitude_d2 += math.sqrt(dict2[word] ** 2)

        magnitude_d2 = math.sqrt(magnitude_d2)
        
        dotprod = 0
        for word in wordset:
            dotprod += dict1[word] * dict2[word]

        document_distance = dotprod / (magnitude_d1 * magnitude_d2)
        
        return document_distance
    

    def sentiment_analysis(self, doctors_note, positive, negative, angular=False):
        # first, get the comments about the patient from the doctor
        #doctors_note = get_patients(doctors_note)
        
        # parse the documents into individual words
        doctors_note_words = self.parse_document(doctors_note)
        positive_words = self.parse_document(positive)
        negative_words = self.parse_document(negative)
        
        # determine the distance between the documents
        pos_sentiment = self.distance(doctors_note_words, positive_words)
        neg_sentiment = self.distance(doctors_note_words, negative_words)
        
        # can utilize the angle between the two vectors rather than the raw
        # distance value, which could be more familiar
        if angular:
            pos_sentiment = math.acos(pos_sentiment)
            neg_sentiment = math.acos(neg_sentiment)
        
        # determine if it is closer to positive or negative, with a tolerance
        # for a neutral sentiment
        return (pos_sentiment, neg_sentiment) 

if __name__ == "__main__":
    sa = Sentiment_Analysis()

    positive = "cash money weed pussy marijuana lamborghini"
    negative = "office job broke depressed stupid gay"
    
    test1 = "I made tons of cash the other day and drove my lamborghini to the weed dispensary to get some marijuana"
    test2 = "I had to go to my office job, which makes me depressed, and my stupid boss is broke because he bought a lamborghini"

    print(sa.sentiment_analysis(test1, positive, negative, 0, False))
    print(sa.sentiment_analysis(test2, positive, negative, 0, False))


