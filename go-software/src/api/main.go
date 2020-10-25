package main

import (
    "log"
    "fmt"
    "net/http"

    h "github.com/slimcdk/sdb-xmas-train/pkg/helpers"
)


var (
    appPort = fmt.Sprintf(":%s", h.Getenv("APP_PORT", "3000"))
)


func main() {
    http.HandleFunc("/", homePage)
    log.Fatal(http.ListenAndServe(appPort, nil))
}

