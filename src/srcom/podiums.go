package main

import (
	"encoding/json"
	"fmt"
	"os"
)

type JsonData struct {
	Data []struct {
		Place int `json:"place"`
	} `json:"data"`
}

func main() {
	if len(os.Args) != 2 {
		Usage("podiums", "[PLAYER NAME]", "whatevermarco")
	}

	uid, err := UserID(os.Args[1])
	if err != nil {
		ErrorAndDie(err)
	}

	res := Request("/users/" + uid + "/personal-bests")

	var runs JsonData
	json.Unmarshal(res, &runs)

	count := 0
	for _, run := range runs.Data {
		if run.Place <= 3 {
			count++
		}
	}
	fmt.Printf("Podium Count: `%s`\nTop 3 Runs: %d\n", os.Args[1], count)
}
