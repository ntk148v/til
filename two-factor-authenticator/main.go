package main

import (
	"bytes"
	"crypto/hmac"
	"crypto/sha1"
	"encoding/base32"
	"encoding/binary"
	"fmt"
	"io/ioutil"
	"strconv"
	"strings"
	"time"
)

type twoFactorAuthenticator struct {
	secret string
}

func newTwoFactorAuthenticator(secret string) twoFactorAuthenticator {
	return twoFactorAuthenticator{
		secret: secret,
	}
}

func (tfa twoFactorAuthenticator) getHOTPToken(interval int64) (hotpToken string, err error) {
	// Convert secret to base32 encoding. Base32 encoding desires a 32-character
	// subset of [A-Z] and ten digits 0-9
	key, err := base32.StdEncoding.DecodeString(strings.ToUpper(tfa.secret))
	if err != nil {
		return hotpToken, err
	}
	bs := make([]byte, 8)
	binary.BigEndian.PutUint64(bs, uint64(interval))

	// Signing the value using HMAC-SHA1 algorithm
	hash := hmac.New(sha1.New, key)
	hash.Write(bs)
	h := hash.Sum(nil)

	// We're going to use a subset of the generated hash.
	// Using the last nibble (half-byte) to choose the index to start from.
	// This number is always appropriate as it's maximum decimal 15, the hash will
	// have the maximum index 19 (20 bytes of SHA1) and we need 4 bytes.
	o := (h[19] & 15)

	var header uint32
	//Get 32 bit chunk from hash starting at the o
	r := bytes.NewReader(h[o : o+4])
	err = binary.Read(r, binary.BigEndian, &header)
	if err != nil {
		return hotpToken, err
	}

	//Ignore most significant bits as per RFC 4226.
	//Takes division from one million to generate a remainder less than < 7 digits
	h12 := (int(header) & 0x7fffffff) % 1000000

	//Converts number as a string
	otp := strconv.Itoa(int(h12))
	hotpToken = prefix0(otp)
	return hotpToken, err
}

func (tfa twoFactorAuthenticator) getTOTPToken() (totpToken string, err error) {
	interval := time.Now().Unix() / 30
	return tfa.getHOTPToken(interval)
}

// prefix0 appends extra 0s if the length of otp less
// than 6. If otp is "1234", it will return it as "001234".
func prefix0(otp string) string {
	if len(otp) == 6 {
		return otp
	}
	return strings.Repeat("0", 6-len(otp)) + otp
}

func main() {
	// Read the secret from the file system
	data, err := ioutil.ReadFile("secret.pem")
	if err != nil {
		panic(err)
	}
	t := newTwoFactorAuthenticator(string(data))
	otp, err := t.getTOTPToken()
	if err != nil {
		panic(err)
	}
	fmt.Println(otp)
}
