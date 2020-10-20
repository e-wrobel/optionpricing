package compute

import stubs "optionpricing/option"

const(
	linear = "Linear"
	nonlinear = "NonLinear"
	spatialSteps = 40
)

func FromStructToMatrix(UxtOut *stubs.UxtSlice) [][]float64 {
	convertedU := make([][]float64, 0)
	for _, u := range UxtOut.U {
		convertedU = append(convertedU, u.Ut)
	}

	return convertedU
}

func FromMatrixToStruct(Uxt [][]float64) *stubs.UxtSlice {
	uSlice := make([]*stubs.Uxt, 0)

	for _, u := range Uxt {
		utStruct := stubs.Uxt{Ut: u}
		uSlice = append(uSlice, &utStruct)
	}

	U := &stubs.UxtSlice{U: uSlice}

	return U
}
