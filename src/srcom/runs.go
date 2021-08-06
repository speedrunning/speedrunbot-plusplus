package main

import (
	"encoding/json"
	"fmt"
	"os"
	"strconv"
)

type JsonData struct {
	Data []struct {
		Level string `json:"level"`
	} `json:"data"`
}

type Runs struct {
	main	uint
	il	uint
	err	error
}

func count_runs(uri string, c chan <- Runs) {
	json_bytes := Request(uri)

	var data JsonData
	err := json.Unmarshal(json_bytes, &data)
	if err != nil {
		ErrorAndDie(err)
	}

	var r Runs
	for _, run := range data.Data {
		if run.Level == "" {
			r.main++
		} else {
			r.il++
		}
	}

	c <- r
}

func get_counts(base string) (uint, uint) {
	c := make(chan Runs)
	offset := 0
	var main uint = 0
	var il uint = 0

	for {
		old_total := main + il

		for i := 0; i < 2; i++ {
			go count_runs(base + strconv.Itoa(offset), c)
			offset += 200
		}

		for i := 0; i < 2; i++ {
			r := <- c
			if r.err != nil {
				ErrorAndDie(r.err)
			}
			main += r.main
			il += r.il
		}

		if main + il - old_total < 400 {
			break
		}
	}

	return main, il
}

func main() {
	argc := len(os.Args)
	if argc == 1 || argc > 3 {
		Usage("runs", "[PLAYER NAME] [GAME (Optional)]", "Oreo321 kirbymeme");
	}

	uid, err := UserID(os.Args[1])
	if err != nil {
		ErrorAndDie(err)
	}

	if argc == 3 {
		game, err := GameData(os.Args[2])
		if err != nil {
			ErrorAndDie(err)
		}
		uri_base := "/runs?user=" + uid + "&game=" + game.id + "&max=200&offset="
		main, il := get_counts(uri_base)
		fmt.Printf("Run Count: %s - %s\nFullgame: %d\nIndividual Level: %d\nTotal: %d\n",
			os.Args[1], game.name, main, il, main + il)
	} else {
		uri_base := "/runs?user=" + uid + "&max=200&offset="
		main, il := get_counts(uri_base)
		fmt.Printf("Run Count: %s\nFullgame: %d\nIndividual Level: %d\nTotal: %d\n",
			os.Args[1], main, il, main + il)
	}
}
