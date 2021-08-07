package main

import (
	"encoding/json"
	"fmt"
	"os"
	"strconv"
	"strings"
	"sync"
)

const (
	WORKERS	= 5
)

type JsonData struct {
	Data []struct {
		Level string `json:"level"`
	} `json:"data"`
}

type Pending struct {
	main	uint
	il	uint
	err	error
}

func get_games(argc int, argv []string) [2]Game {
	var games [2]Game
	var wg sync.WaitGroup

	wg.Add(argc)
	for i, abbreviation := range argv {
		go func(i int, abbreviation string) {
			var err error

			games[i], err = GameData(abbreviation)
			if err != nil {
				ErrorAndDie(err)
			}

			wg.Done()
		}(i, abbreviation)
	}
	wg.Wait()

	return games
}

func worker(id string, jobs <- chan int, counts chan <- Pending) {
	for offset := range jobs {
		json_bytes := Request("/runs?game=" + id + "&status=new&max=200&offset=" +
				strconv.Itoa(offset))

		var data JsonData
		err := json.Unmarshal(json_bytes, &data)
		if err != nil {
			ErrorAndDie(err)
		}

		var p Pending
		for _, run := range data.Data {
			if run.Level == "" {
				p.main++
			} else {
				p.il++
			}
		}

		counts <- p
	}
}

func calculate_pending(id string, c chan <- Pending) {
	jobs := make(chan int)
	counts := make(chan Pending)

	/* Spawn 5 workers */
	for i := 0; i < WORKERS; i++ {
		go worker(id, jobs, counts)
	}

	var pending Pending
	offset := 0
	done := false
	for !done {
		for i := 0; i < WORKERS; i++ {
			jobs <- offset
			offset += 200
		}

		for i := 0; i < WORKERS; i++ {
			p := <- counts

			if p.il == 0 && p.main == 0 {
				done = true
			} else {
				pending.il += p.il
				pending.main += p.main
			}
		}
	}

	c <- pending
}

func get_pending(argc int, games [2]Game) (uint, uint) {
	c := make(chan Pending)
	for i := 0; i < argc; i++ {
		go calculate_pending(games[i].id, c)
	}

	var il uint = 0
	var main uint = 0
	for i := 0; i < argc; i++ {
		p := <- c
		if p.err != nil {
			ErrorAndDie(p.err)
		}
		il += p.il
		main += p.main
	}

	return main, il
}

func main() {
	argc := len(os.Args) - 1
	if argc == 0 || argc > 2 {
		Usage("runqueue", "[GAME] [GAME (Optional)]", "mkw mkwextracategories")
	}
	argv := os.Args[1:]

	if argc == 2 && strings.EqualFold(argv[0], argv[1]) {
		ErrorAndDie("Same game given twice")
	}

	games := get_games(argc, argv)
	main, il := get_pending(argc, games)

	if argc == 1 {
		fmt.Printf("Runs Awaiting Verification: `%s`\n", games[0].name)
	} else {
		fmt.Printf("Runs Awaiting Verification: `%s` and `%s`\n", games[0].name,
			   games[1].name)
	}
	fmt.Printf("Fullgame: %d\nIndividual Level: %d\nTotal: %d\n", main, il, main + il)
}
