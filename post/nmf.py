import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import NMF

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

    print(quora.head())

    # adding the new post to the dataset 
    quora = quora.append(new_post, ignore_index=True)

    tfidf = TfidfVectorizer(max_df=0.95, min_df=2, stop_words='english')
    dtm = tfidf.fit_transform(quora['Question'])

    nmf_model = NMF(n_components=9,random_state=42)
    nmf_model.fit(dtm)

    for index,topic in enumerate(nmf_model.components_):
        print(f'THE TOP 15 WORDS FOR TOPIC #{index}')
        print([tfidf.get_feature_names()[i] for i in topic.argsort()[-15:]])
        print('\n')

    topic_results = nmf_model.transform(dtm)
    quora['Topic'] = topic_results.argmax(axis=1)

    print (quora.tail(1))

    topic_number = quora['Topic'].tail(1).item()
    print ('topic number:', topic_number)

    print ('topics:')
    topic_of_words = [tfidf.get_feature_names()[i] for i in nmf_model.components_[topic_number].argsort()[-15:]]

    print(topic_of_words)

    topics = ["Generic Questions","Finance","Politics","Philosophical Discussions",
                    "Education", "Social Discussions", "Asian Culture and Events",
                    "Marriage and Relationships","Healthy Life Style"]

    print('end of nmf function')

    return Topic(topics[topic_number], '-'.join(topic_of_words))

