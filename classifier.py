# Copyright 2017 Abien Fred Agarap
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# =========================================================================

"""Module for classifier based on a trained DL-SVM model"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

__version__ = '0.1.0'
__author__ = 'Abien Fred Agarap'

import argparse
import numpy as np
import os
import tensorflow as tf
from utils.data import load_data
from utils.data import one_hot_encode

BATCH_SIZE = 'batch_size'
CELL_SIZE = 'cell_size'
DROPOUT = 'dropout'

accuracy_tensor_name = 'accuracy/accuracy/Mean:0'
prediction_tensor_name = 'accuracy/predicted_class:0'


def predict(dataset, model, model_path, **kwargs):
    """Returns classification for given data

    :param dataset: The dataset to be classified using the trained model.
    :param model: The model name to be used for classification.
    :param model_path: The path where the trained model is saved.
    :return:
    """

    init_op = tf.group(tf.local_variables_initializer(), tf.global_variables_initializer())

    assert BATCH_SIZE in kwargs, 'KeyNotFound : {}'.format(BATCH_SIZE)
    assert type(kwargs[BATCH_SIZE]) is int, \
        'Expected data type : int, but {} is {}'.format(kwargs[BATCH_SIZE], type(kwargs[BATCH_SIZE]))

    if model == 1:
        # CNN-SVM
        assert DROPOUT in kwargs, 'KeyNotFound : {}'.format(DROPOUT)
        assert type(kwargs[DROPOUT]) is float, \
            'Expected data type : float, but {} is {}'.format(kwargs[DROPOUT], type(kwargs[DROPOUT]))

        feed_dict = {'input/x_input:0': None, 'input/y_input:0': None, 'p_keep:0': kwargs[DROPOUT]}

        accuracy_tensor_name = 'metrics/accuracy/Mean:0'
        prediction_tensor_name = 'metrics/predicted_class:0'

    elif model == 2:
        # GRU-SVM
        assert CELL_SIZE in kwargs, 'KeyNotFound : {}'.format(CELL_SIZE)
        assert type(kwargs[CELL_SIZE]) is int, \
            'Expected data type : int, but {} is {}'.format(kwargs[CELL_SIZE], type(kwargs[CELL_SIZE]))
        assert DROPOUT in kwargs, 'KeyNotFound : {}'.format(DROPOUT)
        assert type(kwargs[DROPOUT]) is float, \
            'Expected data type : float, but {} is {}'.format(kwargs[DROPOUT], type(kwargs[DROPOUT]))

        initial_state = np.zeros([kwargs[BATCH_SIZE], kwargs[CELL_SIZE]])
        initial_state = initial_state.astype(np.float32)

        feed_dict = {'input/x_input:0': None, 'input/y_input:0': None,
                     'initial_state:0': initial_state, 'p_keep:0': kwargs[DROPOUT]}

    elif model == 3:
        # MLP-SVM
        feed_dict = {'input/x_input:0': None, 'input/y_input:0': None}

    predictions_array = np.array([])
    accuracy_array = np.array([])

    with tf.Session() as sess:
        sess.run(init_op)

        checkpoint = tf.train.get_checkpoint_state(model_path)

        if checkpoint and checkpoint.model_checkpoint_path:
            # get the meta graph from trained model
            saver = tf.train.import_meta_graph(checkpoint.model_checkpoint_path + '.meta')
            # restore previously-saved variables from the meta graph
            saver.restore(sess, tf.train.latest_checkpoint(model_path))
            print('Loaded trained model from {}'.format(tf.train.latest_checkpoint(model_path)))

        assert 'size' in kwargs, 'KeyNotFound : {}'.format('size')

        try:
            for step in range(kwargs['size'] // kwargs['batch_size']):
                offset = (step * kwargs['batch_size']) % kwargs['size']
                features = dataset[0][offset:(offset + kwargs['batch_size'])]
                labels = dataset[1][offset:(offset + kwargs['batch_size'])]

                feed_dict['input/x_input:0'] = features
                feed_dict['input/y_input:0'] = labels

                prediction_tensor = sess.graph.get_tensor_by_name(prediction_tensor_name)
                predictions = sess.run(prediction_tensor, feed_dict=feed_dict)

                predictions_array = np.append(predictions_array, predictions)

                accuracy_tensor = sess.graph.get_tensor_by_name(accuracy_tensor_name)
                accuracy = sess.run(accuracy_tensor, feed_dict=feed_dict)

                accuracy_array = np.append(accuracy_array, accuracy)
        except KeyboardInterrupt:
            print('KeyboardInterrupt at step {}'.format(step))

    return predictions_array, accuracy_array


def parse_args():
    parser = argparse.ArgumentParser(
        description='Deep Learning Using Support Vector Machine for Malware Classification')
    group = parser.add_argument_group('Arguments')
    group.add_argument('-m', '--model', required=True, type=int,
                       help='[1] CNN-SVM, [2] GRU-SVM, [3] MLP-SVM')
    group.add_argument('-t', '--model_path', required=True, type=str,
                       help='path where to save the trained model')
    group.add_argument('-d', '--dataset', required=True, type=str,
                       help='the dataset to be classified')
    arguments = parser.parse_args()
    return arguments


def main(arguments):

    model_choice = arguments.model
    model_path = arguments.model_path
    dataset_path = arguments.dataset

    assert model_choice == 1 or model_choice == 2 or model_choice == 3, \
        'Invalid choice: Choose among 1, 2, and 3 only.'
    assert os.path.exists(path=model_path), '{} does not exist!'.format(model_path)
    assert os.path.exists(path=dataset_path), '{} does not exist!'.format(dataset_path)

    dataset = np.load(dataset_path)

    features, labels = load_data(dataset=dataset)

    labels = one_hot_encode(labels=labels)


if __name__ == '__main__':
    args = parse_args()

    main(arguments=args)
