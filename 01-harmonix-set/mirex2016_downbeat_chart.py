"""
Created 09-01-19 by Matt C. McCallum
"""


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Python standard library imports
import argparse
import os
import copy


def main():
    """
    A simple script to evaluate the results of various algorithms on the
    Harmonix Dataset. Each of these algorithms must first be run on the
    Harmonix Dataset audio which at this stage is difficult to get hold of
    due to copyright restrictions. The code here is provided for completeness
    so that a reader may understand exactly how the published results were obtained.

    This code is provided as a single script for the convenience of quick readibility
    to a reader. Further structuring of this code into classes that may be more modular
    and reusable could be beneficial. For example, classes that maintain reading / writing
    directory hierarchies on disk for various result types. However, our primary concern 
    at this stage is to provide a precise demonstration of how the results were evaluated.

    Args:
        results_dir: str - The directory within which to organize results as easily
        readable .txt or .csv files.
    """

    #
    # Plot results
    #
    plotting_results = {
            'F-Measure': {'Böck A': [0.908, 0.865, 0.369, 0.537, 0.635, 0.970, 0.599]}
    }

    labels = ['ballroom', 'beatles', 'carnatic', 'turkish', 'cretan', 'hjdb', 'rwc']

    c1 = 'turquoise'
    for result_type, result_algs in plotting_results.items():
        plt.figure()
        y = list(result_algs.values())[0]
        x = np.zeros(len(y))
        print(x)
        print(y)
        box2 = plt.scatter(x, y)#, labels=list(result_algs.keys()))
        for i, l in enumerate(labels):
            plt.annotate(l, (x[i], y[i]))

        plt.ylabel(result_type)
        plt.xlabel(['Böck A'])
        plt.tight_layout()
        plt.ylim([0, 1.0])
        plt.show()


if __name__=='__main__':
    parser = argparse.ArgumentParser(description='Evaluates the performance of beat tracking algorithms and plots these results.')
    kwargs = vars(parser.parse_args())
    main(**kwargs)
