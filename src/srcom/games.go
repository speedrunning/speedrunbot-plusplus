package main

import (
	"encoding/json"
	"fmt"
	"os"
)

var count uint

type JsonData struct {
	Data []struct {
		Run struct {
#ifdef CATEGORIES
			ID string `json:"category"`
#else
			ID string `json:"game"`
#endif
		} `json:"run"`
	} `json:"data"`
}

/* https://www.golangprograms.com/golang-program-to-implement-binary-tree.html */
type BinaryNode struct {
	left	*BinaryNode
	right	*BinaryNode
	data	string
}

type BinaryTree struct {
	root	*BinaryNode
}

func (t *BinaryTree) insert(data string) *BinaryTree {
	if t.root == nil {
		t.root = &BinaryNode{data: data, left: nil, right: nil}
		count++
	} else {
		t.root.insert(data)
	}
	return t
}

func (n *BinaryNode) insert(data string) {
	if data < n.data {
		if n.left == nil {
			n.left = &BinaryNode{data: data, left: nil, right: nil}
			count++
		} else {
			n.left.insert(data)
		}
	} else if data > n.data {
		if n.right == nil {
			n.right = &BinaryNode{data: data, left: nil, right: nil}
			count++
		} else {
			n.right.insert(data)
		}
	}
}

func main() {
	if len(os.Args) != 2 {
#ifdef CATEGORIES
		Usage("categories", "[PLAYER NAME]", "StarBoi")
#else
		Usage("games", "[PLAYER NAME]", "Merl_")
#endif
	}

	uid, err := UserID(os.Args[1])
	if err != nil {
		ErrorAndDie(err)
	}

	res := Request("/users/" + uid + "/personal-bests")
	var runs JsonData
	json.Unmarshal(res, &runs)

	tree := &BinaryTree{}
	for _, run := range runs.Data {
		tree.insert(run.Run.ID)
	}
#ifdef CATEGORIES
	fmt.Printf("Categories Played: `%s`\n%d\n", os.Args[1], count)
#else
	fmt.Printf("Games Played: `%s`\n%d\n", os.Args[1], count)
#endif
}
