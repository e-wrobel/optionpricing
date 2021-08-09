package main

import (
	"context"
	"fmt"
	"log"
	"optionpricing/compute"
	stubs "optionpricing/option"

	"google.golang.org/grpc"
)

func main() {
	// Client's code
	log.Println("Client running ...")
	conn, err := grpc.Dial("localhost:9000", grpc.WithInsecure())
	if err != nil {
		log.Fatalln(err)
	}
	defer conn.Close()

	client := stubs.NewOptionPricingClient(conn)

	incomingRequest := &stubs.ComputeRequest{
		MaxPrice:         2350,
		Volatility:       0.2,
		R:                0.01,
		TMax:             0.9,
		StrikePrice:      1500,
		CalculationType:  compute.Linear,
		Beta:             0.001,
		StartPrice:       1400,
		MaturityTimeDays: 40,
		ExpectedPrice:    20,
		OptionStyle:      compute.American,
	}

	calculatedPrice, calculatedDays, calculatedAssetPrice, calculatedBeta, err := executeRPC(client, incomingRequest)
	if err != nil {
		fmt.Printf("Unable to find beta!: %v", err)
		fmt.Printf("The best fit is for data below:\n")
	}

	fmt.Printf("calculatedPrice: %f, calculatedDays: %d, calculatedAssetPrice: %f, calculatedBeta: %f", calculatedPrice, calculatedDays, calculatedAssetPrice, calculatedBeta)
}

func executeRPC(client stubs.OptionPricingClient, incomingRequest *stubs.ComputeRequest) (float64, int32, float64, float64, error) {
	ctx := context.Background()

	UxtOut, err := client.ComputePrice(ctx, incomingRequest)
	if err != nil {
		return 0, 0, 0, 0, fmt.Errorf("unable to make GRPC request: %v", err)

	}

	calculatedPrice := UxtOut.CalculatedOptionprice
	calculatedDays := UxtOut.CalculatedExpirationDays
	calculatedAssetPrice := UxtOut.CalculatedAssetPrice
	calculatedBeta := UxtOut.CalculatedBeta

	// Convert from struct to [][]
	convertedU := compute.FromStructToMatrix(UxtOut)

	if false {
		fmt.Println("From client:")
		fmt.Println(convertedU)
	}

	return calculatedPrice, calculatedDays, calculatedAssetPrice, calculatedBeta, nil
}
