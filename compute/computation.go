package compute

import (
	"fmt"
	"math"
	stubs "optionpricing/option"
)

const daysInYear = 252.0
const numberOfSteps = 10009

func computeLinearBlackScholes(maxPrice, volatility, r, tMax, strikePrice, beta, s0 float64, t int32, optionStyle string) ([][]float64, float64, int32, float64, int32, error) {
	isFound := false
	var calculatedPrice float64
	var calculatedDays, priceIndexForS0 int32
	var calculatedAssetPrice float64
	dailyVolatility := volatility / (math.Sqrt(float64(t)))

	// Spatial differential
	ds := maxPrice / spatialSteps
	ds2 := math.Pow(ds, 2)
	maxPrice2 := math.Pow(maxPrice, 2)
	volatility2 := math.Pow(volatility, 2)

	// Time differential
	dt := ds2 / (float64(spatialSteps-1)*volatility2 + 0.5*r) / maxPrice2
	dt = 0.005
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
			if optionStyle == American {
				bsPrice := PriceBlackScholes(true, s, strikePrice, 1, dailyVolatility, r, 0.0)
				if bsPrice >= Uxt[sIndex][tIndex] {
					Uxt[sIndex][tIndex] = bsPrice
				}
			}

			currentTimeYears := dt * float64(tIndex)

			// Check option price for given asset price and maturity T
			if currentTimeYears >= float64(t)/daysInYear && s >= s0 && !isFound {
				isFound = true
				calculatedPrice = Uxt[sIndex][tIndex]
				calculatedDays = int32(currentTimeYears * daysInYear)
				calculatedAssetPrice = s
				priceIndexForS0 = int32(sIndex)
			}
		}

		//Insert boundary conditions / Runge-Kutta at s = 0, and s = s_max
		Uxt[0][tIndex] = 0
		Uxt[spatialSize-1][tIndex] = priceSlice[spatialSize-1] - strikePrice

	}

	if !isFound {
		return Uxt, 0, 0, 0, 0, fmt.Errorf("unable to find option parameters")
	}

	return Uxt, calculatedPrice, calculatedDays, calculatedAssetPrice, priceIndexForS0, nil
}

func computeNonLinearBlackScholes(maxPrice, volatility, r, tMax, strikePrice, beta, s0 float64, t int32, optionStyle string) ([][]float64, float64, int32, float64, int32, error) {
	var calculatedPrice float64
	var calculatedDays, priceIndexForS0 int32
	var calculatedAssetPrice float64
	dailyVolatility := volatility / (math.Sqrt(float64(t)))

	// Spatial differential
	ds := maxPrice / spatialSteps
	ds2 := math.Pow(ds, 2)
	volatility2 := math.Pow(volatility, 2)

	// Time differential
	dt := 1.0 / 252.0
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
			R1 := -r*Uxt[sIndex][tIndex-1] - beta*math.Pow(Uxt[sIndex][tIndex-1], 3)
			R2 := r * s * (Uxt[sIndex+1][tIndex-1] - Uxt[sIndex-1][tIndex-1]) / (2 * ds)
			R3 := 0.5 * volatility2 * (math.Pow(s, 2)) * (Uxt[sIndex-1][tIndex-1] - 2*Uxt[sIndex][tIndex-1] + Uxt[sIndex+1][tIndex-1]) / ds2

			R := R1 + R2 + R3

			// Runge-Kutta4 coefficients
			k1 := dt * R
			k2 := dt * (R + 0.5*k1)
			k3 := dt * (R + 0.5*k2)
			k4 := dt * (R + k3)

			// Derived function in time domain
			Uxt[sIndex][tIndex] = Uxt[sIndex][tIndex-1] + (1.0/6.0)*(k1+2.0*k2+2.0*k3+k4)
			if optionStyle == American {
				bsPrice := PriceBlackScholes(true, s, strikePrice, 1, dailyVolatility, r, 0.0)
				if bsPrice > Uxt[sIndex][tIndex] {
					Uxt[sIndex][tIndex] = bsPrice
				}
			}

			currentTimeYears := dt * float64(tIndex)

			// Check option price for given asset price and maturity T
			if currentTimeYears >= float64(t)/daysInYear && s >= s0 {
				calculatedPrice = Uxt[sIndex][tIndex]
				calculatedDays = int32(currentTimeYears * daysInYear)
				calculatedAssetPrice = s
				priceIndexForS0 = int32(sIndex)

				if math.IsNaN(calculatedPrice) {
					fmt.Printf("CalculatedPris is NAN\n")
					return Uxt, 0, 0, 0, 0, fmt.Errorf("calculatedPrice is NAN")
				}

				return Uxt, calculatedPrice, calculatedDays, calculatedAssetPrice, priceIndexForS0, nil
			}
		}

		// Insert boundary conditions / Runge-Kutta at s = 0, and s = s_max
		Uxt[0][tIndex] = 0
		Uxt[spatialSize-1][tIndex] = priceSlice[spatialSize-1] - strikePrice

	}

	return Uxt, 0, 0, 0, 0, fmt.Errorf("unable to find option parameters")

}

func calibrateBetaForNonLinearBs(leftBeta, rightBeta float64, incommingRequest *stubs.ComputeRequest) ([][]float64, float64, int32, float64, float64, int32, error) {
	var calculatedPrice, calculatedAssetPrice, middleBeta float64
	var calculatedDays, priceIndexForS0 int32
	var Uxt [][]float64
	var err error
	i := 0

	// Calculate for beta = 0 aka linear model
	Uxt, calculatedPrice, calculatedDays, calculatedAssetPrice, priceIndexForS0, err = computeNonLinearBlackScholes(incommingRequest.MaxPrice,
		incommingRequest.Volatility, incommingRequest.R, incommingRequest.TMax, incommingRequest.StrikePrice, 0,
		incommingRequest.StartPrice, incommingRequest.MaturityTimeDays, incommingRequest.OptionStyle)
	if err != nil {
		return Uxt, calculatedPrice, calculatedDays, calculatedAssetPrice, 0, 0, fmt.Errorf("computation error: %v", err)
	}
	if int32(calculatedPrice) == int32(incommingRequest.ExpectedPrice) {
		return Uxt, calculatedPrice, calculatedDays, calculatedAssetPrice, 0, priceIndexForS0, nil
	}

	// Calculate for beta != 0
	for leftBeta < rightBeta {
		middleBeta = (leftBeta + rightBeta) / 2
		incommingRequest.Beta = middleBeta
		Uxt, calculatedPrice, calculatedDays, calculatedAssetPrice, priceIndexForS0, err = computeNonLinearBlackScholes(incommingRequest.MaxPrice,
			incommingRequest.Volatility, incommingRequest.R, incommingRequest.TMax, incommingRequest.StrikePrice, incommingRequest.Beta,
			incommingRequest.StartPrice, incommingRequest.MaturityTimeDays, incommingRequest.OptionStyle)
		if err != nil {
			return Uxt, calculatedPrice, calculatedDays, calculatedAssetPrice, middleBeta, 0, fmt.Errorf("computation error: %v", err)
		}
		if int32(calculatedPrice) == int32(incommingRequest.ExpectedPrice) {
			break
		}
		if calculatedPrice < incommingRequest.ExpectedPrice {
			rightBeta = middleBeta
		} else {
			leftBeta = middleBeta
		}

		i++

		if i > numberOfSteps {
			fmt.Printf("Number of steps: %v\n, stopping", i)
			break
		}
	}
	if calculatedPrice < 0 {
		calculatedPrice = 0.0
	}

	fmt.Printf("Number of steps: %v\n", i)
	return Uxt, calculatedPrice, calculatedDays, calculatedAssetPrice, middleBeta, priceIndexForS0, nil
}
