package black_scholes

import (
	"github.com/stretchr/testify/assert"
	"testing"
)

func TestAveragePrice(t *testing.T) {
	tests := []struct {
		name          string
		prices        []float64
		expectedPrice float64
	}{
		{
			name:          "test_average_price",
			prices:        []float64{5.5, 20.4, 88.1},
			expectedPrice: 38,
		},
	}

	for _, test := range tests {
		t.Run(test.name, func(t *testing.T) {
			out := average(test.prices)
			assert.Equal(t, out, test.expectedPrice)
		})
	}
}

func TestBlackScholes(t *testing.T) {
	tests := []struct {
		name          string
		obj           *BlackScholes
		expectedPrice float64
	}{
		{
			name: "test_average_price",
			obj: &BlackScholes{
				InitialPrice: 1625.0,
				T:            float64(43) / float64(252),
				K:            1150.0,
				R:            0.03,
				Sigma:        0.2,
			},
			expectedPrice: 500,
		},
	}

	for _, test := range tests {
		t.Run(test.name, func(t *testing.T) {
			out, err := test.obj.SimulateOptionPrice(10000, 1000)
			assert.Greater(t, test.expectedPrice, out)
			assert.NoError(t, err)
		})
	}
}
