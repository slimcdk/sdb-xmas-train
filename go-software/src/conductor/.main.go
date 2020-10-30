package main

import (
	"log"
	"os"
	"sync"
	"time"

	h "github.com/slimcdk/sdb-xmas-train/pkg/helpers"
	"github.com/slimcdk/sdb-xmas-train/pkg/store"
	gpio "github.com/slimcdk/sdb-xmas-train/pkg/gpio"
	"github.com/slimcdk/sdb-xmas-train/pkg/musician"
	"github.com/slimcdk/sdb-xmas-train/pkg/lights"
	trainMotor "github.com/slimcdk/sdb-xmas-train/pkg/motor"

	rpio "github.com/stianeikeland/go-rpio"
)


var (
	wg sync.WaitGroup
	tz, _ = time.LoadLocation(os.Getenv("TIMEZONE"))

	// Shop
	
	openClock, _ = store.ParseClockString(h.Getenv("OPEN_HOUR", "08:00:00"))
	closeClock, _ = store.ParseClockString(h.Getenv("CLOSE_HOUR", "20:00:00"))

	shop = store.Shop{
		OpenClock:  openClock, //store.Clock{Hour: 8, Minute: 0, Second: 0},
		CloseClock: closeClock, //store.Clock{Hour: 20, Minute: 0, Second: 0},
	}

	// Lights
	lightShow = lights.LightShow {
		SpotLights: []lights.SpotLight{
			{Output: gpio.PinConfig{Pin: 11, Inverted: false}},
		},
	}

	// Motor
	motor = trainMotor.Motor{
		ControlPin:    gpio.PinConfig{Pin: 12, Inverted: false},
		MotorRelayPin: gpio.PinConfig{Pin: 13, Inverted: false},
	}

	// Music
	music        = musician.Musician{Directory: os.Getenv("MUSIC_DIR"), Formats: []string{".mp3", ".wav"}}
	tracksToPlay uint = 2

	// Main logic variables
	lightsEnabled = false
	isRunning = false
	nextRun = true

	// Logging related
	logChanges = true
	shopStates = []string{"closed", "open"}
)

func rpioTest () {
	// Initialize hardware
	if err := rpio.Open(); err != nil {
		fmt.Println(err)
		return
	}

	defer rpio.Close()
	
	pin := rpio.Pin(10)
	pin.Output()

	for i := 0; i < 10; i++ {
		time.Sleep(time.Second)
		pin.Toggle()
	}

	wg.Done()
	return
}




func main() {
	log.Println("Choo choo! Christmas train is booting")
	log.Printf("Open and close hours set to %d and %d", openClock, closeClock)

	wg.Add(1)
	go rpioTest()
	wg.Wait();

	os.Exit(0)

	// Run main logic
	wg.Add(1)
	go func() {
		var err error = nil
		for err == nil {
			err = loop()
		}
		wg.Done()
	}()

	wg.Wait()
	
	log.Println("Choo choo! Christmas train is stopping")
	os.Exit(0)
}

func loop() error {
	currentTime := time.Now()
	shopIsOpen := shop.IsOpenIfClock(currentTime.Clock())

	if shopIsOpen {
		if !lightsEnabled {	
			lightsEnabled = true
			log.Println("Enabling lights")
			//lightShow.TurnOn()
		}

		if nextRun {
			nextRun = false
			log.Println("Starting a new goroutine")
			wg.Add(1)
			go func(){
				log.Println("Playing upbeat track")
				music.PlayUpbeat()

				log.Println("Starting motor")
				motor.SetSpeed(255)

				log.Printf("Playing %d tracks\n", tracksToPlay)
				music.PlayTracks(tracksToPlay)

				log.Println("Stopping motor")
				motor.SetSpeed(0)

				log.Println("Sleeping until next run")
				time.Sleep(time.Second * 60)

				nextRun = true
				log.Println("Flagging next run")
				log.Println("Goroutine ended")
				wg.Done()
			}()
		}

	} else {
		if !isRunning {
			if lightsEnabled {
				lightsEnabled = false
				log.Println("Disabling lights")
				//lightShow.TurnOff()
			}	
		}
	}

	if logChanges {
		logChanges = false
		wg.Add(1)
		go func() {
			log.Printf("shop is %s", shopStates[h.B2i(shopIsOpen)])
			time.Sleep(time.Second)
			logChanges = true
			wg.Done()
		}()
	}
	return nil
}
