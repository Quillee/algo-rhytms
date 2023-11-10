package arraylist

import (
	"testing"

	dsa "github.com/quillee/algo-rhytms/go-kata/src/DSA"
)

func TestArrayList(t *testing.T) {
	list := NewArrayList[int](3)
	dsa.TestList(t, list)
}
