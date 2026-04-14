from flask import Flask, render_template, request
import struct
import math

app = Flask(__name__)

def left_rotate(x, c):
    return ((x << c) | (x >> (32-c))) & 0xffffffff


def to_binary(byte_array):
    return ' '.join(format(x, '08b') for x in byte_array)


def md5_visual(message):

    steps = []
    iteration_table = []

    msg = bytearray(message, 'utf-8')

    steps.append(f"Original Message: {message}")
    steps.append(f"ASCII Values: {list(msg)}")

    binary = to_binary(msg)
    steps.append(f"Binary Representation: {binary}")

    original_len_bits = len(msg) * 8
    steps.append(f"Original Length: {original_len_bits} bits")

    msg.append(0x80)

    while (len(msg)*8) % 512 != 448:
        msg.append(0)

    msg += struct.pack('<Q', original_len_bits)

    steps.append("Padding Applied → message + 1 bit + zeros + length")

    padded_binary = to_binary(msg)
    steps.append(f"Padded Block: {padded_binary}")

    A = 0x67452301
    B = 0xefcdab89
    C = 0x98badcfe
    D = 0x10325476

    steps.append(f"Initial Registers → A={hex(A)} B={hex(B)} C={hex(C)} D={hex(D)}")

    K = [int(abs(math.sin(i+1))*(2**32)) & 0xffffffff for i in range(64)]

    s = [7,12,17,22]*4 + \
        [5,9,14,20]*4 + \
        [4,11,16,23]*4 + \
        [6,10,15,21]*4

    for chunk_offset in range(0, len(msg), 64):

        chunk = msg[chunk_offset:chunk_offset+64]
        M = list(struct.unpack('<16I', chunk))

        steps.append("Message Words (32-bit each):")

        for i in range(16):
            steps.append(f"M{i} = {hex(M[i])}")

        a,b,c,d = A,B,C,D

        for i in range(64):

            if i <= 15:
                F = (b & c) | (~b & d)
                g = i
                func="F"

            elif i <= 31:
                F = (d & b) | (~d & c)
                g = (5*i + 1) % 16
                func="G"

            elif i <= 47:
                F = b ^ c ^ d
                g = (3*i + 5) % 16
                func="H"

            else:
                F = c ^ (b | ~d)
                g = (7*i) % 16
                func="I"

            calc = (F + a + K[i] + M[g]) & 0xffffffff
            rot = left_rotate(calc, s[i])

            a_temp = d
            d_temp = c
            c_temp = b
            b_temp = (b + rot) & 0xffffffff

            iteration_table.append({
                "i":i+1,
                "func":func,
                "M":g,
                "K":hex(K[i]),
                "shift":s[i],
                "A":hex(a_temp),
                "B":hex(b_temp),
                "C":hex(c_temp),
                "D":hex(d_temp)
            })

            a,b,c,d = a_temp,b_temp,c_temp,d_temp

        A=(A+a)&0xffffffff
        B=(B+b)&0xffffffff
        C=(C+c)&0xffffffff
        D=(D+d)&0xffffffff

    result = struct.pack('<4I',A,B,C,D)
    hash_result=''.join('{:02x}'.format(i) for i in result)

    return hash_result, steps, iteration_table


@app.route("/",methods=["GET","POST"])
def index():

    hash_value=None
    steps=[]
    table=[]

    if request.method=="POST":

        msg=request.form["message"]
        hash_value,steps,table=md5_visual(msg)

    return render_template("index.html",hash=hash_value,steps=steps,table=table)


if __name__=="__main__":
    app.run(debug=True)