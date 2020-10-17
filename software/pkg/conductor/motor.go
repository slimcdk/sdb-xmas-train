package conductor

import (
	"github.com/stianeikeland/go-rpio/v4"
)

// Motor TODO
type Motor struct {
	ControlPin    rpio.Pin
	DirectionPin  rpio.Pin
	MotorRelayPin rpio.Pin
}

// Initialize opens memory range for GPIO access in /dev/mem
func (m *Motor) Initialize() error {
	err := rpio.Open()
	return err
}

// Close unmap memory when done
func (m *Motor) Close() error {
	err := rpio.Close()
	return err
}

// SetDirection TODO
func (m *Motor) SetDirection(forward bool) error {
	state := rpio.High

	if !forward {
		state = rpio.Low
	}

	//err := m.DirectionPin.Write(state)
	//return err
	_ = state
	return nil
}

// SetSpeed TODO
func (m *Motor) SetSpeed(percentage uint) error {
	return nil
}
