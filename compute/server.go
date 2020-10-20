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
	if input.CalculationType == linear {
		Uxt = computeLinearBlackScholes(input.MaxPrice, input.Volatility, input.R, input.TMax, input.StrikePrice, input.Beta)
	}
	U := FromMatrixToStruct(Uxt)

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
