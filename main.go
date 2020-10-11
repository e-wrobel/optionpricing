package main

import "fmt"

func main(){

	spatialSize := 10
	timeSize := 5

	// Two dimensional slice for Uxt
	Uxt := make([][]float64, spatialSize)

	// Initialize two dminesional slice
	for i := range Uxt{
		Uxt[i] = make([]float64, timeSize)
	}

	for i := 0; i < spatialSize; i++ {
		for j := 0; j < timeSize; j++ {
			Uxt[i][j] = float64(i * j)
		}
	}
	fmt.Println(Uxt)

}
