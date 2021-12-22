def caesar_decode(msg, key):
    key = key % 26
    out = []
    for c in msg:
        c = chr(ord('A') + (ord(c) + key - ord('A')) % 26)
        out.append(c)
    return ''.join(out)


msg = "KYVBVPZJJVMVEKVVEKYVUVTFDGIVJJZFEGRJJNFIUZJKYVTLSVFWKYVBVP"
for key in range(1, 26):
    print(f'key:{key} \t', caesar_decode(msg, key))

"THE KEY IS SEVENTEEN THE DECOMPRESSION PASSWORD IS THE CUBE OF THE KEY"
