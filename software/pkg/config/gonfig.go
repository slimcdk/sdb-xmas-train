package config

import (
	"fmt"

	"github.com/tkanos/gonfig"
)

type Configuration struct {
	SHOP_OPEN_CLOCK  string
	SHOP_CLOSE_CLOCK string
	TRACKS_TO_PLAY   string
	TRAIN_MAX_SPEED  string
}

func GetConfig(params ...string) Configuration {
	configuration := Configuration{}
	env := "dev"
	if len(params) > 0 {
		env = params[0]
	}
	fileName := fmt.Sprintf("./%s_config.json", env)
	gonfig.GetConf(fileName, &configuration)
	return configuration
}
