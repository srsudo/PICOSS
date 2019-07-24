import tensorflow as tf
import edward as ed
from edward.models import Categorical, Normal, Bernoulli
from keras.utils import to_categorical
import numpy as np
############################################
### THIS INTERNAL DEFINITION FOR THE NN ####
############################################

#############################
### REPRODUCIBILITY   ######
#############################
ed.set_seed(314159)
balanced = False

#############################
## PARAMETER SIMULATION #####
#############################

N = 10  # number of isolated signals in a minibatch.
D = 15  # number of features.

hidden1 = 1250

inferences = 200
nsamples_total = 200  # 200

nhidden_prob = 1250  ####### AQUI
# 42, 142, 442, 12345
my_random = 42

initialization = 'glorot_uniform'
K = 7 #number of classes, in our paper, 7

def neural_network(x):
    h = tf.tanh(tf.matmul(x, w0) + b0)
    h = tf.matmul(h, w1) + b1
    return h


def nn_inference(X_test, w0sampled, w1sampled, b0sampled, b1sampled):
    first = tf.tanh(tf.matmul(X_test, w0sampled) + b0sampled)
    second = tf.matmul(first, w1sampled) + b1sampled
    return second


def run_model(D, hidden1, K, X_train, y_train):
    w0 = Normal(loc=tf.zeros([D, hidden1]), scale=tf.ones([D, hidden1]))
    w1 = Normal(loc=tf.zeros([hidden1, K]), scale=tf.ones([hidden1, K]))

    b0 = Normal(loc=tf.zeros(hidden1), scale=tf.ones(hidden1))
    b1 = Normal(loc=tf.zeros(K), scale=tf.ones(K))

    x = tf.placeholder(tf.float32, [None, D])
    y = Categorical(logits=neural_network(x))

    qw0 = Normal(loc=tf.Variable(tf.random_normal([D, hidden1])),
                 scale=tf.nn.softplus(tf.Variable(tf.random_normal([D, hidden1]))))

    qw1 = Normal(loc=tf.Variable(tf.random_normal([hidden1, K])),
                 scale=tf.nn.softplus(tf.Variable(tf.random_normal([hidden1, K]))))

    qb0 = Normal(loc=tf.Variable(tf.random_normal([hidden1])),
                 scale=tf.nn.softplus(tf.Variable(tf.random_normal([hidden1]))))

    qb1 = Normal(loc=tf.Variable(tf.random_normal([K])),
                 scale=tf.nn.softplus(tf.Variable(tf.random_normal([K]))))

    # the posterior
    y_ph = tf.placeholder(tf.int32, [N])
    inference = ed.KLqp({w0: qw0, b0: qb0, w1: qw1, b1: qb1}, data={y: y_ph})
    # Intialize the infernce variables
    inference.initialize(n_iter=inferences, n_print=100, scale={y: float(nsamples_training) / N})
    # We will use an interactive session.
    sess = tf.InteractiveSession()
    tf.global_variables_initializer().run()
    data = generator([X_train, y_train], N)

    ##### INFERENCE
    for _ in range(inference.n_iter):
        X_batch, Y_batch = next(data)
        Y_batch = np.argmax(Y_batch, axis=1)
        # TensorFlow method gives the label data in a one hot vector format. We convert that into a single label.
        info_dict = inference.update(feed_dict={x: X_batch, y_ph: Y_batch})
        inference.print_progress(info_dict)

    # once again, we shall convert to get the single label (not one_hot), otherwise
    # we will have mismatch dimensions.
    # we measure the progress now
    n_samples = nsamples_total
    y_post = ed.copy(y, {w0: qw0, b0: qb0, w1: qw1, b1: qb1})
    prob_lst = []

    w0_samples = []
    b0_samples = []

    w1_samples = []
    b1_samples = []

    for _ in range(n_samples):
        w0_samp = qw0.sample()
        b0_samp = qb0.sample()

        w1_samp = qw1.sample()
        b1_samp = qb1.sample()

        w0_samples.append(w0_samp)
        b0_samples.append(b0_samp)

        w1_samples.append(w1_samp)
        b1_samples.append(b1_samp)

        prob = tf.nn.softmax(nn_inference(tf.cast(X_test, tf.float32), w0_samp, w1_samp, b0_samp, b1_samp))

        prob_lst.append(prob.eval())
    # sample = tf.concat([tf.reshape(w_samp, [-1]), b_samp], 0)
    # samples.append(sample.eval())

    print "... Testing"
    Y_pred = np.argmax(np.mean(prob_lst, axis=0), axis=1)
    print("accuracy in predicting the test data = ", (Y_pred == y_test).mean() * 100)
    print "... Confusion matrix"
    print confusion_matrix(y_true=y_test, y_pred=Y_pred)
    confusion = confusion_matrix(y_true=y_test, y_pred=Y_pred)
    toSave = "%s%s.npy" % ("BNN", my_random)
    np.save(toSave, confusion)

    precision = precision_score(y_true=y_test, y_pred=Y_pred, average='weighted')
    recall = recall_score(y_true=y_test, y_pred=Y_pred, average='weighted')
    f1_score = 2 * (precision * recall) / float(precision + recall)

    print "Precision BNN weighted %s" % (precision)
    print "Recall BNN weighted %s" % (recall)
    print "F1 score BNN %s" % (f1_score)