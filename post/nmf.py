import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import NMF

# helper class to store and return 2 values 
class Topic: 
    def __init__(self, name, relatedWords): 
        self.topicName = name
        self.topicWords = relatedWords  

# AUTOMATIC CLASSIFICATION ALGORITHM
def classify_post_topics(postContent):

    # creating a DataFrame with the new post content to then add it to our dataset 
    new_post = pd.DataFrame([postContent], columns=['Question'])
    
    # our unlabelled dataset 
    quora = pd.read_csv('cleaned_data.csv')

    # adding the new post to the dataset 
    quora = quora.append(new_post, ignore_index=True)

    # max_df is the maximum document frequencey. 
    # we're asking for words that show up in no more than 95% of the documents.
    # min_df could also be a percentage, but here we're choosing to work with full numbers
    # min_df = 2 means only look at words that appear in at least 2 documents 
    tfidf = TfidfVectorizer(max_df=0.95, min_df=2, stop_words='english')

    # document term matrix with 2 dimensions: the number of words X the number of documents 
    dtm = tfidf.fit_transform(quora['Question'])

    # n_components number of topics that we want 
    nmf_model = NMF(n_components=9,random_state=42)
    nmf_model.fit(dtm)

    # topic_results stores arrays of the probabilities for each document of belonging to each of the 9 topics.
    # so topic_results is a list of lists in which each inner list has 9 numbers, each number represents the 
    # probability of the document belonging to the topic with the same index 
    topic_results = nmf_model.transform(dtm)

    # argmax gives the index position of the most represented topic. (axis=1 means run it on the 1st column)
    quora['Topic'] = topic_results.argmax(axis=1)

    # the topic number that the last item in the DataFrame belongs to (the last item is the question we added)
    topic_number = quora['Topic'].tail(1).item()

    # a list of 9 lists. the inner lists represents 1 topic and contains the top 15 most words in that topic
    topic_of_words = [tfidf.get_feature_names()[i] for i in nmf_model.components_[topic_number].argsort()[-15:]]

    # labeling the 9 topics after running the code and checking ourselves what the words of each topic discuss
    topics = ["Generic Questions","Finance","Politics","Philosophical Discussions",
                    "Education", "Social Discussions", "Asian Culture and Events",
                    "Marriage and Relationships","Healthy Life Style"]

    # returning a Topic object (an object of a class we've defined). 
    # the object contains the name of the topic and a string of the top 15 words that represent the topic 
    return Topic(topics[topic_number], '-'.join(topic_of_words))

