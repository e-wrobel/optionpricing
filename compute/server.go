package compute

import (
	"context"
	"fmt"
	"net"
	stubs "optionpricing/option"

	"google.golang.org/grpc"
)

type optionPricingServer struct{}

func (o *optionPricingServer) ComputePrice(ctx context.Context, input *stubs.ComputeRequest) (*stubs.UxtSlice, error) {

	var Uxt [][]float64
	var calculatedPrice float64
	var calculatedDays int32
	var calculatedAssetPrice float64
	var err error
	var U *stubs.UxtSlice

	if input.CalculationType == linear {
		Uxt, calculatedPrice, calculatedDays, calculatedAssetPrice, err = computeLinearBlackScholes(input.MaxPrice, input.Volatility, input.R, input.TMax, input.StrikePrice, input.Beta, input.StartPrice, input.MaturityTimeDays)
		if err != nil {
			return U, fmt.Errorf("error received from computeLinearBlackScholes: %v", err)
		}
		U = FromMatrixToStruct(Uxt, calculatedPrice, calculatedDays, calculatedAssetPrice)
	} else if input.CalculationType == nonlinear {
		Uxt, calculatedPrice, calculatedDays, calculatedAssetPrice, err = computeNonLinearBlackScholes(input.MaxPrice, input.Volatility, input.R, input.TMax, input.StrikePrice, input.Beta, input.StartPrice, input.MaturityTimeDays)
		if err != nil {
			return U, fmt.Errorf("error received from computeLinearBlackScholes: %v", err)
		}
		U = FromMatrixToStruct(Uxt, calculatedPrice, calculatedDays, calculatedAssetPrice)
	}

	return U, nil
}

type optionPricingInterface interface {
	stubs.OptionPricingServer
}

func StartServer() {
	lis, err := net.Listen("tcp", fmt.Sprintf(":%d", 9000))
	if err != nil {
		fmt.Printf("failed to listen: %v", err)
		return
	}

	s := optionPricingServer{}

	grpcServer := grpc.NewServer()

	stubs.RegisterOptionPricingServer(grpcServer, &s)

	if err := grpcServer.Serve(lis); err != nil {
		fmt.Printf("failed to serve: %s", err)
		return
	}
}
