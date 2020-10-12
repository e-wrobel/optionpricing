package main

import (
	"context"
	"fmt"
	"log"
	stubs "optionpricing/option"
	"os"

	"google.golang.org/grpc"
)

func main() {

	spatialSize := 10
	timeSize := 5

	// Two dimensional slice for Uxt
	Uxt := make([][]float32, spatialSize)

	// Initialize two dminesional slice
	for i := range Uxt {
		Uxt[i] = make([]float32, timeSize)
	}

	for i := 0; i < spatialSize; i++ {
		for j := 0; j < timeSize; j++ {
			Uxt[i][j] = float32(i * j)
		}
	}
	fmt.Println(Uxt)

	// Client's code
	log.Println("Client running ...")
	conn, err := grpc.Dial("localhost:50051", grpc.WithInsecure())
	if err != nil {
		log.Fatalln(err)
	}
	defer conn.Close()

	client := stubs.NewOptionPricingClient(conn)

	ctx := context.Background()
	incommingRequest := stubs.ComputeRequest{Params: []string{"10", "dupa"}}
	UxtOut, err := client.ComputePrice(ctx, &incommingRequest)
	if err != nil {
		fmt.Printf("unable to make Client request: %v", err)
		os.Exit(1)

	}

	// End of Client's code

	fmt.Println(UxtOut)

}
