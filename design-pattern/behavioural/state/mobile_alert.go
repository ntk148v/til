package main

import "fmt"

type MobileAlertState interface {
	alert()
}

type AlertStateContext struct {
	currentState MobileAlertState
}

func NewAlertStateContext() *AlertStateContext {
	return &AlertStateContext{currentState: &Vibration{}}
}

func (ctx *AlertStateContext) SetState(state MobileAlertState) {
	ctx.currentState = state
}

func (ctx *AlertStateContext) Alert() {
	ctx.currentState.alert()
}

type Vibration struct{}

func (v *Vibration) alert() {
	fmt.Println("Vibrating...")
}

type Silence struct{}

func (s *Silence) alert() {
	fmt.Println("Silent...")
}

func main() {
	stateContext := NewAlertStateContext()
	stateContext.Alert()
	stateContext.Alert()
	stateContext.Alert()
	stateContext.SetState(&Silence{})
	stateContext.Alert()
	stateContext.Alert()
	stateContext.Alert()
}
