package main

import "fmt"

// Shape is the component
type Shape interface {
	Draw(drawer *Drawer) error
}

// Square and Circle are leaves
type Square struct {
	Location Point
	Size     float64
}

func (square *Square) Draw(drawer *Drawer) error {
	return drawer, DrawRect(Rect{
		Location: square.Location,
		Size: Size{
			Height: square.Side,
			Width:  square.Side,
		},
	})
}
