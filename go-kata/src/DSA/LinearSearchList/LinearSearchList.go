package linearsearchlist

func LinearSearch(haystack []int, needle int) bool {
    for _, hay := range haystack {
        if hay == needle {
            return true
        }
    }
    return false
}
