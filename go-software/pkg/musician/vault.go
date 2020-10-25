package musician

import (
	"path/filepath"
	"strings"
)

// GetVaultDirectory returns the absolute directory of the music vault
func (m *Musician) GetVaultDirectory() (string, error) {
	path, err := filepath.Abs(m.Directory)
	if err != nil {
		return "", err
	}
	return path, nil
}

// GetFullPlaylist returns the path of every track in the dir
func (m *Musician) GetFullPlaylist() ([]string, error) {
	path, err := m.GetVaultDirectory()

	if err != nil {
		return nil, err
	}

	path += "/*"
	if len(m.Formats) > 0 {
		path += "[" + strings.Join(m.Formats, ",") + "]"
	}

	tracks, err := filepath.Glob(path)
	if err != nil {
		return nil, err
	}

	return tracks, nil
}

// GetTracks returns n number of tracks. Tracks are duplicated if n is greater than the absolute number of tracks
func (m *Musician) GetTracks(n int) ([]string, error) {

	var tracks []string
	playlist, err := m.GetFullPlaylist()
	if err != nil {
		return playlist, err
	}

	if len(playlist) <= 0 {
		return playlist, nil
	}

	i := 0
	for i < n {
		tracks = append(tracks, playlist[i%len(playlist)])
		i++
	}

	return tracks[:n], nil
}

// NewPlaylistQueue TODO
func (m *Musician) NewPlaylistQueue(n int) ([]string, int, error) {
	playlist, err := m.GetTracks(n)
	if err != nil {
		return nil, -1, err
	}

	m.playlistQueue = playlist
	length := 0
	return playlist, length, nil
}
