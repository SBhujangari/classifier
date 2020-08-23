import tensorflow as tf
import numpy as np
from skimage.transform import resize
from transformers import AutoTokenizer, TFAutoModelWithLMHead, TFBertModel, TFDistilBertModel, DistilBertConfig
import transformers
import tokenizers

# Let's call the image img. It can be given in a list with dimensions (256, 256, 3) or as an image for me to read from a filepath.
# Ok so inside static/uploads there'll be images
# I'll pass in the image name, but the path will just be static/uploads/{image name that I pass in}
def predict_image(img):
    img = np.asarray(img)
    img = img / 255.0
    img = resize(img, (256, 256))

    model = tf.keras.models.load_model('/home/stanleyzheng/Desktop/ignitionhacks/saved_models/savedmodelCV/assets')
    prediction = model(img)
    
    return prediction

class roBERTaClassifier(tf.keras.Model):    
    def __init__(self, bert: TFBertModel, num_classes: int):
        super().__init__()
        self.bert = bert
        self.classifier = tf.keras.layers.Dense(num_classes, activation='sigmoid')
        
    @tf.function
    def call(self, input_ids, attention_mask=None, token_type_ids=None, position_ids=None, head_mask=None):
        outputs = self.bert(input_ids,
                                attention_mask=attention_mask,
                                token_type_ids=token_type_ids,
                                position_ids=position_ids,
                                head_mask=head_mask)
        cls_output = outputs[1]
        cls_output = self.classifier(cls_output)
                
        return cls_output
    
    def act(self, state):
        options = self.model.predict(state)
        return np.argmax(options[0]), options


def predict_sentence(sentence):
    tokenizer = AutoTokenizer.from_pretrained("distilbert-base-uncased")
    trainenc=[]
    trainattn=[]

    enc = tokenizer.encode(sentence)
    trainenc.append(enc)

    trainenc = tf.keras.preprocessing.sequence.pad_sequences(trainenc, maxlen=128, dtype="long", value=0, truncating="post", padding="post")

    for i in trainenc:
        att=[int(x > 0) for x in i]
        trainattn.append(att)
    loader = tf.data.Dataset.from_tensor_slices((trainenc, trainattn))
    model = roBERTaClassifier(TFBertModel.from_pretrained("saved_models/somewhere"), 1)
    prediction = model.predict(loader)
    return np.average(prediction)

# Doom is 1, Animal Crossing is 0

import cv2
img = cv2.imread('test/animalcrossing.jpg')
predict_image(img)