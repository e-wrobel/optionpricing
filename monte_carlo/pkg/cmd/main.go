package main

import (
	"fmt"
	"math"
	"optionpricing/monte_carlo/black_scholes"
	"optionpricing/monte_carlo/heston"
	"os"
	"time"
)

func main() {
	// OW20A211150
	now := time.Now()
	blackScholesExample()
	diff := time.Now().Sub(now)
	fmt.Printf("Black-Scholes calculation time minutes: %v, seconds: %v\n", diff.Minutes(), diff.Seconds())

	now = time.Now()
	hestonExample()
	diff = time.Now().Sub(now)
	fmt.Printf("Heston calculation time minutes: %v, seconds: %v\n", diff.Minutes(), diff.Seconds())
}

func hestonExample() {
	h := heston.Heston{
		InitialPrice: 1625.0,
		T:            float64(43) / float64(252),
		K:            1150.0,
		R:            0.03,
		Parameters:   heston.Parameters{},
	}

	// Expected price
	expectedPrice := 848

	parameters, price, found, err := h.FindHestonParameters(heston.Parameters{
		Kappa: 1.0,
		Theta: 1.0,
	}, heston.Parameters{
		Kappa: 15.0,
		Theta: 15.0,
	}, 10, -0.7, math.Pow(0.065, 2), 0.2, expectedPrice, 5, false)
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
