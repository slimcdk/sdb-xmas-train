package lights

import (
	"github.com/slimcdk/sdb-xmas-train/pkg/gpio"
)


type SpotLight struct {
	Output gpio.PinConfig
}


func (sl* SpotLight) TurnOn() {
	sl.Output.High()
}

func (sl* SpotLight) TurnOff() {
	sl.Output.Low()
}

func (sl* SpotLight) Toggle() {
	sl.Output.Toggle()
}
