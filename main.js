var fs = require('fs');
var path = require('path');
var CryptoJS = require("crypto-js");

var infopath = path.join(__dirname, 'info.json');
var obj = JSON.parse(fs.readFileSync(infopath, 'utf8'));

var iv = obj["iv"];
var key = obj["key"];

if (process.argv.length === 2) {
  var e = obj["data"];
} else {
  var e = process.argv[2];
}

var O = {
  "-": "+",
  "_": "/",
  "~": "="
}

var t = e.replace(/(-)|(_)|(~)/g, function(e) {
  return O[e]
})

var out = CryptoJS.AES.decrypt(
  t,
  CryptoJS.enc.Utf8.parse(key),
  {
    iv: CryptoJS.enc.Utf8.parse(iv),
    padding: CryptoJS.pad.Pkcs7,
  }
).toString(CryptoJS.enc.Utf8)

console.log(out);
// console.log(CryptoJS.HmacSHA1("Message", "Key"));
