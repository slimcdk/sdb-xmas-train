package musician

import (
	"time"

	"github.com/jleight/omxplayer"
)


// PlayTrack TODO
func (m *Musician) PlayTrack(trackPath string) error {

	player, err := omxplayer.New(trackPath)
	if err != nil {
		return err
	}
	m.Player = player
	return nil
}

// StopPlayer TODO
func (m *Musician) StopPlayer() error {
	err := m.Player.Stop()
	if err != nil {
		return err
	}
	return nil
}

// CanGoNext TODO
func (m *Musician) CanGoNext() (bool, error) {
	can, err := m.Player.CanGoNext()
	if err != nil {
		return can, err
	}
	return can, nil
}


func (m *Musician) SetUser () {
	omxplayer.SetUser(user, home)
}


func (m *Musician) PlayUpbeat() error {
	time.Sleep(time.Second * 5)
	return nil
}

func (m *Musician) PlayTracks(numberOfTracks uint) error {
	time.Sleep(time.Second * 60)
	return nil
}