from parser.parser import get_patients
import re
import math

def document_distance(doctors_note, positive, negative):

    def parse_document(document):
        """
        Parse the document word by word.
        """
        # Use regular expression to split the document into words
        words = re.findall(r'\b\w+\b', document)
        return words

    def dot_product(doc1, doc2):
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
    
    
    doctors_note = get_patients(doctors_note)
        
    doctors_note_words = parse_document(doctors_note)
    positive_words = parse_document(positive)
    negative_words = parse_document(negative)
    
    pos_sentiment = dot_product(doctors_note_words, positive_words)
    neg_sentiment = dot_product(doctors_note_words, negative_words)
    if pos_sentiment > neg_sentiment:
        return "positive"
    else:
        return "negative"
        

