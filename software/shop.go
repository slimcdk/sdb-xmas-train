package main

import (
	"time"
)

// Shop TODO
type Shop struct {
	openClock  Clock
	closeClock Clock
	isOpen     bool
}

// SetOpenClock TODO
func (s *Shop) SetOpenClock(c Clock) {
	s.openClock = c
}

// SetCloseClock TODO
func (s *Shop) SetCloseClock(c Clock) {
	s.closeClock = c
}

// OpenClock TODO
func (s *Shop) OpenClock() (int, int, int) {
	return s.openClock.Time()
}

// CloseClock TODO
func (s *Shop) CloseClock() (int, int, int) {
	return s.closeClock.Time()
}

// IsOpen TODO
func (s *Shop) IsOpen() bool {
	isOpen, _ := s.IsOpenIfClock(time.Now().Clock())
	s.isOpen = isOpen
	return isOpen
}

// IsOpenIfClock TODO
func (s *Shop) IsOpenIfClock(hour, minute, second int) (bool, error) {

	test := Clock{hour: hour, minute: minute, second: second}
	isOpen, err := test.IsBetween(s.openClock, s.closeClock)

	if err != nil {
		return false, err
	}
	return isOpen, nil
}
