package main

import (
	"fmt"
	"os"
	"strings"
)

func count(endpoint, uid string, c chan uint) {
	data := string(Request(endpoint + uid))
	index := strings.LastIndex(data, "\"size\":")

	var count uint
	fmt.Sscanf(data[index:], "\"size\":%d,\"links\"", &count)
	c <- count
}

func main() {
	if len(os.Args) != 2 {
		Usage("modcount", "[PLAYER NAME]", "AnInternetTroll")
	}

	uid, err := UserID(os.Args[1])
	if err != nil {
		ErrorAndDie(err)
	}

	gc := make(chan uint)
	sc := make(chan uint)

	/*
	 * At this scale this is probably overkill (and maybe a little slower), but oh well.
	 *
	 * TODO: Support offsets and such when someone actually hits that number (likely not for a
	 * VERY long time)
	 */
	go count("/games?&_bulk=yes&max=1000&moderator=", uid, gc)
	go count("/series?&max=200&moderator=", uid, sc)

	games := <- gc
	series := <- sc

	fmt.Printf("Games: %d\nSeries: %d\nTotal: %d\n", games, series, games + series)
}
