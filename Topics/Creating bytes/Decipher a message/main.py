str = input()
key = int(input())

bytes = (key).to_bytes(2, 'big')
sum = 0

for byte in bytes:
    sum += byte

decoded_str = ''
codepoint = 0

for letter in str:
    codepoint = ord(letter)
    decoded_str += chr(codepoint + sum)

print(decoded_str)