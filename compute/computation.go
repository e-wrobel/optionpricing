package compute

import (
	"math"
)

func computeLinearBlackScholes(maxPrice, volatility, r, tMax, strikePrice, beta float64) [][]float64 {

	// Spatial differential
	ds := maxPrice / spatialSteps
	//ds = 56.41025641025641

	ds2 := math.Pow(ds, 2)
	maxPrice2 := math.Pow(maxPrice, 2)
	volatility2 := math.Pow(volatility, 2)

	// Time differential
	dt := ds2 / (float64(spatialSteps-1)*volatility2 + 0.5*r) / maxPrice2

	spatialSize := int(maxPrice / ds)
	timeSize := int(tMax / dt)

	// Two dimensional slice for Uxt
	Uxt := make([][]float64, spatialSize)

	// Initialize 2D slice - option price
	for i := range Uxt {
		Uxt[i] = make([]float64, timeSize)
	}

	// Prepare values for price slice
	priceSlice := make([]float64, spatialSize)
	for i := 0; i < spatialSize; i++ {
		priceSlice[i] = float64(i) * ds
	}

	// Prepare values for time slice
	timeSlice := make([]float64, timeSize)
	for i := 0; i < timeSize; i++ {
		timeSlice[i] = float64(i) * dt
	}

	// Initial condition
	for i := 0; i < spatialSize; i++ {
		s := priceSlice[i]
		Uxt[i][0] = math.Max(s-strikePrice, 0)
	}

	// Main loop stands for moving across time slice
	for tIndex := 1; tIndex < timeSize; tIndex++ {
		// Second loops stands for calculating Uxt at given t value and for every price in priceSlice
		for sIndex := 1; sIndex < spatialSize-1; sIndex++ {
			s := priceSlice[sIndex]

			R1 := -r * Uxt[sIndex][tIndex-1]
			R2 := r * s * (Uxt[sIndex+1][tIndex-1] - Uxt[sIndex-1][tIndex-1]) / (2 * ds)
			R3 := 0.5 * volatility2 * (math.Pow(s, 2)) * (Uxt[sIndex-1][tIndex-1] - 2*Uxt[sIndex][tIndex-1] + Uxt[sIndex+1][tIndex-1]) / ds2

			R := R1 + R2 + R3

			// Runge-Kutta4 coeficients
			k1 := dt * R
			k2 := dt * (R + 0.5*k1)
			k3 := dt * (R + 0.5*k2)
			k4 := dt * (R + k3)

			// Deriviated function in time domain
			Uxt[sIndex][tIndex] = Uxt[sIndex][tIndex-1] + (1.0/6.0)*(k1+2.0*k2+2.0*k3+k4)
		}

		//Insert boundary conditions / Runge-Kutta at s = 0, and s = s_max
		Uxt[0][tIndex] = 0
		Uxt[spatialSize -1][tIndex] = priceSlice[spatialSize -1] - strikePrice

	}

	return Uxt
}
