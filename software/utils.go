package main

import "time"

func timeInRange(min time.Time, test time.Time, max time.Time) (bool, error) {
	s := (min.Hour() * 3600) + (min.Minute() * 60) + min.Second()
	t := (test.Hour() * 3600) + (test.Minute() * 60) + test.Second()
	e := (max.Hour() * 3600) + (max.Minute() * 60) + max.Second()
	inRange := s <= t && t < e
	return inRange, nil
}

func b2i(b bool) int8 {
	if b {
		return 1
	}
	return 0
}
