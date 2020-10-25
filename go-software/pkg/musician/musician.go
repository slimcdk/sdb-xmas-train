package musician

import (
	"github.com/jleight/omxplayer"
	h "github.com/slimcdk/sdb-xmas-train/pkg/helpers"

)

// Musician TODO
type Musician struct {
	Player        *omxplayer.Player
	Directory     string
	Formats       []string
	playlistQueue []string
	isPlaying     bool
}

var (
	user = h.Getenv("USER", "root")
	home = h.Getenv("HOME", "/root")

	queueIndex = 0
)