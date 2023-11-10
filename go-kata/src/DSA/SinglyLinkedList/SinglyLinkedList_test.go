package singlylinkedlist

import (
	"testing"

	dsa "github.com/quillee/algo-rhytms/go-kata/src/DSA"
)

func TestSinglyLinkedList(t *testing.T) {
	list := NewSinglyLinkedList[int]()
	dsa.TestList(t, list)
}
