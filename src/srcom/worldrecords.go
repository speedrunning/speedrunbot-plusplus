package main

import (
	"encoding/json"
	"fmt"
	"os"
)

type JsonData struct {
	Data []struct {
		Run struct {
			Level string `json:"level"`
		} `json:"run"`
	} `json:"data"`
}

func get_counts(json_bytes []byte) (uint, uint) {
	var data JsonData
	err := json.Unmarshal(json_bytes, &data)
	if err != nil {
		ErrorAndDie(err)
	}

	var main uint
	var il uint
	for _, run := range data.Data {
		if run.Run.Level == "" {
			main++
		} else {
			il++
		}
	}

	return main, il
}

func main() {
	argc := len(os.Args)
	if argc == 1 || argc > 3 {
		Usage("worldrecords", "[PLAYER] [GAME (Optional)]", "ElTreago mcbe")
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
		json_bytes := Request("/users/" + uid + "/personal-bests?top=1&game=" + game.id)
		main, il := get_counts(json_bytes)
		fmt.Printf("World Record Count: %s - %s\n" +
			   "Full Game: %d\n" +
			   "Individual Level: %d\n" +
			   "Total: %d\n", os.Args[1], game.name, main, il, main + il)
	} else {
		json_bytes := Request("/users/" + uid + "/personal-bests?top=1")
		main, il := get_counts(json_bytes)
		fmt.Printf("World Record Count: %s\n" +
			   "Full Game: %d\n" +
			   "Individual Level: %d\n" +
			   "Total: %d\n", os.Args[1], main, il, main + il)
	}
}
