package config

import (
	"fmt"
	"log"

	"github.com/jinzhu/configor"
)

type Configuration struct {
	MUSIC_DIR string `env:"MUSIC_DIR"`
	CONFIG_DIR string `env:"CONFIG_DIR"`
	SHOP_OPEN_CLOCK  string `env:"OPEN_CLOCK"`
	SHOP_CLOSE_CLOCK string`env:"CLOSE_CLOCK"`
	TRACKS_TO_PLAY   string `env:"TRACKS_TO_PLAY"`
	TRAIN_MAX_SPEED  string `env:"TRAIN_MAX_SPEED"`
}



var (
	configFile = "parameters"
	Config = struct {
		APPName string `default:"app name"`
	
		DB struct {
			Name     string
			User     string `default:"root"`
			Password string `required:"true" env:"DBPassword"`
			Port     uint   `default:"3306"`
		}
	
		Contacts []struct {
			Name  string
			Email string `required:"true"`
		}
	}{}
)


func GetConfig() Configuration {

	configuration := Configuration{}
	file := fmt.Sprintf("parameters.json", configFile)

	err := gonfig.GetConf(file, &configuration)
	if err != nil { 
		log.Fatal("No configuration file found")
	}

	return configuration
}

func main() {
	configor.Load(&Config, "config.yml")
	fmt.Printf("config: %#v", Config)
}