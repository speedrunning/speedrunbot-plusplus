package main

import (
	"encoding/json"
	"fmt"
	"net/http"
	"os"
)

type Runs struct {
	Data []Run
}

type Run struct {
	Place int
}

func main() {
	if len(os.Args) != 2 {
		Usage("top3", "[PLAYER NAME]", "whatevermarco")
	}

	uid, err := UserID(os.Args[1])
	if err != nil {
		ErrorAndDie(err)
	}

	res, err := http.Get(API + "/users/" + uid + "/personal-bests")
	if err != nil {
		ErrorAndDie(err)
	}
	defer res.Body.Close()

	var runs Runs
	json.NewDecoder(res.Body).Decode(&runs)

	count := 0
	for _, run := range runs.Data {
		if run.Place <= 3 {
			count++
		}
	}
	fmt.Printf("Podium Count: %s\nTop 3 Runs: %d\n", os.Args[1], count)
}
