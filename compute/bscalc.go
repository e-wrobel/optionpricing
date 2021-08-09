package compute

import "math"

func PriceBlackScholes(callType bool, underlying float64, strike float64, timeToExpiration float64, volatility float64, riskFreeInterest float64, dividend float64) float64 {

	var sign float64
	if callType {
		if timeToExpiration <= 0 {
			return math.Abs(underlying - strike)
		}
		sign = 1
	} else {
		if timeToExpiration <= 0 {
			return math.Abs(strike - underlying)
		}
		sign = -1
	}

	if sign == 0 {
		return 0.0
	}

	re := math.Exp(-riskFreeInterest * timeToExpiration)
	qe := math.Exp(-dividend * timeToExpiration)
	vt := volatility * (math.Sqrt(timeToExpiration))
	d1 := d1f(underlying, strike, timeToExpiration, volatility, riskFreeInterest, dividend, vt)
	d2 := d2f(d1, vt)
	d1 = sign * d1
	d2 = sign * d2
	nd1 := Stdnorm.Cdf(d1)
	nd2 := Stdnorm.Cdf(d2)

	bsprice := sign * ((underlying * qe * nd1) - (strike * re * nd2))
	return bsprice
}

func d1f(underlying float64, strike float64, timeToExpiration float64, volatility float64, riskFreeInterest float64, dividend float64, volatilityWithExpiration float64) float64 {
	d1 := math.Log(underlying/strike) + (timeToExpiration * (riskFreeInterest - dividend + ((volatility * volatility) * 0.5)))
	d1 = d1 / volatilityWithExpiration
	return d1
}

func d2f(d1 float64, volatilityWithExpiration float64) float64 {
	d2 := d1 - volatilityWithExpiration
	return d2
}