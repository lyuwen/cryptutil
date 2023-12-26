import os
import json
import base64
import argparse
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad,unpad

O = {
  "-": "+",
  "_": "/",
  "~": "="
}

info = json.load(open(os.path.join(os.path.dirname(__file__), "info.json"), "r"))
iv = info["iv"]
key = info["key"]
data = info["data"]

#CBC with Fix IV
def encrypt(data,key,iv):
  data= pad(data.encode(),16)
  cipher = AES.new(key, AES.MODE_CBC, iv)
  return base64.b64encode(cipher.encrypt(data))

def decrypt(enc,key,iv):
  enc = base64.b64decode(enc)
  cipher = AES.new(key, AES.MODE_CBC, iv)
  return unpad(cipher.decrypt(enc),16)


if __name__ == "__main__":
  parser = argparse.ArgumentParser()
  mode_group = parser.add_mutually_exclusive_group()
  mode_group.add_argument("--mode", type=str, default="decrypt", choices=["decrypt", "encrypt"], help="AES mode.")
  mode_group.add_argument("--decrypt", "-d", dest="mode", action="store_const", const="decrypt", help="Set AES mode to decrypt.")
  mode_group.add_argument("--encrypt", "-e", dest="mode", action="store_const", const="encrypt", help="Set AES mode to encrypt.")
  parser.add_argument("--key", type=str, default=key, help="AES key.")
  parser.add_argument("--iv", type=str, default=iv, help="AES iv.")
  parser.add_argument("data", nargs="?", help="Input data.")

  args = parser.parse_args()

  data = args.data or data
  iv = (args.iv or iv).encode("utf-8")
  key = (args.key or key).encode("utf-8")

  for k, v in O.items():
    data = data.replace(k, v)

  if args.mode == "encrypt":
    encrypted = encrypt(data,key,iv)
    print('encrypted CBC base64 : ',encrypted.decode("utf-8", "ignore"))
  else:
    decrypted = decrypt(data, key, iv)
    print('data: ', decrypted.decode("utf-8", "ignore"))
