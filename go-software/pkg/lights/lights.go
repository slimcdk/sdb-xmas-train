package lights

import (
	_ "github.com/slimcdk/sdb-xmas-train/pkg/gpio"
)


// LightStruct TODO
type LightShow struct {
	SpotLights    []SpotLight
}



func (ls *LightShow) TurnOn () {
	for _, spot := range ls.SpotLights {
		spot.TurnOn()
	}
}

func (ls *LightShow) TurnOff () {
	for _, spot := range ls.SpotLights {
		spot.TurnOff()
	}
}


func (ls *LightShow) Toggle () {
	for _, spot := range ls.SpotLights {
		spot.Toggle()
	}
}

func (ls *LightShow) TurnOnSpots () {
	for _, spot := range ls.SpotLights {
		spot.TurnOn()
	}
}

func (ls *LightShow) TurnOffSpots () {
	for _, spot := range ls.SpotLights {
		spot.TurnOff()
	}
}