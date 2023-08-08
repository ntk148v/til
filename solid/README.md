# SOLID principles

Source:

- <https://hackernoon.com/go-design-patterns-an-introduction-to-solid>
- <https://dave.cheney.net/2016/08/20/solid-go-design>

The SOLID principles are five principles of **object-oriented** class design. They are a set of rules and best practices to follow while designing a class structure.

Let's dive into the world of SOLID design and learn how these principles can help us create better software, and how they can be applied in Golang.

## 1. Single Responsibility Principle (SRP)

```plain
A class should have one, and only one, reason to change.

– Robert C Martin -
```

- This principle states that **a class (or struct in Golang) should only have one responsibility and therefore it should only have one reason to change**.
- BY adhering to this principle, code becomes more modular, easier to understand, and less susceptible to bugs as changes are made.
- Bad example: one struct handles both paymenst and invoices.

```go
type PaymentInvoiceService struct{}

func (pis PaymentInvoiceService) ProcessPayment(amount float64) {
    // Process the payment
}

func (pis PaymentInvoiceService) CreateInvoice(amount float64) {
    // Create the invoice
}
```

- Good example:

```go
type PaymentService struct{}

func (ps PaymentService) ProcessPayment(amount float64) {
    // Process the payment
}

type InvoiceService struct{}

func (is InvoiceService) CreateInvoice(amount float64) {
    // Create the invoice
}
```

## 2. Open/Closed Principle (OCP)

```plain
Software entities should be open for extension, but closed for modification.

– Bertrand Meyer, Object-Oriented Software Construction -
```

- The open-closed principle states that classes, modules, and functions should be **open for extension, but closed for modification**. It means you should be able to extend the functionality of them by adding more code without modifying the existing code.
- For example:

```go
package main

import "fmt"

type PaymentMethod interface {
	Pay()
}

type Payment struct{}

func (p Payment) Process(pm PaymentMethod) {
	pm.Pay()
}

type CreditCard struct {
	amount float64
}

func (cc CreditCard) Pay() {
	fmt.Printf("Paid %.2f using CreditCard", cc.amount)
}

// Using PaymentMethod, I don't have to edit Payment behavior when adding new payment methods.
type PayPal struct {
    amount float64
}

func (pp PayPal) Pay() {
    fmt.Printf("Paid %.2f using PayPal", pp.amount)
}

func main() {
	p := Payment{}
	cc := CreditCard{12.23}
	p.Process(cc)

    pp := PayPal{22.33}
    p.Process(pp)
}
```

## 3. Liskov Subtitution Principle (LSP)

- The Liskov Substitution principle is one of the most important principles to adhere to in object-oriented programming (OOP). It states that child classes or subclasses must be substitutable for their parent classes or super classes. Narrowing it down, we have **if class A is a subclass of class B, we should be able to replace B with A without disrupting the behavior of our program**.
- For example:

```go
type Animal struct {
    Name string
}

func (a Animal) MakeSound() {
    fmt.Println("Animal sound")
}

// Golang doesn't have subclass term
// but we can leverage it using embedded tyep field.
type Bird struct {
    Animal
}

func (b Bird) MakeSound() {
    fmt.Println("Chirp chirp")
}
```

- This principle states that objects of a superclass should be replaceable with objects of a subclass without affecting the correctness of the program. This helps to ensure that the relationships between classes are well-defined and maintainable.

```go
type AnimalBehavior interface {
  MakeSound()
}

// MakeSound represent a program that works with animals and is expected
// to work with base class (Animal) or any subclass (Bird in this case)
func MakeSound(ab AnimalBehavior) {
    ab.MakeSound()
}

a := Animal{}
b := Bird{}
MakeSound(a)
MakeSound(b)
```

- This demonstrates inheritance in Go, as well as the Liskov Substitution Principle, as objects of a subtype `Bird` can be used wherever objects of the base type `Animal` are expected, without affecting the correctness of the program.

## Interface Segregation Principle (ISP)

```plain
Clients should not be forced to depend on methods they do not use.

– Robert C. Martin -
```

- According to this principle, **a client should never be forced to implement an interface that it doesn’t use**, or a client shouldn’t be forced to depend on methods it does not use.
- In Go, the application of the interface segregation principle can refer to a process of isolating the behaviour required for a function to do its job. As a concrete example, say I’ve been given a task to write a function that persists a Document structure to disk.

```go
// Save writes the contents of doc to the file f.
func Save(f *os.File, doc *Document) error
```

- The signature of `Save` precludes the option to write the data to a network location. Assuming that network storage is likely to become requirement later, the signature of this function would have to change, impacting all its callers.
- Because `Save` operates directly with files on disk, it is unpleasant to test. To verify its operation, the test would have to read the contents of the file after being written. Additionally the test would have to ensure that f was written to a temporary location and always removed afterwards.
- `*os.File` also defines a lot of methods which are not relevant of `Save`, like reading directories and checking to see if a path is symlink. It would be useful if the signature of `Save` function could describe only the parts of `*os.File` that were relevant.
- Apply ISP to redefine the `Save` to take an interface that describes more general file-shaped things.

```go
// Save writes the contents of doc to the supplied ReadWriterCloser.
func Save(rwc io.ReadWriteCloser, doc *Document) error
```

- We no longer have the option to call those unrelated methods on `*os.File` as it is hidden behind the `io.ReadWriteCloser` interface. But we can take the ISP a bit further.
- Firstly, it is unlikely that if `Save` follows the Single Responsibility Principle, it will read the file it just wrote to verify its contents-that should be responsibility of another piece of code. So we can narrow the specification for the interface we pass to `Save` to just writing and closing.

```go
// Save writes the contents of doc to the supplied WriteCloser.
func Save(wc io.WriteCloser, doc *Document) error
```

- Secondly, by providing Save with a mechanism to close its stream, which we inherited in a desire to make it look like a file shaped thing, this raises the question of under what circumstances will `wc` be closed. Possibly Save will call `Close` unconditionally, or perhaps `Close` will be called in the case of success. This presents a problem for the caller of `Save` as it many want to write additional data to the stream after the document is written.

- A crude solution would be to define a new type which embeds an `io.Writer` and overrides the `Close` method, preventing `Save` from closing the underlying stream. But this would probably be a violation of the LSP, as `NopCloser` doesn't actually close anything.

```go
type NopCloser struct {
    io.Writer
}

// Close has no effect on the underlying writer.
func (c *NopCloser) Close() error { return nil }
```

- A better solution would be to redefine `Save`:

```go
// Save writes the contents of doc to the supplied Writer.
func Save(w io.Writer, doc *Document) error
```

- Noise!

```plain
A great rule of thumb for Go is accept interfaces, return structs.

- Jack Lindamood -
```

## Dependency Inversion Principle (DIP)

```plain
High-level modules should not depend on low-level modules. Both should depend on abstractions.
Abstractions should not depend on details. Details should depend on abstractions.

– Robert C. Martin -
```

- This principle is about **decoupling modules, making them as separate from one another as possible**. The principle states that high-level modules should not depend on low-level modules. Instead, they should both depend on abstractions.

- For example:

```go
package main

type Worker struct {
	ID   int
	Name string
}

func (w Worker) GetID() int {
	return w.ID
}

func (w Worker) GetName() string {
	return w.Name
}

type Supervisor struct {
	ID   int
	Name string
}

func (s Supervisor) GetID() int {
	return s.ID
}

func (s Supervisor) GetName() string {
	return s.Name
}
```

- We have a high-level module `Department` that represents a department in a company, and needs to store information about the workers and supervisors, which are considered a low-level modules:

```go
type Department struct {
    Workers     []Worker
    Supervisors []Supervisor
}
```

- According the DIP, high-level modules should not depend on low-level modules. Instead, both should depend on abstractions. To fix my anti-pattern, I can create an Interface `Employee` that represents both, Worker and Supervisor.

```go
type Employee interface {
    GetID() int
    GetName() string
}

type Department struct {
    Employees []Employee
}
```
