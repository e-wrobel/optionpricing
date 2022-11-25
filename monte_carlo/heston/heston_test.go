package heston

import (
	"github.com/stretchr/testify/assert"
	"testing"
)

func TestHeston(t *testing.T) {
	tests := []struct {
		name             string
		obj              *Heston
		minExpectedPrice float64
	}{
		{
			name: "test_average_price",
			obj: &Heston{
				InitialPrice: 1400.0,
				T:            float64(43) / float64(252),
				K:            1200.0,
				R:            0.03,
				Parameters: Parameters{
					V0:      0.065,
					Rho:     -0.7,
					Kappa:   9.0,
					Theta:   11.0,
					Epsilon: 0.1,
				},
			},
			minExpectedPrice: 500,
		},
	}

	for _, test := range tests {
		t.Run(test.name, func(t *testing.T) {
			out, err := test.obj.SimulateOptionPrice(10000, 1000)
			assert.Greater(t, test.minExpectedPrice, out)
			assert.NoError(t, err)
		})
	}
}
