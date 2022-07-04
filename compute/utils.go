package compute

import stubs "optionpricing/option"

const (
	Linear       = "Linear"
	Nonlinear    = "NonLinear"
	European     = "European"
	American     = "American"
	spatialSteps = 100
	leftBeta     = -0.25
	rightBeta    = 0.25
)

func FromStructToMatrix(UxtOut *stubs.UxtSlice) [][]float64 {
	convertedU := make([][]float64, 0)
	for _, u := range UxtOut.U {
		convertedU = append(convertedU, u.Ut)
	}

	return convertedU
}

func FromMatrixToStruct(Uxt [][]float64, calculatedPrice float64, calculatedDays int32, calculatedAssetPrice, calculatedBeta float64, priceIndexForS0 int32) *stubs.UxtSlice {
	uSlice := make([]*stubs.Uxt, 0)

	for _, u := range Uxt {
		utStruct := stubs.Uxt{Ut: u}
		uSlice = append(uSlice, &utStruct)
	}

	U := &stubs.UxtSlice{
		U:                        uSlice,
		CalculatedOptionprice:    calculatedPrice,
		CalculatedExpirationDays: calculatedDays,
		CalculatedAssetPrice:     calculatedAssetPrice,
		CalculatedBeta:           calculatedBeta,
		PriceIndex:               priceIndexForS0,
	}

	return U
}
