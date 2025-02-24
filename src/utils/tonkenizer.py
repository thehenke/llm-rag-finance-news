import string
import re

STOPWORDS = {
    "a", "ao", "aos", "as", "até", "com", "como", "da", "das", "de", "do", "dos", "e", "em", "entre",
    "é", "era", "eram", "essa", "esse", "esta", "estamos", "estão", "eu", "foi", "foram", "isso", "lhe",
    "me", "mesmo", "minha", "muito", "na", "não", "nas", "nem", "no", "nos", "nós", "o", "os", "ou",
    "para", "pela", "pelas", "pelo", "pelos", "por", "porque", "que", "se", "sem", "seu", "sua",
    "são", "também", "te", "tem", "tinha", "todos", "tudo", "um", "uma", "você",
    # Stopwords em inglês
    "i", "me", "my", "myself", "we", "our", "ours", "ourselves", "you", "your", "yours", "yourself",
    "yourselves", "he", "him", "his", "himself", "she", "her", "hers", "herself", "it", "its", "itself",
    "they", "them", "their", "theirs", "themselves", "what", "which", "who", "whom", "this", "that",
    "these", "those", "am", "is", "are", "was", "were", "be", "been", "being", "have", "has", "had",
    "having", "do", "does", "did", "doing", "a", "an", "the", "and", "but", "if", "or", "because", "as",
    "until", "while", "of", "at", "by", "for", "with", "about", "against", "between", "into", "through",
    "during", "before", "after", "above", "below", "to", "from", "up", "down", "in", "out", "on", "off",
    "over", "under", "again", "further", "then", "once", "here", "there", "when", "where", "why", "how",
    "all", "any", "both", "each", "few", "more", "most", "other", "some", "such", "only", "own", "same",
    "so", "than", "too", "very", "can", "will", "just", "should", "now", "let"
}

def word_tokenize(text):

    text = text.lower()

    text = re.sub(r"[{}]+".format(re.escape(string.punctuation.replace("'", "").replace("-", ""))), " ", text)

    tokens = re.findall(r"\b\w+(?:[-']\w+)*\b", text)

    tokens = [word for word in tokens if word not in STOPWORDS]

    return tokens
