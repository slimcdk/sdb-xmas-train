package main

import (
	"log"
	"os"

	"github.com/slimcdk/sdb-xmas-train/pkg/musician"
)

var (
	music = musician.Musician{Directory: os.Getenv("MUSIC_PATH"), Formats: []string{".mp3"}}
)

func main() {
	log.Println("Starting processing of music library")
	log.Println(music.Get)
}
