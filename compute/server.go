package compute

import (
	"context"
	"fmt"
	"net"
	stubs "optionpricing/option"

	"google.golang.org/grpc"
)

type optionPricingServer struct {
	stubs.UnimplementedOptionPricingServer
}

func (o *optionPricingServer) ComputePrice(ctx context.Context, input *stubs.ComputeRequest) (*stubs.UxtSlice, error) {

	var Uxt [][]float64
	var calculatedPrice, beta float64
	var calculatedDays, priceIndexForS0 int32
	var calculatedAssetPrice float64
	var err error
	var U *stubs.UxtSlice

	if input.CalculationType == Linear {
		Uxt, calculatedPrice, calculatedDays, calculatedAssetPrice, priceIndexForS0, err = computeLinearBlackScholes(input.MaxPrice, input.Volatility, input.R, input.TMax, input.StrikePrice, input.Beta, input.StartPrice, input.MaturityTimeDays, input.OptionStyle)
		if err != nil {
			return U, fmt.Errorf("error received from computeLinearBlackScholes: %v", err)
		}
		U = FromMatrixToStruct(Uxt, calculatedPrice, calculatedDays, calculatedAssetPrice, 0, priceIndexForS0)
	} else if input.CalculationType == Nonlinear {
		// If beta in request i 0.0 then it means we want to calibrate it
		if input.Beta == 0.0 {
			Uxt, calculatedPrice, calculatedDays, calculatedAssetPrice, beta, priceIndexForS0, err = calibrateBetaForNonLinearBs(leftBeta, rightBeta, input)
			if err != nil {
				return U, fmt.Errorf("error received from calibrateBetaForNonLinearBs: %v", err)
			}
			U = FromMatrixToStruct(Uxt, calculatedPrice, calculatedDays, calculatedAssetPrice, beta, priceIndexForS0)
			// Otherwise we want just to calculate option price using that particular beta
		} else {
			Uxt, calculatedPrice, calculatedDays, calculatedAssetPrice, priceIndexForS0, err = computeNonLinearBlackScholes(input.MaxPrice,
				input.Volatility, input.R, input.TMax, input.StrikePrice, input.Beta,
				input.StartPrice, input.MaturityTimeDays, input.OptionStyle)
			U = FromMatrixToStruct(Uxt, calculatedPrice, calculatedDays, calculatedAssetPrice, input.Beta, priceIndexForS0)
		}
	}

	return U, nil
}

type optionPricingInterface interface {
	stubs.OptionPricingServer
}

func StartServer() {
	lis, err := net.Listen("tcp", fmt.Sprintf("localhost:%d", 9000))
	if err != nil {
		fmt.Printf("failed to listen: %v", err)
		return
	}

	s := &optionPricingServer{}

	grpcServer := grpc.NewServer()

	stubs.RegisterOptionPricingServer(grpcServer, s)

	if err := grpcServer.Serve(lis); err != nil {
		fmt.Printf("failed to serve: %s", err)
		return
	}
}
