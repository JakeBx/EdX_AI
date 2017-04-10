import argparse
import numpy as np
from statistics import mean
from statistics import stdev

# TODO define regressor class
# class LinearRegression:
#     def __init__(self, alpha):
#         self.iterations = 100
#         self.alphas = alpha
#         self.weights = np.zeros(3)


# performs linear regression using gradient decent
def gradient_decent(X, y, alpha, iterations):
    weights = np.zeros(X.shape[1])
    features = X.shape[1]
    n = len(y)
    sse = []

    for each in range(iterations):
        y_est = np.dot(X, weights)
        error = y_est - y
        sse = np.sum(error ** 2)
        for i in range(features):
            errors_x = error * X[:,i]
            weights[i] -= alpha * (1/n) * np.sum(errors_x)

    return alpha, iterations, weights[0], weights[1], weights[2], sse   # The weights are picked out one by one


# returns the "z-scores"
def feature_norm(X):
    mean_r = []
    std_r = []
    x_norm = X
    features = X.shape[1]
    for feature in range(features):
        m = mean(X[:, feature])
        s = stdev(X[:, feature])
        mean_r.append(m)
        std_r.append(s)
        x_norm[:, feature] = (x_norm[:, feature] - m) / s

    return x_norm


# contiues to run models until the SSE beings to increase
def find_my_alpha(X, y, iterations):
    my_alpha = 0.00
    test_alpha = 0.00
    SSE = float('Inf')
    while True:
        result = gradient_decent(X, y, test_alpha, iterations)
        test_alpha+=0.01
        SSE_new = result[-1]
        if SSE_new > SSE:
            break

        SSE = SSE_new
        my_alpha = test_alpha

    return round(my_alpha,2)


def main(input_file, output_file):
    # Values
    alphas = [0.001, 0.005, 0.01, 0.05, 0.1, 0.5, 1, 5, 10]
    iterations = 100

    # file io
    fi = open(input_file, 'rb')
    fo = open(output_file, 'w')
    raw_data = np.loadtxt(fi, delimiter=',')

    # normalise data, construct matrices for the regression
    X_norm = feature_norm(raw_data[:, :-1])
    b_0 = np.ones(X_norm.shape[0])
    X = np.column_stack((b_0.T,X_norm))
    y = raw_data[:, -1]

    # gradient decent on alpha, objective function is the sum of squared errors
    # my_alpha = find_my_alpha(X, y, iterations)  # is 0.62
    my_alpha = 0.62
    alphas.append(my_alpha)

    # perform gradient decent on weights for each alpha
    for alpha in alphas:
        result = gradient_decent(X,y,alpha,iterations)
        fo.write("%s, %d, %s, %s, %s\n" % result[:-1])

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('input_file')
    parser.add_argument('output_file')
    args = parser.parse_args()

    if args and args.input_file and args.output_file:
        main(args.input_file, args.output_file)

"""
REFERENCES:
http://aimotion.blogspot.com.au/2011/10/machine-learning-with-python-linear.html
http: // stackoverflow.com / questions / 17784587 / gradient - descent - using - python - and -numpy
"""