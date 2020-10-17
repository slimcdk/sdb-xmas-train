package musician

import (
	"strings"
	"path/filepath"
)


// Vault TODO
type Vault struct {
	Directory string
	Formats []string
}

// GetVaultDirectory returns the absolute directory of the music vault
func (v *Vault) GetVaultDirectory() (string, error) {
	path, err := filepath.Abs(v.Directory)
	if err != nil {
		return "", err
	}
	return path, nil
}

// GetFullPlaylist returns the path of every track in the dir
func (v *Vault) GetFullPlaylist() ([]string, error) {
	path, err := v.GetVaultDirectory()
	if err != nil {
		return nil, err
	}

	path += "/*"
	if len(v.Formats) > 0 {
		path += "[" + strings.Join(v.Formats, ",")  + "]"
	}
	
	tracks, err := filepath.Glob(path)
	if err != nil {
		return nil, err
	}

	return tracks, nil
}


// GetTracks returns n number of tracks. Tracks are duplicated if n is greater than the absolute number of tracks
func (v* Vault) GetTracks(n int) ([]string, error) {

	var tracks []string
	playlist, err := v.GetFullPlaylist()
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