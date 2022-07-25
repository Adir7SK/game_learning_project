import matplotlib.pyplot as plt
from src.Common_general_functionalities.Gaussian_generated_data import scaled_data

if __name__ == '__main__':
    count, bins, ignored = plt.hist(scaled_data, 30)
    plt.show()
