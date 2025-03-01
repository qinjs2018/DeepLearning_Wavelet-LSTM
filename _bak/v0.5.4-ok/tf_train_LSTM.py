
from __future__ import print_function

import tensorflow as tf
from tensorflow.contrib import rnn
import numpy as np
import matplotlib.pyplot as plt

import pickle as pickle     # python pkl 文件读写

def RNN(x, weights, biases, timesteps , num_hidden):
    # Prepare data shape to match `rnn` function requirements
    # Current data input shape: (batch_size, timesteps, n_input)
    # Required shape: 'timesteps' tensors list of shape (batch_size, n_input)

    # Unstack to get a list of 'timesteps' tensors of shape (batch_size, n_input)
    x = tf.unstack(x, timesteps, 1)

    # Define a lstm cell with tensorflow
    lstm_cell = rnn.BasicLSTMCell(num_hidden, forget_bias=1.0)

    # Get lstm cell output
    outputs, states = rnn.static_rnn(lstm_cell, x, dtype=tf.float32)

    # Linear activation, using rnn inner loop last output
    return tf.matmul(outputs[-1], weights['out']) + biases['out']


def main():


    # Training Parameters
    
    # learning_rate = 0.001
    learning_rate = 0.01
    training_steps = 500
    display_step = 50

    # Network Parameters
    num_input = 1
    timesteps = 83 # timesteps
    num_hidden = 200 # hidden layer num of features
    num_classes = 4 # MNIST total classes (1-4 digits)

    ''' ********************************************************************************** '''
    

    # tf Graph input
    X = tf.placeholder("float", [None, timesteps, num_input])
    Y = tf.placeholder("float", [None, num_classes])

    # Define weights
    weights = {
        'out': tf.Variable(tf.random_normal([num_hidden, num_classes]))
    }
    biases = {  
        'out': tf.Variable(tf.random_normal([num_classes]))
    }

    logits = RNN(X, weights, biases, timesteps , num_hidden)
    prediction = tf.nn.softmax(logits) # prediction-预测

    # Define loss and optimizer
    # 定义 损失函数 和 优化器
    loss_op = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(
        logits=logits, labels=Y))
    optimizer = tf.train.GradientDescentOptimizer(learning_rate=learning_rate)
    train_op = optimizer.minimize(loss_op)

    # Evaluate model (with test logits, for dropout to be disabled)
    # 评估模型（使用测试日志，禁用dropout）
    correct_pred = tf.equal(tf.argmax(prediction, 1), tf.argmax(Y, 1))
    accuracy = tf.reduce_mean(tf.cast(correct_pred, tf.float32))

    
    # Initialize the variables (i.e. assign their default value)
    # 初始化变量（即分配它们的默认值）
    init = tf.global_variables_initializer()
    

    # 声明tf.train.Saver类用于保存/加载模型
    saver = tf.train.Saver() 


    ''' ********************************************************************************** '''
    

    train_data = np.array(pickle.load(open('tf_model_lstm/train_seg_data.plk', 'rb')) )
    train_labels = np.array(pickle.load(open('tf_model_lstm/train_seg_labels.plk', 'rb')) )

    batch_size = len(train_data)

    print( type(train_data) )
    print( train_data.shape )
    # ndarray
    
    
    # Start training
    # 开始训练
    with tf.Session() as sess:

        # Run the initializer
        # 运行初始化程序
        sess.run(init)

        for step in range(1, training_steps+1):
            # batch_x, batch_y = mnist.train.next_batch(batch_size)
            batch_x = train_data
            batch_y = train_labels
            # Reshape data to get 28 seq of 28 elements
            batch_x = batch_x.reshape((batch_size, timesteps, num_input))
            # Run optimization op (backprop)  
            # 运行优化操作（backprop）
            sess.run(train_op, feed_dict={X: batch_x, Y: batch_y})
            if step % display_step == 0 or step == 1:
                # Calculate batch loss and accuracy 
                # 计算批次损失和准确性
                loss, acc = sess.run([loss_op, accuracy], feed_dict={X: batch_x,
                                                                    Y: batch_y})
                print("Step " + str(step) + ", Minibatch Loss= " + \
                    "{:.4f}".format(loss) + ", Training Accuracy= " + \
                    "{:.3f}".format(acc))

        print("Optimization Finished(优化完成)!")

        saver_path = saver.save(sess, "tf_model_lstm/model.ckpt")  # 将模型保存到save/model.ckpt文件
        print("Model saved in file:", saver_path)


        # Calculate accuracy for 128 mnist test images
        # 计算128个mnist测试图像的准确性
        # test_data = mnist.test.images[:test_len].reshape((-1, timesteps, num_input))
        # test_label = mnist.test.labels[:test_len]


        print("Testing Accuracy(测试精度):", \
            sess.run(accuracy, feed_dict={X: batch_x, Y: batch_y}))

        # 分类
        # test_data = mnist.test.images[:test_len].reshape((-1, timesteps, num_input))
        # test_label = mnist.test.labels[:test_len]
        '''
        test_data = batch_x[0]
        test_label = batch_y[0]
        print(test_data.shape, test_label)
        print("分类:", \
            sess.run(prediction, feed_dict={X: test_data}))

        '''


        out = []
        for i in range(batch_size):
            test_data = train_data[i]
            test_label = train_labels[i]
                # Reshape data to get 28 seq of 28 elements
            test_data = test_data.reshape((1, timesteps, num_input))

            # print(test_data.shape, test_label)

            # print("分类:", sess.run(prediction, feed_dict={X: test_data}))
            out_tag = sess.run(prediction, feed_dict={X: test_data})
            # 获取矩阵值(概率)最大下标
            j = np.unravel_index( out_tag[0].argmax(), out_tag[0].shape ) + 1
            # print(j)
            out.append(j)
        
        plt.plot( out )
        plt.show() 



if __name__=='__main__':
    main()


