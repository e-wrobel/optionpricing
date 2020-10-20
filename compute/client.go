package compute

import (
	"context"
	"fmt"
	"log"
	stubs "optionpricing/option"
	"os"

	"google.golang.org/grpc"
)

func StartClient() {
	// Client's code
	log.Println("Client running ...")
	conn, err := grpc.Dial("localhost:9000", grpc.WithInsecure())
	if err != nil {
		log.Fatalln(err)
	}
	defer conn.Close()

	client := stubs.NewOptionPricingClient(conn)

	ctx := context.Background()
	incomingRequest := stubs.ComputeRequest{
		MaxPrice:        2200,
		Volatility:      0.2,
		R:               0.03,
		TMax:            0.9,
		StrikePrice:     1200,
		CalculationType: linear,
		Beta:            0.000001,
	}

	UxtOut, err := client.ComputePrice(ctx, &incomingRequest)
	if err != nil {
		fmt.Printf("unable to make Client request: %v", err)
		os.Exit(1)

	}

	// Convert from struct to [][]
	convertedU := FromStructToMatrix(UxtOut)

	fmt.Println("From client:")
	fmt.Println(convertedU)
}
