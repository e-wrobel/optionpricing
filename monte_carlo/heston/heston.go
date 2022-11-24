package heston

import (
	"fmt"
	"gonum.org/v1/gonum/stat/distuv"
	"math"
)

type Heston struct {
	InitialPrice    float64
	T               float64
	K               float64
	R               float64
	InitialVariance float64
	Rho             float64
	Kappa           float64
	Theta           float64
	Epsilon         float64
}

func (h *Heston) SimulateOptionPrice(numberOfPaths, numberOfTimeSteps int) (float64, error) {
	S := make([]float64, numberOfPaths, numberOfPaths)
	V := make([]float64, numberOfPaths, numberOfPaths)

	dt := h.T / float64(numberOfTimeSteps)

	if numberOfPaths == 0 || numberOfTimeSteps == 0 {
		return 0, fmt.Errorf("incorrect number of steps")
	}
	// Init price vector with initial price.
	for i := 0; i < numberOfPaths; i++ {
		S[i] = h.InitialPrice
	}

	// Init variance vector with initial variance.
	for i := 0; i < numberOfPaths; i++ {
		V[i] = h.InitialVariance
	}

	for t := 1; t < numberOfTimeSteps; t++ {
		// Random numbers for S_t and V_t.
		Zs := normalDistributedSlice(numberOfPaths)
		Zv := normalModifiedDistributedSlice(Zs, h.Rho, numberOfPaths)

		for i := 0; i < numberOfPaths; i++ {
			exp := math.Exp((h.R-0.5*V[i])*dt + math.Sqrt(V[i]*dt)*Zs[i])
			S[i] = S[i] * exp
		}

		// Volatility process
		for i := 0; i < numberOfPaths; i++ {
			V[i] = math.Max(V[i]+h.Kappa*(h.Theta-V[i])*dt+h.Epsilon*math.Sqrt(V[i]*dt)*Zv[i], 0)
		}
	}

	optionPrices := make([]float64, numberOfPaths, numberOfPaths)
	for i := 0; i < numberOfPaths; i++ {
		optionPrices[i] = math.Max(S[i]-h.K, 0)
	}
	averagePrice := average(optionPrices)

	return averagePrice, nil
}

func average(priceSlice []float64) float64 {
	var averagePrice float64
	for _, price := range priceSlice {
		averagePrice += price
	}

	return averagePrice / float64(len(priceSlice))
}

func normalDistributedSlice(n int) []float64 {
	dist := distuv.UnitNormal

	z := make([]float64, n)

	// Generate some random numbers from standard normal distribution.
	for i := range z {
		z[i] = dist.Rand()
	}

	return z
}

func normalModifiedDistributedSlice(normalDistribution []float64, rho float64, n int) []float64 {
	independentNormDist := normalDistributedSlice(n)
	z := make([]float64, n, n)

	// Generate some random numbers from standard normal distribution.
	for i := 0; i < n; i++ {
		z[i] = rho*normalDistribution[i] - math.Sqrt(1.0-math.Pow(rho, 2))*independentNormDist[i]
	}

	return z
}