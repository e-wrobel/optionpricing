from option_pricing.optionlib.neural_network import NeuralNetwork
from numpy import array

if __name__ == "__main__":

    #Intialise a single neuron neural network.
    neural_network = NeuralNetwork()

    print("Random starting synaptic weights: ")
    print(neural_network.synaptic_weights)

    # The training set. We have 4 examples, each consisting of 3 input values
    # and 1 output value.

    inputs = [[0.002, 9], [0.438, 7], [0.235, 81], [0.057, 86], [0.059, 87], [0.037, 88], [0.023, 88], [0.033, 69], [0.072, 8], [0.025, 71], [0.032, 25], [0.026, 67]]
    training_set_inputs = array(inputs)

    outputs = [[0.00040820, -0.00036946, -0.00001225, -0.00000796, -0.00000960, -0.00001047, -0.00001223, -0.00002113, -0.00033881, -0.00002570, -0.00008742, -0.00003704]]
    training_set_outputs = array(outputs).T

    # Train the neural network using a training set.
    # Do it 10,000 times and make small adjustments each time.
    neural_network.train(training_set_inputs, training_set_outputs, 1000)

    print("New synaptic weights after training: ")
    print(neural_network.synaptic_weights)

    # Test the neural network with a new situation.
    print("Considering new situation -> ?: ")
    predict = neural_network.think(array([0.032, 25]))
    print('{:.14f}'.format(float(predict)))
