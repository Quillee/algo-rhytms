package generate

import (
	"fmt"
    "github.com/quillee/algo-rhytms/go-kata/internal/day"
    "github.com/quillee/algo-rhytms/go-kata/internal/dsa"
)

func Generate(DSAs []string) error {
	nextDay, err := day.GetNext()
	if err != nil {
		return fmt.Errorf("get next day: %w", err)
	}
	nextDayDirPath := day.GetDayDirPath(nextDay)

	for _, d := range DSAs {
		if err := dsa.Copy(d, nextDayDirPath); err != nil {
			return err
		}
	}

	return nil
}
