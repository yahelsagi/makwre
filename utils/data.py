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

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

__version__ = '0.1.0'
__author__ = 'Abien Fred Agarap'

import numpy as np
import os
from sklearn.preprocessing import StandardScaler


def save_labels(predictions, actual, result_path, phase, model, step):
    """Saves the actual and predicted labels to a NPY file

    :param predictions: The NumPy array containing the predicted labels.
    :param actual: The NumPy array containing the actual labels.
    :param result_path: The path where to save the concatenated actual and predicted labels.
    :param phase: The phase for which the predictions is, i.e. training/validation/testing.
    :param model: The name of the model used for classification
    :param step: The time step for the NumPy arrays.
    :return:
    """

    if not os.path.exists(path=result_path):
        os.mkdir(result_path)

    # Concatenate the predicted and actual labels
    labels = np.concatenate((predictions, actual), axis=1)

    # save every labels array to NPY file
    np.save(file=os.path.join(result_path, '{}-{}-{}.npy'.format(phase, model, step)), arr=labels)


def load_data(dataset, standardize=True):
    """

    :param dataset:
    :param standardize:
    :return:
    """

    features = dataset['arr'][:, 0]
    features = np.array([feature for feature in features])
    features = np.reshape(features, (features.shape[0], features.shape[1] * features.shape[2]))

    if standardize:
        features = StandardScaler().fit_transform(features)

    labels = dataset['arr'][:, 1]
    labels = np.array([label for label in labels])

    return features, labels


def one_hot_encode(labels):
    """

    :param labels:
    :return:
    """
    one_hot = np.zeros((labels.shape[0], labels.max() + 1))
    one_hot[np.arange(labels.shape[0]), labels] = 1
    labels = one_hot
    labels[labels == 0] = -1
    return labels
