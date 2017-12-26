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

"""Main program implementing the MLP class"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

__version__ = '0.1'
__author__ = 'Abien Fred Agarap'

import argparse
from models.cnn_svm import CNN
from models.gru_svm import GruSvm
from models.mlp_svm import MLP
import numpy as np
from sklearn.model_selection import train_test_split

malware_family = ['Adialer.C',
 'Agent.FYI',
 'Allaple.A',
 'Allaple.L',
 'Alueron.gen!J',
 'Autorun.K',
 'C2LOP.P',
 'C2LOP.gen!g',
 'Dialplatform.B',
 'Dontovo.A',
 'Fakerean',
 'Instantaccess',
 'Lolyda.AA1',
 'Lolyda.AA2',
 'Lolyda.AA3',
 'Lolyda.AT',
 'Malex.gen!J',
 'Obfuscator.AD',
 'Rbot!gen',
 'Skintrim.N',
 'Swizzor.gen!E',
 'Swizzor.gen!I',
 'VB.AT',
 'Wintrim.BX',
 'Yuner.A']


def parse_args():
    parser = argparse.ArgumentParser(
        description='')
    group = parser.add_argument_group('Arguments')
    group.add_argument('-d', '--dataset', required=True, type=str,
                       help='the dataset to be used')
    group.add_argument('-n', '--num_epochs', required=True, type=int,
                       help='number of epochs')
    group.add_argument('-l', '--log_path', required=True, type=str,
                       help='path where to save the TensorBoard logs')
    group.add_argument('-r', '--result_path', required=True, type=str,
                       help='path where to save actual and predicted labels array')
    arguments = parser.parse_args()
    return arguments


def main(arguments):
    
    dataset = np.load(arguments.dataset)

    features = dataset['arr'][:, 0]
    
    labels = dataset['arr'][:, 1]

    # get the number of features
    num_features = features.shape[1]

    train_features, test_features, train_labels, test_labels = train_test_split(features, labels, test_size=0.30,
                                                                                stratify=labels)


if __name__ == '__main__':
    args = parse_args()

    main(args)
