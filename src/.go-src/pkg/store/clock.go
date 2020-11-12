package store

import (
	"strings"
	"strconv"
)


// Clock TODO
type Clock struct {
	Hour, Minute, Second int
}

// Hour TODO
func (c *Clock) GetHour() int {
	return c.Hour
}

// SetHour TODO
func (c *Clock) SetHour(hour int) {
	c.Hour = hour
}

// Minute TODO
func (c *Clock) GetMinute() int {
	return c.Minute
}

// SetMinute TODO
func (c *Clock) SetMinute(minute int) {
	c.Hour = minute
}

// Second TODO
func (c *Clock) GetSecond() int {
	return c.Second
}

// SetSecond TODO
func (c *Clock) SetSecond(second int) {
	c.Hour = second
}

// SetClock TODO
func (c *Clock) SetClock(hour, minute, second int) {
	c.SetHour(hour)
	c.SetMinute(minute)
	c.SetSecond(second)
}

// Time TODO
func (c *Clock) Time() (int, int, int) {
	return c.Hour, c.Minute, c.Second
}

// IsBetween TODO
func (c *Clock) IsBetween(start, end Clock) bool {

	// Times are converted to seconds past midnight
	var (
		s int = (start.Hour * 3600) + (start.Minute * 60) + start.Second
		e int = (end.Hour * 3600) + (end.Minute * 60) + end.Second
		t int = (c.Hour * 3600) + (c.Minute * 60) + c.Second
	)

	//fmt.Printf("%d %d\n", t-s, e-s)

	return 0 <= (t-s) && (t-s) < (e-s)
}


func ParseClockString(value string ) (Clock, error) {

	values := strings.Split(value, ":")

	h, err := strconv.Atoi(values[0])
	if err != nil { return Clock{Hour:0, Minute:0, Second:0}, err }

	m, err := strconv.Atoi(values[1])
	if err != nil { return Clock{Hour:0, Minute:0, Second:0}, err }

	s, err := strconv.Atoi(values[2])
	if err != nil { return Clock{Hour:0, Minute:0, Second:0}, err }

	clock := Clock{Hour: h, Minute: m, Second: s }

	return clock, nil
}