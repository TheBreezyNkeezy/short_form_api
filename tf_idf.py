import nltk, math

def find_frequencies(sentences):
    return None

def create_tf(frequencies):
    return None

def find_documents_per_word(frequencies):
    return None

def create_idf(frequencies, sents_per_words, total):
    return None

def calculate_tf_idf(tfs, idfs):
    return None

def calculate_scores(tf_idfs):
    return None

def generate_summary(sentences, scores, threshold):
    return None

# """
# Matrix summarizer using TF-IDF algorithm
# Sources:
# https://en.wikipedia.org/wiki/Tf%E2%80%93idf
# https://towardsdatascience.com/text-summarization-using-tf-idf-e64a0644ace3
# """
def tf_idf_summarizer(passage: str, brevity: int = 35, quality: int = 1.5):
    nltk.download('punkt')
    nltk.download("stopwords")
    ps = nltk.PorterStemmer()
    stopwords = nltk.corpus.stopwords.words("english")

    token_sentences = nltk.sent_tokenize(passage)
    total_sentences = len(token_sentences)

    # TF step: find total frequencies of words in each sentence
    frequency_matrix = find_frequencies(token_sentences)
    tf_matrix = create_tf(frequency_matrix)

    # IDF step: find rarity of a word relative to each "document" (sentence)
    sentences_containing_words = find_documents_per_word(frequency_matrix)
    idf_matrix = create_idf(
        frequency_matrix,
        sentences_containing_words,
        total_sentences
    )

    # TF_IDF step: multiply the TF values and the IDF values
    tf_idf_matrix = calculate_tf_idf(tf_matrix, idf_matrix)

    # Score sentences and generate summary from best sentences
    sentence_scores = calculate_scores(tf_idf_matrix)
    average_score = sum(sentence_scores.values()) / len(sentence_scores)
    return generate_summary(token_sentences, sentence_scores, quality * average_score)