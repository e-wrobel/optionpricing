package main

import (
	"fmt"
	"optionpricing/monte_carlo/black_scholes"
	"optionpricing/monte_carlo/heston"
	"os"
)

func main() {
	// OW20A211150
	blackScholesExample()
	hestonExample()
}

func hestonExample() {
	h := heston.Heston{
		InitialPrice: 1400.0,
		T:            float64(43) / float64(252),
		K:            1200.0,
		R:            0.03,
		Parameters:   heston.Parameters{},
	}
	parameters, price, found, err := h.FindHestonParameters(heston.Parameters{
		V0:      0.06,
		Rho:     -0.7,
		Kappa:   9.0,
		Theta:   9.0,
		Epsilon: 0.1,
	}, heston.Parameters{
		V0:      0.07,
		Rho:     -0.5,
		Kappa:   10,
		Theta:   11,
		Epsilon: 0.2,
	}, 10, 577, 5)
	if err != nil {
		fmt.Printf("Uable to find price: Found error: %v", err)
		os.Exit(1)
	}
	if found {
		fmt.Printf("Found option parameters: %+v, price: %v", parameters, price)
	} else {
		fmt.Printf("Didn't find option price for given sigma, but last computation was for parameters: %+v, price: %v", parameters, price)
	}
}

func blackScholesExample() {
	maxNumberOfIterations := 10000
	b := &black_scholes.BlackScholes{
		InitialPrice: 1625,
		T:            float64(43) / float64(252),
		K:            1150,
		R:            0.03,
		Sigma:        0,
	}

	//
	expectedPrice := 848
	left := 0.1
	right := 3.0
	price, sigma, found, err := b.FindImpliedVolatility(left, right, expectedPrice, maxNumberOfIterations)
	if err != nil {
		fmt.Printf("Uable to find price: Found error: %v", err)
		os.Exit(1)
	}
	if found {
		fmt.Printf("Found option price: %v, sigma: %v", price, sigma)
	} else {
		fmt.Printf("Didn't find option price for given sigma, but last computation was for price: %v, sigma %v", price, sigma)
	}
}
