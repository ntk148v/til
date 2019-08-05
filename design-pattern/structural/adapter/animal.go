package main

type Animal interface {
	Move()
}

// Cat is a concrete animal since it implements the method Move
type Cat struct{}

func (c *Cat) Move() {}

// and somewhere in the code we need to use the crocodile type which is often not our code and this Crocodile type does not implement the Animal interface
// but we need to use a crocodile as an animal

type Crocodile struct{}

func (c *Crocodile) Slither() {}

// we create an CrocodileAdapter struct that dapts an embeded crocodile so that it can be usedd as an Animal

type CrocodileAdapter struct {
	*Crocodile
}

func NewCrocodile() *CrocodileAdapter {
	return &CrocodileAdapter{new(Crocodile)}
}

func (this *CrocodileAdapter) Move() {
	this.Slither()
}

func main() {
	var animals []Animal
	animals = append(animals, new(Cat))
	animals = append(animals, NewCrocodile())

	for _, entity := range animals {
		entity.Move()
	}
}
