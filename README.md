# Zero Width Space Encoder
Plain simple zero width space encoder that **does not** necessarily hide information in texts.

There is no optimization of memory or speed for the time being. 
No Huffman, LZW, arithimatic or any other fancy coding algorithms are used. 
The code words are at fixed size. The code is dirty.

The output encoded strings is always suffixed with a "]" so that you can distinguish the border of the hard-to-notice characters.

## Examples
```bash
# encode some text from command line argument
python zwsp_encoder.py encode "https://github.com" -o "github.txt"

# encode any binaries
python zwsp_encoder.py encode_file "mini.webp" -o pic_enc.txt

# decode from command line argument
python zwsp_encoder.py decode "‌‍‍‌‍‌‌‌‌‍‍‍‌‍‌‌‌‍‍‍‌‍‌‌‌‍‍‍‌‌‌‌‌‍‍‍‌‌‍‍‌‌‍‍‍‌‍‌‌‌‍‌‍‍‍‍‌‌‍‌‍‍‍‍‌‍‍‍‌‍‌‌‌‍‍‌‍‌‌‌‌‌‍‍‌‌‌‌‌‍‍‌‍‍‌‍‌‍‍‌‌‌‌‍‌‍‍‍‌‌‍‍‌‍‍‍‍‌‌‌‌‍‍‍‌‍‌‍‌‌‍‌‍‍‍‌‌‍‍‌‌‌‍‍‌‍‍‌‍‍‍‍‌‍‍‌‍‍‌‍]"

# decode from text file and write to binary file
python zwsp_encoder.py decode_to_bin "pic_enc.txt" "mini_decoded.webp"
```
