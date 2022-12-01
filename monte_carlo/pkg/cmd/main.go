package main

import (
	"fmt"
	"math"
	"optionpricing/monte_carlo/black_scholes"
	"optionpricing/monte_carlo/heston"
	"os"
)

func main() {
	// OW20A211150
	// now := time.Now()
	// blackScholesExample()
	// diff := time.Now().Sub(now)
	// fmt.Printf("Black-Scholes calculation time minutes: %v, seconds: %v\n", diff.Minutes(), diff.Seconds())

	// now := time.Now()
	// hestonExample()
	// diff := time.Now().Sub(now)
	// fmt.Printf("Heston calculation time minutes: %v, seconds: %v\n", diff.Minutes(), diff.Seconds())

	h := heston.Heston{
		InitialPrice: 1650.0,
		T:            float64(70) / float64(252),
		K:            1200.0,
		R:            0.03,
		Parameters: heston.Parameters{
			V0:      math.Pow(0.045, 2),
			Rho:     -0.7,
			Kappa:   1.906721378588332,
			Theta:   14.791111111111112,
			Epsilon: 0.2,
		},
	}
	price, err := h.SimulateOptionPrice(10000, 1000)
	if err != nil {
		fmt.Printf("err: %v", err)
		os.Exit(1)
	}
	fmt.Printf("Price: %v", price)
}

func hestonExample() {
	h := heston.Heston{
		InitialPrice: 1650.0,
		T:            float64(70) / float64(252),
		K:            1200.0,
		R:            0.03,
		Parameters:   heston.Parameters{},
	}

	// Expected price
	expectedPrice := 824

	parameters, price, found, err := h.FindHestonParameters(heston.Parameters{
		Kappa: 1.0,
		Theta: 13.0,
	}, heston.Parameters{
		Kappa: 3.0,
		Theta: 15.0,
	}, 15, -0.7, math.Pow(0.045, 2), 0.2, expectedPrice, 1, false)
	if err != nil {
		fmt.Printf("Unable to find price: Found error: %v", err)
		os.Exit(1)
	}
	if found {
		fmt.Printf("Found option parameters: %+v, price: %v\n", parameters, price)
	} else {
		fmt.Printf("Didn't find option price for given sigma, but last computation was for parameters: %+v, price: %v\n", parameters, price)
	}
}

func blackScholesExample() {
	maxNumberOfIterations := 10000
	b := &black_scholes.BlackScholes{
		InitialPrice: 1930,
		T:            float64(25) / float64(252),
		K:            2075,
		R:            0.03,
		Sigma:        0,
	}

	// Expected price
	expectedPrice := 0
	left := 0.0
	right := 5.0
	price, sigma, found, err := b.FindImpliedVolatility(left, right, expectedPrice, maxNumberOfIterations)
	if err != nil {
		fmt.Printf("Uable to find price: Found error: %v", err)
		os.Exit(1)
	}
	if found {
		fmt.Printf("Found option price: %v, sigma: %v\n", price, sigma)
	} else {
		fmt.Printf("Didn't find option price for given sigma, but last computation was for price: %v, sigma %v\n", price, sigma)
	}
}
