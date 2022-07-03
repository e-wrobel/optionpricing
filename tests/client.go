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
		MaxPrice:         200,
		Volatility:       0.2,
		R:                0.01,
		TMax:             0.9,
		StrikePrice:      138,
		CalculationType:  compute.Nonlinear,
		Beta:             0.0,
		StartPrice:       149,
		MaturityTimeDays: 18,
		ExpectedPrice:    8.1,
		OptionStyle:      compute.European,
	}

	calculatedPrice, calculatedDays, calculatedAssetPrice, calculatedBeta, priceIndexForS0, err := executeRPC(client, incomingRequest)
	if err != nil {
		fmt.Printf("Unable to find beta!: %v", err)
		fmt.Printf("The best fit is for data below:\n")
	}

	fmt.Printf("calculatedPrice: %f, calculatedDays: %d, calculatedAssetPrice: %f, calculatedBeta: %f, priceIndex: %v", calculatedPrice, calculatedDays, calculatedAssetPrice, calculatedBeta, priceIndexForS0)
}

func executeRPC(client stubs.OptionPricingClient, incomingRequest *stubs.ComputeRequest) (float64, int32, float64, float64, int32, error) {
	ctx := context.Background()

	UxtOut, err := client.ComputePrice(ctx, incomingRequest)
	if err != nil {
		return 0, 0, 0, 0, 0, fmt.Errorf("unable to make GRPC request: %v", err)

	}

	calculatedPrice := UxtOut.CalculatedOptionprice
	calculatedDays := UxtOut.CalculatedExpirationDays
	calculatedAssetPrice := UxtOut.CalculatedAssetPrice
	calculatedBeta := UxtOut.CalculatedBeta
	priceIndexForS0 := UxtOut.PriceIndex

	// Convert from struct to [][]
	convertedU := compute.FromStructToMatrix(UxtOut)

	if false {
		fmt.Println("From client:")
		fmt.Println(convertedU)
	}

	return calculatedPrice, calculatedDays, calculatedAssetPrice, calculatedBeta, priceIndexForS0, nil
}
