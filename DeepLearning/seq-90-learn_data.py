import sys
import tensorflow as tf
import pandas as pd
from sklearn.model_selection import train_test_split

from data_util import scaler

ARGS = None


def main():
    # prepare data
    xy = pd.read_csv(ARGS.input)
    xy = scaler(xy.values[:, 1:])
    
    # split train and test
    train_xy, test_xy = train_test_split(xy, test_size=0.2, 
                                         random_state=8080)

    # Only speedindex
    train_xy = pd.DataFrame(train_xy)
    test_xy = pd.DataFrame(test_xy)
    x_data = train_xy.values[:, :-5]
    y_data = train_xy.values[:, -5:]
    x_test = test_xy.values[:, :-5]
    y_test = test_xy.values[:, -5:]
    #x_data = train_xy[:, :-5]
    #y_data = train_xy[:, [-5]]
    #x_test = test_xy[:, :-5]
    #y_test = test_xy[:, [-5]]
    
    # placeholder for a tensor
    X = tf.placeholder(tf.float32, shape=[None, 4])
    Y = tf.placeholder(tf.float32, shape=[None, 5])

    # 
    W = tf.Variable(tf.random_normal([4, 5]), name='weight')
    b = tf.Variable(tf.random_normal([5]), name='bias')

    # Hypothesis
    hypothesis = tf.matmul(X, W) + b

    # cost function
    cost = tf.reduce_mean(tf.square(hypothesis - Y))

    # minimize
    optimizer = tf.train.GradientDescentOptimizer(learning_rate=1e-5)
    train = optimizer.minimize(cost)

    # Launch the graph in a session
    sess = tf.Session()
    # Initialize global variable
    sess.run(tf.global_variables_initializer())

    for step in range(0, 20001):
        cost_val, hy_val, _ = sess.run([cost, hypothesis, train],
                                       feed_dict={X: x_data, Y: y_data})
        if step%1000 == 0:
            print(step, 'Cost: ', cost_val)


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input',
                        type=str,
                        required=True,
                        help='learning data')
    ARGS = parser.parse_args()

    main()

