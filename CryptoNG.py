#!/usr/bin/python3
from Crypto.Cipher import AES
from Crypto.Hash import MD5
from math import ceil, sqrt
from PIL import Image
from random import randrange
from sys import argv, stdin, stdout, stderr
from time import time
from zlib import compress, decompress

def encrypt(b, key):
	stderr.write('\n')
	if (type(b) != bytes): b = bytes(b, 'utf-8')
	key = key.ljust(16*(len(key)//16+1), '\0')
	t0 = time()
	b = compress(b, 9)
	t1 = time()
	stderr.write("1. Compressed in %d sec.\n" % (t1-t0))
	b = AES.new(key).encrypt(b.ljust(16*(len(b)//16+1), b'\0'))
	t2 = time()
	stderr.write("2. Encrypted in %d sec.\n" % (t2-t1))
	b = compress(b, 9)
	t3 = time()
	stderr.write("3. Compressed in %d sec.\n" % (t3-t2))
	hash = MD5.new(key.encode()).digest()
	b = bytes([len(hash)]) + hash + b
	sep = bytes()
	while (sep in b): sep += b'\0'
	b = bytes([len(sep)]) + b
	l = len(b)
	s = ceil(sqrt(l))
	t4 = time()
	stderr.write("4. Processed in %d sec.\n" % (t4-t3))
	c = Image.new('L', (l, l))
	p = c.load()
	i = int()
	for x in range(l):
		for y in range(l):
			stderr.write('\r\033[KPreparing Image: %d / %d (%d%%)' % (i, l**2, i/(l**2)*100))
			p[x, y] = randrange(256)
			i += 1
	stderr.write('\r\033[K')
	t5 = time()
	stderr.write("5. Prepared Image in %d sec.\n" % (t5-t4))
	x, y = int(), int()
	for i in range(l):
		stderr.write('\r\033[KWriting Image Data: %d / %d (%d%%)' % (i, l, i/l*100))
		p[x, y] = b[i]
		y = y + (x+1) // s
		x = (x+1) % s
	stderr.write('\r\033[K')
	t6 = time()
	stderr.write("6. Written Image Data in %d sec.\n" % (t6-t5))
	stderr.write("Completed in %d sec.\n\n" % (t6-t0))
	return c

def decrypt(c, key):
	key = key.ljust(16*(len(key)//16+1), '\0')
	s = c.size
	if (s[0] != s[1]): raise AttributeError("Image non-square")
	s = ceil(sqrt(s[0]))
	c = c.load()
	r = bytes()
	t0 = time()
	i = int()
	for x in range(s):
		for y in range(s):
			stderr.write('\r\033[KReading: %d / %d (%d%%)' % (i, s**2, i/(s**2)*100))
			r += bytes([c[y, x]])
			i += 1
	stderr.write('\r\033[K')
	t1 = time()
	stderr.write("1. Read in %d sec.\n" % (t1-t0))
	sep, l, r = b'\0'*r[0], r[1], r[2:]
	hash, r = r[:l], r[l:]
	if (hash != MD5.new(key.encode()).digest()): raise AttributeError("Wrong key")
	r = r.split(sep)[0]
	t2 = time()
	stderr.write("2. Prepared in %d sec.\n" % (t2-t1))
	r = decompress(r)
	t3 = time()
	stderr.write("3. Decompressed in %d sec.\n" % (t3-t2))
	r = AES.new(key).decrypt(r)
	t4 = time()
	stderr.write("4. Decrypted in %d sec.\n" % (t4-t3))
	r = decompress(r)
	t5 = time()
	stderr.write("5. Decompressed in %d sec.\n" % (t5-t4))
	stderr.write("Completed in %d sec.\n\n" % (t5-t0))
	return r

if (__name__ == '__main__'):
	if (len(argv) < 4): exit("Too less args. Usage: %s <encrypt | decrypt> <file> <key>" % argv[0])
	if (argv[1] == 'encrypt'):
		try: encrypt(stdin.read().encode(), argv[3]).save(argv[2])
		except Exception as ex: exit("Error: %s" % ex)
	elif (argv[1] == 'decrypt'):
		try: stdout.write(decrypt(Image.open(argv[2]), argv[3]).decode()); stdout.flush(); stderr.write('\n')
		except Exception as ex: exit("Error: %s" % ex)
	else: exit("Unknown mode. Usage: %s <encrypt | decrypt> <file> <key>" % argv[0])
# by Sdore, 2018
