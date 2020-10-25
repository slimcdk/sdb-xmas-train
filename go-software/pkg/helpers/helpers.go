package helpers

import (
	"os"
)

func Getenv(key, fallback string) string {
    if value, ok := os.LookupEnv(key); ok {
        return value
    }
    return fallback
}


func B2i(b bool) int8 {
	if b {
		return 1
	}
	return 0
}