package musician

import "github.com/jleight/omxplayer"

// Musician TODO
type Musician struct {
	Player        *omxplayer.Player
	Directory     string
	Formats       []string
	playlistQueue []string
	isPlaying     bool
}

var (
	queueIndex = 0
)

/*
// Loop lifecycle of the musician
func (m *Musician) Loop() {

	// Process the playlist queue
	if len(m.playlistQueue) > 0 {
		nextTrack := m.playlistQueue[queueIndex]
		player, err := omxplayer.New()
		m.Player
	}

}
*/
