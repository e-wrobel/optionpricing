package black_scholes

import (
	"gonum.org/v1/gonum/stat/distuv"
	"math"
)

type BlackScholes struct {
	InitialPrice float64
	T            float64
	K            float64
	R            float64
	Sigma        float64
}

func (b *BlackScholes) SimulateOptionPrice(numberOfPaths, numberOfTimeSteps int) (float64, error) {
	S := make([]float64, numberOfPaths, numberOfPaths)
	dt := b.T / float64(numberOfTimeSteps)

	// Init price vector with initial price.
	for i := 0; i < numberOfPaths; i++ {
		S[i] = b.InitialPrice
	}

	for t := 1; t < numberOfTimeSteps; t++ {
		Z := normalDistributedSlice(numberOfPaths)

		for i := 0; i < numberOfPaths; i++ {
			S[i] = S[i] * math.Exp((b.R-0.5*math.Pow(b.Sigma, 2))*dt+b.Sigma*math.Sqrt(dt)*Z[i])
		}
	}

	averagePrices := make([]float64, numberOfPaths, numberOfPaths)
	for i := 0; i < numberOfPaths; i++ {
		averagePrices[i] = math.Max(S[i]-b.K, 0)
	}
	averagePrice := average(averagePrices)

	return averagePrice, nil
}

func average(priceSlice []float64) float64 {
	averagePrice := 0.0
	for _, price := range priceSlice {
		averagePrice += price
	}

	return averagePrice / float64(len(priceSlice))
}

func normalDistributedSlice(n int) []float64 {
	// use the defined variable
	dist := distuv.UnitNormal

	z := make([]float64, n)

	// Generate some random numbers from standard normal distribution.
	for i := range z {
		z[i] = dist.Rand()
	}

	return z
}
