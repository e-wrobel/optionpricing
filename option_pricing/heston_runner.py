from option_pricing.optionlib.heston_model import HestonModel


def generate_scenarios(from_number, to_number, step):
    x = from_number
    numbers = []
    while x < to_number:
        numbers.append(x)
        x = x + step

    return numbers


class Solution(object):
    def __init__(self, initial_variance, epsilon, rho, kappa, calculated_price, desired_price):
        self.initial_variance = initial_variance
        self.epsilon = epsilon
        self.rho = rho
        self.kappa = kappa
        self.calculated_price = calculated_price
        self.desired_price = desired_price

    def __str__(self):
        out = 'Initial variance: {}, epsilon: {}, rho: {}, kappa: {}, calclutaed price: {}, desired price: {}'.format(
            self.initial_variance,
            self.epsilon,
            self.rho,
            self.kappa,
            self.calculated_price,
            self.desired_price
        )

        return out


if __name__ == '__main__':
    # OW20A211975
    N = 1000  # Number of small sub-steps (time)
    n = 10000  # Number of Monte carlo paths

    S_0 = 1663.75  # Initial stock price
    K = 1800  # Strike price
    V_0 = 0.56  # Initial variance is square of volatility
    kappa = 1  # kappa mean reversion speed
    theta = 0.03  # Long-run variance
    epsilon = 0.3  # volatility of volatility
    rho = 0.0  # correlation
    T = 88 / 252  # time to maturity

    h = HestonModel(s0=S_0, initial_variance=V_0, rho=rho, kappa=kappa, theta=theta, epsilon=epsilon, T=T, K=K)
    price = h.option_pricing(number_of_montecarlo_paths=n, number_of_time_steps=N)
    # # plot_dir = '/Users/marcinwroblewski/GolandProjects/optionpricing/option_pricing/option_data'

    print(price)
    # initial_variances = generate_scenarios(0.01, theta, 0.05 * theta)
    # epsilons = generate_scenarios(0.01, 0.02, 0.001)
    # rhos = generate_scenarios(-1.0, 1.0, 0.2)
    # kappas = generate_scenarios(0.0, 5.0, 1.0)
    #
    # total_loops = len(initial_variances) * len(epsilons) * len(rhos) * len(kappas)
    # print('Max number of loops: {}\n'.format(total_loops))
    # j = 0
    #
    # s = None
    # desired_price = 26.35
    # for i in initial_variances:
    #     j += 1
    #     for e in epsilons:
    #         j += 1
    #         for k in kappas:
    #             j += 1
    #             for r in rhos:
    #                 j += 1
    #                 h = HestonModel(s0=S_0, initial_variance=i, rho=r, kappa=k, theta=theta, epsilon=e, T=T, K=K)
    #                 price = h.option_pricing(number_of_montecarlo_paths=n, number_of_time_steps=N)
    #                 if j % 10 == 0:
    #                     print("Number of loops: {}, {}%, price calculated: {}, price desired: {}".format(j,
    #                                                                                                      j / total_loops * 100,
    #                                                                                                      price,
    #                                                                                                      desired_price))
    #                 if abs(price - desired_price) / desired_price < 0.1:
    #                     s = Solution(initial_variance=i, epsilon=e, rho=r, kappa=k, calculated_price=price,
    #                                  desired_price=desired_price)
    #                     break
    #
    # print(s)
