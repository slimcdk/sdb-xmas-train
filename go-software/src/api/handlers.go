package main


import (
	"fmt"
	"net/http"
	//c "github.com/slimcdk/sdb-xmas-train/pkg/config"
)


func homePage (w http.ResponseWriter, r *http.Request) {
    fmt.Fprintf(w, "Welcome to the HomePage!")
}

