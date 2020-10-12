package main

import (
	"context"
	stubs "optionpricing/option"
)

type optionPricingServer struct {}

func (o *optionPricingServer) ComputePrice(ctx context.Context, input *stubs.ComputeRequest) (*stubs.UxtSlice, error) {
	panic("implement me")
}

type optionPricingInterface interface {
	stubs.OptionPricingServer
}