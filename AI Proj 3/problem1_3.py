import argparse
import numpy as np
from matplotlib import pyplot as plt


class Perceptron:
    def __init__(self, labels: np.array):
        self.weights = np.zeros(3)
        self.labels = labels

    def predict(self, row: np.array):
        predict = np.dot(row, self.weights)
        if predict > 0:
            return 1
        else:
            return -1

    def results(self, data: np.array):
        correct, incorrect = 0, 0
        for (row, actual) in zip(data, self.labels):
            predict = self.predict(row)
            if actual != predict:
                incorrect += 1
            else:
                correct += 1
        return correct, incorrect

    def train(self, data):
        for (row, label) in zip(data, self.labels):
            actual = label
            predict = self.predict(row)
            if actual < predict:
                self.weights -= row
            elif actual > predict:
                self.weights += row

        correct, incorrect = self.results(data)
        return self.weights, correct, incorrect


def graph(data: np.array, perceptron: Perceptron):
    colormap = np.array(['r', 'k'])
    ixs = [0 if x == 1 else 1 for x in perceptron.labels]
    xs = data[:, [0]]
    ys = data[:, [1]]
    plt.scatter(xs.flatten(), ys.flatten(), c=colormap[ixs])
    w = perceptron.weights
    xx = np.linspace(min(xs), max(xs))
    a = -w[0] / w[1]
    yy = a * xx - (w[2]) / w[1]
    plt.plot(xx, yy, 'k-')
    plt.savefig('figure1')


def main(input_file, output_file):
    fi = open(input_file, 'rb')
    raw_data = np.loadtxt(fi, delimiter=',')
    rows = raw_data.shape[0]
    labels = raw_data[:, [-1]].flatten()
    data = raw_data[:, [0,1]]
    const = np.ones(rows)
    const.shape = (rows,1)
    data = np.hstack((data,const))

    perceptron = Perceptron(labels)

    incorrect = 1

    fo = open(output_file, 'w')

    while incorrect:
        weights, correct, incorrect = perceptron.train(data)
        fo.write("%d, %d, %d\n"%(weights[0], weights[1], weights[2]))

    graph(data, perceptron)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('input_file')
    parser.add_argument('output_file')
    args = parser.parse_args()

    if args and args.input_file and args.output_file:
        main(args.input_file, args.output_file)







