package compute

import stubs "optionpricing/option"

func FromStructToMatrix(UxtOut *stubs.UxtSlice) [][]float32 {
	convertedU := make([][]float32, 0)
	for _, u := range UxtOut.U {
		convertedU = append(convertedU, u.Ut)
	}

	return convertedU
}

func FromMatrixToStruct(Uxt [][]float32) *stubs.UxtSlice {
	uSlice := make([]*stubs.Uxt, 0)

	for _, u := range Uxt {
		utStruct := stubs.Uxt{Ut: u}
		uSlice = append(uSlice, &utStruct)
	}

	U := &stubs.UxtSlice{U: uSlice}

	return U
}
