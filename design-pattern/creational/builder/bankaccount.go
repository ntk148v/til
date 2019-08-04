package main

import "fmt"

type bankAccount struct {
	ownerName            string
	identificationNumber uint64
	branch               string
	balance              int64
}

type BankAccount interface {
	WithDraw(amt uint64)
	Deposit(amt uint64)
	GetBalance() uint64
}

type BankAccountBuilder interface {
	WithOwnerName(name string) BankAccountBuilder
	WithOwnerIdentity(identificationNumber uint64) BankAccountBuilder
	AtBranch(branch string) BankAccountBuilder
	OpeningBalance(balance uint64) BankAccountBuilder
	Build() BankAccount
}

func (acc *bankAccount) WithDraw(amt uint64) {

}

func (acc *bankAccount) Deposit(amt uint64) {

}

func (acc *bankAccount) GetBalance() uint64 {
	return 0
}

func (acc *bankAccount) WithOwnerName(name string) BankAccountBuilder {
	acc.ownerName = name
	return acc
}

func (acc *bankAccount) WithOwnerIdentity(identificationNumber uint64) BankAccountBuilder {
	acc.identificationNumber = identificationNumber
	return acc
}

func (acc *bankAccount) AtBranch(branch string) BankAccountBuilder {
	acc.branch = branch
	return acc
}

func (acc *bankAccount) OpeningBalance(balance uint64) BankAccountBuilder {
	acc.balance = int64(balance)
	return acc
}

func (acc *bankAccount) Build() BankAccount {
	return acc
}

func NewBankAccountBuilder() BankAccountBuilder {
	return &bankAccount{}
}

func main() {
	account := NewBankAccountBuilder().
		WithOwnerName("Kien").
		WithOwnerIdentity(123456789).
		AtBranch("Ha Noi").
		OpeningBalance(1000).Build()

	account.Deposit(10000)
	account.WithDraw(50000)
	fmt.Println(account)
}
