import numpy as np
import tensorflow as tf
from collections import Counter
import os

class train:
    def __init__(self, data = None, target = None):
        self.data = data
        self.target = target



class neural:
    def __init__(self):
        self.newsgroups_train = train()
        self.word2index = ()
        self.vocab = Counter()
        self.total_words = 0


    def  data_init(self):
        corpus = []
        targ = []
        for i in os.listdir("app/model/repair"):
            with open("app/model/repair/" + i,'r') as fl:
                corpus.append(fl.read())
                targ.append(0)
        for i in os.listdir("app/model/service"):
            with open("app/model/service/" + i,'r',encoding='utf-8') as fl:
                corpus.append(fl.read())
                targ.append(1)
        for i in os.listdir("app/model/service1"):
            with open("app/model/service1/" + i,'r') as fl:
                corpus.append(fl.read())
                targ.append(1)
        newsgroups_train = train(corpus,targ)

        for text in newsgroups_train.data:
            for word in text.split(' '):
                self.vocab[word.lower()] += 1

                # for text in newsgroups_test.data:
                # for word in text.split(' '):
                #    vocab[word.lower()] += 1

        self.total_words = len(self.vocab)
        self.word2index = self.get_word_2_index(self.vocab)
        # Network Parameters
        n_hidden_1 = 100  # 1st layer number of features
        n_hidden_2 = 100  # 2nd layer number of features
        n_classes = 2  # Categories: graphics, sci.space and baseball
        n_input = self.total_words  # Words in vocab
        # Store layers weight & bias
        self.weights = {
            'h1': tf.Variable(tf.random_normal([n_input, n_hidden_1]), name="h1"),
            'h2': tf.Variable(tf.random_normal([n_hidden_1, n_hidden_2]), name="h2"),
            'out': tf.Variable(tf.random_normal([n_hidden_2, n_classes]), name="wout")
        }
        self.biases = {
            'b1': tf.Variable(tf.random_normal([n_hidden_1]), name="b1"),
            'b2': tf.Variable(tf.random_normal([n_hidden_2]), name="b2"),
            'out': tf.Variable(tf.random_normal([n_classes]), name="bout")
        }
        self.input_tensor = tf.placeholder(tf.float32, [None, n_input], name="input")
        self.output_tensor = tf.placeholder(tf.float32, [None, n_classes], name="output")
        # Construct model
        self.prediction = self.multilayer_perceptron(self.input_tensor, self.weights, self.biases)

    def get_word_2_index(self,vocab):
        word2index = {}
        for i, word in enumerate(vocab):
            word2index[word.lower()] = i

        return word2index

    def text_to_vector(self,text):
        layer = np.zeros(self.total_words, dtype=float)
        for word in text.split(' '):
            if word in self.vocab:
                layer[self.word2index[word.lower()]] += 1
            else:
                continue
        return layer

    def multilayer_perceptron(self,input_tensor, weights, biases):
        layer_1_multiplication = tf.matmul(input_tensor, weights['h1'])
        layer_1_addition = tf.add(layer_1_multiplication, biases['b1'])
        layer_1 = tf.nn.relu(layer_1_addition)

        # Hidden layer with RELU activation
        layer_2_multiplication = tf.matmul(layer_1, weights['h2'])
        layer_2_addition = tf.add(layer_2_multiplication, biases['b2'])
        layer_2 = tf.nn.relu(layer_2_addition)

        # Output layer
        out_layer_multiplication = tf.matmul(layer_2, weights['out'])
        out_layer_addition = out_layer_multiplication + biases['out']

        return out_layer_addition


    def check_cat(self,text):
        x_res = []
        text = self.text_to_vector(text)
        x_res.append(text)

        saver = tf.train.Saver()
        with tf.Session() as sess:
            saver.restore(sess, "/model/model.ckpt")
            classification = sess.run(tf.argmax(self.prediction, 1), feed_dict={self.input_tensor: x_res})
        return classification
