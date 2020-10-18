package main

import (
	"log"
	"os"
	"sync"
	"time"

	"github.com/jleight/omxplayer"
	"github.com/slimcdk/sdb-xmas-train/conductor/pkg/musician"
)

var (
	wg sync.WaitGroup

	shop = Shop{
		openClock:  Clock{hour: 8, minute: 0, second: 0},
		closeClock: Clock{hour: 20, minute: 0, second: 0},
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
	music                  = musician.Musician{Directory: os.Getenv("MUSIC_PATH"), Formats: []string{}}
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
	omxplayer.SetUser("root", "/root")

	// Run main logic
	wg.Add(1)
	go func() {
		var err error = nil
		for err == nil {
			err = loop()
		}
	}()
	wg.Wait()

	/*
		if err := motor.Close(); err != nil {
			panic(err)
		}
	*/
	os.Exit(0)
}

func loop() error {
	currentTime := time.Now()
	shopIsOpen := shop.IsOpenIfClock(currentTime.Clock())

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
			pl, _ := music.GetFullPlaylist()
			log.Printf("\t%s\tshop is %s\t%d songs in playlist", currentTime.Format("15:04:05"), shopStates[b2i(shopIsOpen)], len(pl))
			time.Sleep(time.Second)
			logChanges = true
		}()
	}
	return nil
}
