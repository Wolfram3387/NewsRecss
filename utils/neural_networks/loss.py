import os.path

from keras.utils import custom_object_scope
import tensorflow as tf
from keras import backend as K
def euclidean_distance(vectors):
    import keras.models
    from keras.preprocessing.sequence import pad_sequences
    from keras import backend as K
    # unpack the vectors into separate lists
    (featsA, featsB) = vectors
    # compute the sum of squared distances between the vectors
    sumSquared = K.sum(K.square(featsA - featsB), axis=1, keepdims=True)
    # return the euclidean distance between the vectors
    return K.sqrt(K.maximum(sumSquared, K.epsilon()))

def contrastive_loss(y, preds, margin=1):
    import keras.models
    from keras.preprocessing.sequence import pad_sequences
    from keras import backend as K
    # explicitly cast the true class label data type to the predicted
    # class label data type (otherwise we run the risk of having two
    # separate data types, causing TensorFlow to error out)
    y = tf.cast(y, preds.dtype)
    # calculate the contrastive loss between the true labels and
    # the predicted labels
    squaredPreds = K.square(preds)
    squaredMargin = K.square(K.maximum(margin - preds, 0))
    loss = K.mean(y * squaredPreds + (1 - y) * squaredMargin)
    # return the computed contrastive loss to the calling function
    return loss

with custom_object_scope({'contrastive_loss': contrastive_loss, 'euclidean_distance': euclidean_distance,'K': K}):
    model = tf.keras.models.load_model(os.path.join("utils","neural_networks","siamesemodel.h5"))
