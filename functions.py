""" Core functions for the project """
# pylint: disable-msg=C0103
import pickle
import numpy as np
import tensorflow as tf
tf.enable_eager_execution()

def save_image(image):
    """ Save the image received to a temp folder on the server """
    image.save("./image/temp.jpg")

def preprocess(image_path):
    """ Preprocess the image before feeding it to Inception V3 model """
    # Convert all the images to size 299x299 as expected by the inception v3 model
    img = tf.keras.preprocessing.image.load_img(image_path, target_size=(299, 299))
    # Convert image to numpy array of 3-dimensions
    x = tf.keras.preprocessing.image.img_to_array(img)
    # Add one more dimension
    x = np.expand_dims(x, axis=0)
    # preprocess the images using preprocess_input() from inception module
    x = tf.keras.applications.inception_v3.preprocess_input(x)

    return x

def load_inception():
    """ Load inceptionv3 model without the last layer """
    # Load the inception v3 model
    model_inceptionv3 = tf.keras.applications.inception_v3.InceptionV3(weights="imagenet")
    # Remove the last layer (output softmax layer) from the inception V3
    model_inceptionv3_new = tf.keras.models.Model(model_inceptionv3.input, model_inceptionv3.layers[-2].output)

    return model_inceptionv3_new

def encode(image):
    """ Function to encode a given image into a vector of size (2048, ) """
    image = preprocess(image)
    model_inceptionv3_new = load_inception()
    fea_vec = model_inceptionv3_new.predict(image)  # Get the encoding vector for the image
    fea_vec = np.reshape(fea_vec, fea_vec.shape[1]) # reshape from (1, 2048) to (2048, )

    return fea_vec

def process_image(image_path):
    """ Process image before feeding it to the model """
    image = encode(image_path)
    image = image.reshape((1, 2048))

    return image

def greedy_search(image_path):
    """ Core function which does all the job """
    # contants
    in_text = "startseq"
    max_length = 34
    wordtoix = pickle.load(open("./pickle/wordtoix.pkl", "rb"))
    ixtoword = pickle.load(open("./pickle/ixtoword.pkl", "rb"))

    model_final = tf.keras.models.load_model("./model/model_final.h5")
    photo = process_image(image_path)
    for _ in range(max_length):
        sequence = [wordtoix[w] for w in in_text.split() if w in wordtoix]
        sequence = tf.keras.preprocessing.sequence.pad_sequences([sequence], maxlen=max_length)

        yhat = model_final.predict([photo, sequence])
        yhat = np.argmax(yhat)
        word = ixtoword[yhat]

        in_text += " " + word

        if word == "endseq":
            break

    final = in_text.split()
    final = final[1: -1]
    final = " ".join(final)

    tf.keras.backend.clear_session()

    return {"Caption": final}
