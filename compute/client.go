package compute

import (
	"context"
	"fmt"
	"log"
	stubs "optionpricing/option"
	"os"

	"google.golang.org/grpc"
)

const numberOfSteps = 100

func StartClient() {
	// Client's code
	log.Println("Client running ...")
	conn, err := grpc.Dial("localhost:9000", grpc.WithInsecure())
	if err != nil {
		log.Fatalln(err)
	}
	defer conn.Close()

	client := stubs.NewOptionPricingClient(conn)

	expectedOptionPrice := 120.0
	leftBeta := -0.00005
	rightBeta := 0.0095
	incomingRequest := &stubs.ComputeRequest{
		MaxPrice:         2350,
		Volatility:       0.02,
		R:                0.03,
		TMax:             0.9,
		StrikePrice:      1650,
		CalculationType:  nonlinear,
		Beta:             0,
		StartPrice:       1800,
		MaturityTimeDays: 35,
	}

	calculatedPrice, calculatedDays, calculatedAssetPrice, currentBeta, err := calibrateBetaForOptionPrice(client, expectedOptionPrice, leftBeta, rightBeta, incomingRequest)
	if err != nil {
		fmt.Printf("Unable to find beta!: %v", err)
		fmt.Printf("The best fit is for data below:\n")
	}

	fmt.Printf("calculatedPrice: %v, calculatedDays: %v, calculatedAssetPrice: %v, currentBeta: %v", calculatedPrice, calculatedDays, calculatedAssetPrice, currentBeta)
}

func calibrateBetaForOptionPrice(client stubs.OptionPricingClient, expectedOptionPrice float64, leftBeta, rightBeta float64, incommingRequest *stubs.ComputeRequest) (float64, int32, float64, float64, error) {
	var calculatedPrice, calculatedAssetPrice, middleBeta float64
	var calculatedDays int32
	isFound := false
	i := 0

	for leftBeta <= rightBeta {
		middleBeta = (leftBeta + rightBeta) / 2
		incommingRequest.Beta = middleBeta
		calculatedPrice, calculatedDays, calculatedAssetPrice = executeRPC(client, incommingRequest)
		if int32(calculatedPrice) == int32(expectedOptionPrice) {
			isFound = true
			break
		}
		if calculatedPrice < expectedOptionPrice {
			rightBeta = middleBeta
		} else {
			leftBeta = middleBeta
		}

		i++

		if i > numberOfSteps {
			break
		}
	}

	if !isFound {
		return calculatedPrice, calculatedDays, calculatedAssetPrice, middleBeta, fmt.Errorf("unable to find the right value")
	}

	fmt.Printf("Number of steps: %v\n", i)
	return calculatedPrice, calculatedDays, calculatedAssetPrice, middleBeta, nil
}

func executeRPC(client stubs.OptionPricingClient, incomingRequest *stubs.ComputeRequest) (float64, int32, float64) {
	ctx := context.Background()


	UxtOut, err := client.ComputePrice(ctx, incomingRequest)
	if err != nil {
		fmt.Printf("unable to make Client request: %v", err)
		os.Exit(1)

	}

	calculatedPrice := UxtOut.CalculatedOptionprice
	calculatedDays := UxtOut.CalculatedExpirationDays
	calculatedAssetPrice := UxtOut.CalculatedAssetPrice

	// Convert from struct to [][]
	convertedU := FromStructToMatrix(UxtOut)

	if false {
		fmt.Println("From client:")
		fmt.Println(convertedU)
	}

	return calculatedPrice, calculatedDays, calculatedAssetPrice
}
