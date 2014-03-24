package main

//Connect to http://10.0.2.2:8080 on android (http://developer.android.com/tools/devices/emulator.html#networkaddresses)

import (
	"fmt"
	"io/ioutil"
	"net/http"
	"os"
	"strings"
)

var (
	HOST     = "https://api.wrapp.com"
	OVERRIDE = "override/"
	OUTPUT   = "output/"
)

func main() {
	os.Mkdir(OVERRIDE, 0777)
	os.Mkdir(OUTPUT, 0777)
	fmt.Println("Listening...")
	http.HandleFunc("/", defaultHandler)
	err := http.ListenAndServe(":8080", nil)
	if err != nil {
		panic(err)
	}
}

func defaultHandler(w http.ResponseWriter, r *http.Request) {
	file := strings.Split(strings.Replace(strings.Replace(r.URL.String(), "/", ".", -1), ".", "", 1), "?")[0] + ".txt" //Changes '/' to '.', remove the first '.', and remove everything after and including '?'
	if fileExists(OVERRIDE + file) {
		fmt.Println("overriding: " + r.URL.String())
		writeFileToOut(w, OVERRIDE+file)
	} else {
		fmt.Println("requesting: " + r.URL.String())
		var resp *http.Response
		var err error
		if r.Method == "GET" {
			resp, _ = http.Get(HOST + r.URL.String())
		} else {
			resp, err = http.Post(HOST+r.URL.String(), "application/json", r.Body)
		}

		if err != nil {
			fmt.Printf("Connection error: %s\n", err)
			fmt.Fprintf(w, "Connection error!")
		} else {
			defer resp.Body.Close()
			body, _ := ioutil.ReadAll(resp.Body)
			ioutil.WriteFile(OUTPUT+file, body, 0777)
			fmt.Fprintf(w, string(body))
		}
	}
}

func writeFileToOut(w http.ResponseWriter, url string) {
	contents, _ := ioutil.ReadFile(url)
	fmt.Fprintf(w, string(contents))
}

func fileExists(path string) bool {
	_, err := os.Stat(path)
	if err == nil {
		return true
	}
	return false
}
