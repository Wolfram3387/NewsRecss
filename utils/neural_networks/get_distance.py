from keras.src.preprocessing.text import Tokenizer

from keras.preprocessing.sequence import pad_sequences
import warnings
from utils.neural_networks.loss import model

warnings.filterwarnings('ignore')

t = Tokenizer()


def get_distance(user_keywords, article_keywords):
    prediction_data = article_keywords
    prediction_vector = t.texts_to_sequences([prediction_data])
    prediction_vector = pad_sequences(prediction_vector, maxlen=200)

    assistant_data = user_keywords
    assistant_vector = t.texts_to_sequences([assistant_data])
    assistant_vector = pad_sequences(assistant_vector, maxlen=200)

    result = model.predict([prediction_vector, assistant_vector])[0][0]
    return result
