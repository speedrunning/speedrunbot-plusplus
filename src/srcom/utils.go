package main

import (
	"errors"
	"fmt"
	"io/ioutil"
	"net/http"
	"os"
	"time"
)

const (
	API		= "https://www.speedrun.com/api/v1"
	EXIT_FAILURE	= 1
	RATE_LIMIT	= 420
	ID_START	= 16
	ID_END		= 24
	NAME_START	= 52
)

type Game struct {
	name	string
	id	string
}

func Usage(cmd string, usage string, example string) {
	fmt.Fprintf(os.Stderr, "Usage: `+%s %s`\nExample: `+%s %s`\n", cmd, usage, cmd, example)
	os.Exit(EXIT_FAILURE)
}

func ErrorAndDie(err interface{}) {
	fmt.Fprintf(os.Stderr, "Error: %v\n", err)
	os.Exit(EXIT_FAILURE)
}

func Request(endpoint string) []byte {
	var resp *http.Response
	var err error
	for {
		resp, err = http.Get(API + endpoint)
		if err != nil {
			ErrorAndDie(err)
		}
		if resp.StatusCode != RATE_LIMIT {
			break
		}
		time.Sleep(2 * time.Second)
	}

	data, _ := ioutil.ReadAll(resp.Body)
	return data
}


func UserID(name string) (string, error) {
	id := string(Request("/users?lookup=" + name)[ID_START:ID_END])

	if id == `nation":` {
		return "", errors.New("User with name '" + name + "' not found.")
	}

	return id, nil
}

func GameData(abbreviation string) (Game, error) {
	json := string(Request("/games?abbreviation=" + abbreviation))
	id := json[ID_START:ID_END]

	if id == `nation":` {
		return Game{"", ""}, errors.New("Game with abbreviation '" + abbreviation +
					     "' not found.")
	}

	var i uint
	for i = NAME_START; json[i] != '"'; i++ {}
	name := json[NAME_START:i]

	return Game{name, id}, nil
}
