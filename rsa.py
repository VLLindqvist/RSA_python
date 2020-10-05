import random, sys, os, sympy
from Crypto.Util.number import inverse, getPrime

def egcd(a, b):
	# return (g, x, y) such that a*x + b*y = g = gcd(a, b), x being our d
	if a == 0:
		return (b, 0, 1)
	else:
		g, x, y = egcd(b % a, a)
		return (g, y - (b // a) * x, x)

def modInverse(a, m):
	g, x, _ = egcd(a, m)
	if g != 1:
		return None
	else:
		return x % m
			
def generateKey():
	# ====== STEP 1 ========
	# # Generate p prime
	p = getPrime(512)
	# #  Generate q prime
	q = getPrime(512)
	# Calculate n
	n = p * q
	# ======================
	
	# ====== STEP 2 ========
	# Generate e with gcd(e, (p-1)*(q-1)) = 1
	while True:
		e = getPrime(1024)
		if egcd(e, (p - 1) * (q - 1))[0] == 1:
			break
	# ======================

	# ====== STEP 3 ========
	# Generate d, which is the modular multiplicative inverse of e (mod (p-1)(q-1))
	d = modInverse(e, (p - 1) * (q - 1))
	# ======================
	
	# Return private and public key
	publicKey = (n, e)
	privateKey = (p, q, d)
	return publicKey, privateKey

	
def toInt(plainTextMessage):
	EncryptedMessage = ''
	for c in plainTextMessage:
		EncryptedMessage += str(ord(c) * 1000)

	return int(EncryptedMessage)

def toString(EncryptedMessage):
	plainTextMessage = ''
	div = 1000

	while EncryptedMessage > 0:
		EncryptedMessage //= 1000
		charByteIsSmall = int(EncryptedMessage % 1000) < 100
		plainTextMessage = chr(int(EncryptedMessage % 1000)) + plainTextMessage
		div = 100 if charByteIsSmall else 1000
		EncryptedMessage //= div

	return plainTextMessage

def encrypt(plainTextMessage, publicKey):
	m = toInt(plainTextMessage)
	n = publicKey[0]
	e = publicKey[1]
	c = pow(m, e, n)

	# print('\nEncrypted message: ', c)
	
	return c

def decrypt(EncryptedMessage, privateKey):
	p = privateKey[0]
	q = privateKey[1]
	n = p * q
	d = privateKey[2]
	m = pow(EncryptedMessage, d, n)
	plainTextMessage = toString(m)
	print('\nDecrypted message: ', plainTextMessage)

	return None

def main():
	publicKey, privateKey, EncryptedMessage = None, None, None
	a = 0
	while( a != 4 ):
		print('\nMenu')
		print('1. Generate Public and Private keys')
		print('2. Encrypt message')
		print('3. Decrypt message')
		print('4. Exit')
		a = int(input('Choose an option: '))

		if a == 1:
			print('\nGenerating new key pair...')
			publicKey, privateKey = generateKey()
			print('\nPublic key:\n', publicKey, '\n')
			print('Private key:\n', privateKey)
			continue
		elif a == 2:
			plainTextMessage = str(input('Enter message to encrypt: '))
			EncryptedMessage = encrypt(plainTextMessage, publicKey)
			continue
		elif a == 3:
			decrypt(EncryptedMessage, privateKey)
main()