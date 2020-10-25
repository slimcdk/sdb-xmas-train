package store


import (
	"time"
)


// Shop TODO
type Shop struct {
	OpenClock, CloseClock Clock
	isOpen                bool
}

// SetOpenClock TODO
func (s *Shop) SetOpenClock(c Clock) {
	s.OpenClock = c
}

// SetCloseClock TODO
func (s *Shop) SetCloseClock(c Clock) {
	s.CloseClock = c
}

// OpenClock TODO
func (s *Shop) GetOpenClock() (int, int, int) {
	return s.OpenClock.Time()
}

// CloseClock TODO
func (s *Shop) GetCloseClock() (int, int, int) {
	return s.CloseClock.Time()
}

// IsOpen TODO
func (s *Shop) IsOpen() bool {
	isOpen := s.IsOpenIfClock(time.Now().Clock())
	s.isOpen = isOpen
	return isOpen
}

// IsOpenIfClock TODO
func (s *Shop) IsOpenIfClock(hour, minute, second int) bool {

	test := Clock{Hour: hour, Minute: minute, Second: second}
	isOpen := test.IsBetween(s.OpenClock, s.CloseClock)
	return isOpen
}
