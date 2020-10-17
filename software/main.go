package main

import (
	"log"
	"os"
	"time"

	"github.com/slimcdk/sdb-xmas-train/pkg/musician"
)

var (
	shop = Shop{
		openClock:  Clock{hour: 1, minute: 1, second: 0},
		closeClock: Clock{hour: 1, minute: 2, second: 0},
	}

	// Motor control related
	/*
		motor = conductor.Motor{
			ControlPin:    rpio.Pin(12).Output().Pwm().PullDown(),
			DirectionPin:  rpio.Pin(11),
			MotorRelayPin: rpio.Pin(13).Output().PullDown(),
		}
	*/

	// Music related
	music                  = musician.Vault{Directory: os.Getenv("MUSIC_PATH"), Formats: []string{".go", ".mod"}}
	tracksToPlay           = 2
	currentPlayList        = []string{}
	currentPlayListDuation = 0
	newPlaylist            = true

	// Loggin related
	logChanges = true
	shopStates = []string{"closed", "open"}
)

func main() {
	log.Println("Choo choo! Christmas train is booting")

	/*err := motor.Initialize()
	if err != nil {
		panic(err)
	}
	*/

	// Run main logic
	var err error = nil
	for err == nil {
		err = loop()
	}

	/*
		if err := motor.Close(); err != nil {
			panic(err)
		}
	*/
}

func loop() error {
	currentTime := time.Now()
	shopIsOpen, _ := shop.IsOpenIfClock(currentTime.Clock())

	if shopIsOpen {
		// Set lights

		// Populate new playlist

		// Compute run duration for playlist

	} else {

		// Empty playlist

		// Extend train run duration to match active song

	}

	// Start player with next song in queue / playlist

	// Set flags to initiate a new run

	if logChanges {
		logChanges = false
		go func() {
			log.Printf("\t%s\tshop is %s\t", currentTime.Format("15:04:05"), shopStates[b2i(shopIsOpen)])
			time.Sleep(time.Second)
			logChanges = true
		}()
	}
	return nil
}
