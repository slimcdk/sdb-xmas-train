package gpio

import (
	"github.com/stianeikeland/go-rpio/v4"
)

// Open https://github.com/stianeikeland/go-rpio/blob/acc952dac3eb73de3a6d78dbf7fee5644a24ec96/rpio.go#L704
func Open() error {
	err := rpio.Open()
	return err
}

// Close https://github.com/stianeikeland/go-rpio/blob/acc952dac3eb73de3a6d78dbf7fee5644a24ec96/rpio.go#L776
func Close() error {
	err := rpio.Close()
	return err
}



// High takes the inverted state into context
func (pc *PinConfig) High() {
	if pc.Inverted { pc.Pin.Low() } else { pc.Pin.High() }
}


// Low takes the inverted state into context
func (pc *PinConfig) Low() {
	if pc.Inverted { pc.Pin.High() } else { pc.Pin.Low() }
}

// Low takes the inverted state into context
func (pc *PinConfig) Toggle() {
	pc.Pin.Toggle()
}

// Write TODO
func (pc *PinConfig) DutyCycle (dutyLen, cycleLen uint32) {

	newDutyLength := dutyLen

	if pc.Inverted {
		newDutyLength = ^uint32(0) - dutyLen
	}

	pc.Pin.DutyCycle(newDutyLength, cycleLen)
}
