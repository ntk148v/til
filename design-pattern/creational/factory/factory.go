package main

type PaymentMethod interface {
	Pay(amount float32) string
}

type PaymentType int

const (
	Cash PaymentType = iota
	DebitCard
)

type CashPM struct{}
type DebitCardPM struct{}

func (c *CashPM) Pay(amount float32) string {
	return ""
}

func (c *DebitCardPM) Pay(amount float32) string {
	return ""
}

func GetPaymentMethod(t PaymentType) PaymentMethod {
	switch t {
	case Cash:
		return new(CashPM)
	default:
		return new(DebitCardPM)
	}
}

func main() {
	payment := GetPaymentMethod(DebitCard)
	payment.Pay(20)
	payment = GetPaymentMethod(Cash)
	payment.Pay(20)
}
