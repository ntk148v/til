package main

type AsymEncryptionStrategy interface {
	Encrypt(data interface{}) (byte[] cipher, error)
}

type EllipticCurvestrategy struct {}
type RSAstrategy struct {}

func (strat *EllipticCurvestrategy) Encrypt(data interface{}) (byte[] cipher, error) {
	// some compplex math
	return cipher, err
}

func (strat *RSAstrategy) Encrypt(data interface{}) (byte[] cipher, error) {
	// some complex math
	return cipher, err
}

func encryptMessage(msg string, strat AsymEncryptionStrategy) (byte[] cipher, error) {
	return strat.Encrypt(msg)
}

func main() {
	msg := "this is a confidential message"
	cipher, err := encryptMessage(msg, ElliptionCurvestrategy)
	cipher, err = encrypMessage(msg, RSAstrategy)
}
