
from statistics import mean
cipher='NKEEVKPGIJJBSIKQOLXZBADJBJLBFZWWFNVPRVAMWNIUAMVIKHFNYPXUWQLKECZYYMEJVWHMTFTMVYVGZXZBADJBJLJGWGKFNDLQZMJLKECZYYMISFKJVKZVGUVLWSNKGMWNIUAMVAIDJWPVKCQKKKQVDFJBLHJMCZTEWJGRZMUJJAMWNIUAMVATUZVIVKYWTHZBYHXKPIZZVVLWFNHHJXCPWNMLDUMXLWPBLLEODLKFZIXJEGOFUVSWYQPNGVNSUVCUDJNMVHRTNNTZVKGZZGJYKWLHRDGUBVEIUVINSLFQRJUQTLHKBLHFBJLWNICLEAJVWKBLHGMTPTUEEVJWHHWCQOHKPGWWVAIQKXGYNFLXKRBUVRVWJLKAPVNJQIVKIWAMFZMWZMUPSJQWWVLQUNKAFHZVIYJTMMYVLHVWXWSGFZHVWVDMOZVVOJJCTHITCANMMHHXZGLTWKSPGITPXFVSQCG'
def get_lenth(cipher):
	k_cipher=''
	l_cipher: int=len(cipher)
	count=[]
	IC=[]
	alphabet=['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']
	ic=0
	for i in range(2, 30):
		for n in range(0,i):
			for j in range(n,l_cipher,i):
				k_cipher+=cipher[j]

			for e in range(0,26):
				count.append(k_cipher.count(alphabet[e]))

			for q in count:
				ic+=q*(q-1)/(len(k_cipher)*len(k_cipher)-1)
			IC.append(ic)
			ic=0
			k_cipher=''
			count=[]
		num=mean(IC)
		IC=[]
		if num >0.06 and num<0.07:
			return i

def Caesar(k):
	Standard = {'A': 0.08167, 'B': 0.01492, 'C': 0.02782, 'D': 0.04253, 'E': 0.12702, 'F': 0.02228, 'G': 0.02015,
				'H': 0.06094, 'I': 0.06966, 'J': 0.00153, 'K': 0.00772, 'L': 0.04025, 'M': 0.02406, 'N': 0.06749,
				'O': 0.07507, 'P': 0.01929, 'Q': 0.00095, 'R': 0.05987, 'S': 0.06327, 'T': 0.09056, 'U': 0.02758,
				'V': 0.00978, 'W': 0.02360, 'X': 0.00150, 'Y': 0.01974, 'Z': 0.00074}
	target=0.065379
	the_count=[];
	eps=1 #与target的最小差
	key=0
	for i in Standard.keys():
		the_count.append(k.count(i)/len(k))
	for i in range(0,26):
		sum=0;
		for j in range(0,26):
			t=(i+j)%26
			sum+=Standard[chr(j+ord('A'))]*the_count[t]
		temp=abs(sum-target)
		if temp<eps :
			eps=temp
			key=i;
	return chr(key+ord('A'))

def get_key(cipher):
	l_cipher: int = len(cipher)
	key_lenth=get_lenth(cipher)
	key=''
	K_cipher=[]
	for i in range(0,key_lenth):
		k_cipher=''
		for j in range(i, l_cipher, key_lenth):
			k_cipher += cipher[j]
		K_cipher.append(k_cipher)
	for k in K_cipher:
		key+=Caesar(k)
	return key


def get_true(cipher):
	key=get_key(cipher)
	l_cipher: int = len(cipher)
	key_lenth = get_lenth(cipher)
	true=''
	for i in range(0, l_cipher):
		true+=chr((-ord(key[i%key_lenth])+ord(cipher[i]))%26+ord('A'))
	return true

def get_true_key(cipher):
	true_key=''
	key=get_key(cipher)
	key_Caesar=Caesar(key)
	print(key_Caesar)
	print(key)
	for i in range(0,get_lenth(cipher)):
		true_key+=chr((ord(key[i])-ord(key_Caesar))%26+ord('A'))
	return true_key

print(get_true_key(cipher))
print(get_true(cipher))