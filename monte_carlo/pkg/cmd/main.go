package main

import (
	"fmt"
	"optionpricing/monte_carlo/black_scholes"
	"os"
)

func main() {
	// OW20A211150
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
