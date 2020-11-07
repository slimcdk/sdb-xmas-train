package gpio


import (
	"github.com/stianeikeland/go-rpio/v4"
)


type Mode rpio.Mode
type State rpio.State
type Pull rpio.Pull
type Edge rpio.Edge
type Pin rpio.Pin


// Pin holds a definition of the output GPIO pin
type PinConfig struct {
	Pin    rpio.Pin
	Inverted bool
}

