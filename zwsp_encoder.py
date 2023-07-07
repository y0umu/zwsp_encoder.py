import argparse
import os

# TODO use some Shannon coding to reduce the symbol to use.
# https://en.wikipedia.org/wiki/Shannon%E2%80%93Fano_coding
# plain fixed length encoding is super wasting
ENCODE_TABLE = {
    0x0: '0000',
    0x1: '0001',
    0x2: '0010',
    0x3: '0011',
    0x4: '0100',
    0x5: '0101',
    0x6: '0110',
    0x7: '0111',
    0x8: '1000',
    0x9: '1001',
    0xa: '1010',
    0xb: '1011',
    0xc: '1100',
    0xd: '1101',
    0xe: '1110',
    0xf: '1111'
}

def encode_byte(byte: int):
    hbits = byte >> 4  # higher significant bits
    lbits = byte & 0x0f
    return ENCODE_TABLE[hbits] + ENCODE_TABLE[lbits]

def encode_str(s: str):
    enclst = []
    for byte in s.encode('utf-8'):
        c = encode_byte(byte)
        enclst.append(c)
    return ''.join(enclst)

def encode_file(fname):
    enclst = []
    with open(fname, 'rb') as f_in:
        buf = f_in.read(1)
        while len(buf) > 0:
            enclst.append(encode_byte(ord(buf)))
            buf = f_in.read(1)
    str_encoded = ''.join(enclst)
    return str_encoded

def find_encoded(s: str):
    '''
    locate the '\u200c' '\u200d' sequence in s.

    return the first occurence of such sequence in s

    return empty string if not found
    '''
    i = 0
    while s[i] != '\u200c' and s[i] != '\u200d':
        i += 1
    if i > len(s):
        return ''
    
    j = i
    while s[j] == '\u200c' or s[j] == '\u200d':
        j += 1
    
    return s[i:j]

def decode_byte(s: str):
    assert len(s) == 8
    sum = 0
    for i in range(8):
        sum += (2**(7-i)) if s[i] == '\u200d' else 0
    return sum


def decode_str(s: str, to_str=True):
    '''
    if to_str is True, this function decode encoded str to str.
    if to_str is False, this function decode encoded str to bytes
    '''
    if (len(s) % 8) != 0 :
        print('The length of sequence to decode is not multiples of 8. Are you sure the input is correct?')
        return
    declst = []
    for i in range(0, len(s), 8):
        j = i + 8
        c = decode_byte(s[i:j])
        declst.append(c.to_bytes(length=1, byteorder='big'))
    s_bin = b''.join(declst)
    if to_str:
        s_bin = s_bin.decode('utf-8')
    return s_bin
    

def main():
    def encode_callback(args):
        str_in = args.str_plain
        str_out = encode_str(str_in)
        s = str_out.replace('0', '\u200c')  # zero-width non-joiner
        s = s.replace('1', '\u200d')  # zero-width joiner

        if args.outname is None:
            outname = 'encoded.txt'
        else:
            outname =  args.outname
        with open(outname, 'w', encoding='utf-8') as f_out:
            f_out.write(f'{s}]')
        print(f'Output written to {outname}')
    
    def encode_file_callback(args):
        str_out = encode_file(args.fname)
        s = str_out.replace('0', '\u200c')  # zero-width non-joiner
        s = s.replace('1', '\u200d')  # zero-width joiner

        if args.outname is None:
            outname = 'encoded.txt'
        else:
            outname =  args.outname
        with open(outname, 'w', encoding='utf-8') as f_out:
            f_out.write(f'{s}]')
        print(f'Output written to {outname}')
    
    def decode_callback(args):
        str_encoded = find_encoded(args.str_encoded)
        if len(str_encoded) == 0:
            print('There is no encoded string in your sequence')
            return
        str_plain = decode_str(str_encoded)
        print(str_plain)
        return str_plain
    
    def decode_file_callback(args):
        with open(args.fname, 'r', encoding='utf-8') as f_in:
            str_encoded_ = f_in.readline()
        if len(str_encoded_) == 0:
            print('There is no encoded string in your sequence')
            return
        str_encoded = find_encoded(str_encoded_)
        bin_plain = decode_str(str_encoded, to_str=False)
        if args.outname is None:
            outname = 'decoded'
        else:
            outname =  args.outname
        with open(outname, 'wb') as f_out:
            f_out.write(bin_plain)
        print(f'Output written to {outname}')

    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers()

    parser_enc = subparsers.add_parser('encode', help='encode a sequence')
    parser_enc.add_argument('str_plain', help='input sequence')
    parser_enc.add_argument('-o', dest='outname', help='output file path')
    parser_enc.set_defaults(callback=encode_callback)

    parser_encf = subparsers.add_parser('encode_file', help='encode a file')
    parser_encf.add_argument('fname', help='input filename')
    parser_encf.add_argument('-o', dest='outname', help='output file path')
    parser_encf.set_defaults(callback=encode_file_callback)

    parser_dec = subparsers.add_parser('decode', help='decode a sequence')
    parser_dec.add_argument('str_encoded', help='decode the encoded part in the sequence')
    parser_dec.set_defaults(callback=decode_callback)

    parser_decf = subparsers.add_parser('decode_to_bin', help='decode a file and output to a binary')
    parser_decf.add_argument('fname', help='input filename')
    parser_decf.add_argument('-o', dest='outname', help='output file path')
    parser_decf.set_defaults(callback=decode_file_callback)


    args = parser.parse_args()

    args.callback(args)


if __name__ == '__main__':
    main()
