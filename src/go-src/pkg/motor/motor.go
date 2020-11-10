package motor

import (
	"time"

	"github.com/slimcdk/sdb-xmas-train/pkg/gpio"
)

// Motor TODO
type Motor struct {
	ControlPin    gpio.PinConfig
	MotorRelayPin gpio.PinConfig
	//DirectionPin  gpio.PinConfig
}


func (m *Motor) SetSpeed(target uint8) error {
	//m.ControlPin.Duty
	time.Sleep(time.Second * 2)
	return nil
}