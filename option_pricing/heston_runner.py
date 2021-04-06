from option_pricing.optionlib.heston_model import HestonModel

if __name__ == '__main__':
    T = 365
    dt = 1 / 252
    S0 = 100  # Initial price
    mu = 0.1  # Expected return
    rho = -0.2  # Correlation
    kappa = 0.03  # Revert rate
    theta = 0.02  # Long-term volatility
    xi = 0.02  # Volatility of instantaneous volatility
    v0 = 0.04  # Initial instantaneous volatility

    plot_dir = '/Users/marcinwroblewski/GolandProjects/optionpricing/option_pricing/option_data'
    h = HestonModel(s0=S0, mu=mu, v0=v0, rho=rho, kappa=kappa, theta=theta, xi=xi, T=T, dt=dt)
    h.generate_brownian_motion()
    S_t, V_t = h.heston_pricing()
    h.plot_heston(s_t=S_t, v_t=V_t, plot_directory=plot_dir)
