package doublylinkedlist

import (
	"testing"

	dsa "github.com/quillee/algo-rhytms/go-kata/src/DSA"
)

func TestDoublyLinkedList(t *testing.T) {
	list := NewDoublyLinkedList[int]()
	dsa.TestList(t, list)
}
