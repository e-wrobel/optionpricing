package compute

func computeMatrix(params ...float32) [][]float32 {
	spatialSize := 5
	timeSize := 3

	// Two dimensional slice for Uxt
	Uxt := make([][]float32, spatialSize)

	// Initialize 2D slice
	for i := range Uxt {
		Uxt[i] = make([]float32, timeSize)
	}

	for i := 0; i < spatialSize; i++ {
		for j := 0; j < timeSize; j++ {
			Uxt[i][j] = float32(i * j)
		}
	}
	return Uxt
}
