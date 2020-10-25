package main

import (
	"log"
	"os"

	"github.com/slimcdk/sdb-xmas-train/pkg/musician"
)

var (
	music = musician.Musician{Directory: os.Getenv("MUSIC_DIR"), Formats: []string{".mp3", ".wav"}}
)

func main() {
	log.Println("Starting processing of music library")
	log.Println(music.GetTracks(2))
}
