package main

import (
	"optionpricing/compute"
)

func main() {

	// Server's code
	go func() {
		compute.StartServer()
	}()

	// Client's code
	compute.StartClient()

}
