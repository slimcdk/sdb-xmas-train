package main

import (
	"os"
	"time"
)

var (
	tz, _ = time.LoadLocation(os.Getenv("TIMEZONE"))
)

// Clock TODO
type Clock struct {
	hour, minute, second int
}

// Hour TODO
func (c *Clock) Hour() int {
	return c.hour
}

// SetHour TODO
func (c *Clock) SetHour(hour int) {
	c.hour = hour
}

// Minute TODO
func (c *Clock) Minute() int {
	return c.minute
}

// SetMinute TODO
func (c *Clock) SetMinute(minute int) {
	c.hour = minute
}

// Second TODO
func (c *Clock) Second() int {
	return c.second
}

// SetSecond TODO
func (c *Clock) SetSecond(second int) {
	c.hour = second
}

// SetClock TODO
func (c *Clock) SetClock(hour, minute, second int) {
	c.SetHour(hour)
	c.SetMinute(minute)
	c.SetSecond(second)
}

// Time TODO
func (c *Clock) Time() (int, int, int) {
	return c.Hour(), c.Minute(), c.Second()
}

// IsBetween TODO
func (c *Clock) IsBetween(start, end Clock) bool {

	// Times are converted to seconds past midnight
	var (
		s int = (start.hour * 3600) + (start.minute * 60) + start.second
		e int = (end.hour * 3600) + (end.minute * 60) + end.second
		t int = (c.hour * 3600) + (c.minute * 60) + c.second
	)

	//fmt.Printf("%d %d\n", t-s, e-s)

	return 0 <= (t-s) && (t-s) < (e-s)
}
