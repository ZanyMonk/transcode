# Transcode
Simple CLI utility that converts data into various encodings.


```
Usage: transcode COMMAND [command options] <subject>

Common options:
  -s, --separator <str>  String added in between each char.
  -S, --suffix <str>     String added at the end of the output.
  -P, --prefix <str>     String added in front of the output.
  -u, --unsafe           Prints raw output, can damage TTY !
  -v, --verbosity        Set verbosity level.
  -h, --help             Show this message and exit.

Commands:
  b64     Converts to/from base64.
  -c, --charset TEXT  Custom charset.  [default: ABCDEFGHIJKLMNOPQRSTUVWXYZabc
                      defghijklmnopqrstuvwxyz0123456789+/=]

  -bf, --bruteforce   Try all charset combinations
  -r, --reverse       Reverse process (decode)

  bin     Converts to/from binary.
  -b, --byte-length <int>  Byte length  [default: 8]
  -r, --reverse            Reverse process (decode)

  dec     Converts to/from decimal.
  -js, --fromCharCode  ie. String.fromCharCode(97,98,99) > abc
  -r, --reverse        Reverse process (decode)

  hex     None
  -C, --upper    Outputs uppercase hexadecimal
  -c, --lower    Outputs lowercase hexadecimal (default)
  -r, --reverse  Reverse process (decode)

  not     Inverse every bit.

  rot     Rotates characters.
  -n, --offset <int>   Rotation offset.  [default: 13]
  -a, --alpha          Use alphabet (default)
  -A, --ascii          Use entire ASCII charset
  -C, --charset <str>  Use a custom charset. Overwrites -a and -A

  url     Converts to/from URL encoding (ie. %5C).
  -a, --all        Process every character
  -A, --non-ascii  Process only non-ASCII characters. Not available in reverse
                   mode.

  --default        Process reserved and unprintable characters (default)"
  -r, --reverse    Reverse process (decode)

  xor     (un)XOR bytes.
  -x, --hexa  Get key as hexadecimal

  zlib    Compress/decompress zlib encoded data.
  -l, --level <int>  Compression level. [default: 6]
                     0: no compression, 1: best speed, 9: best compression

  -r, --reverse      Reverse process (decode)
```

## Examples
### Shortcut
```
$ transcode hex abcd
0x61626364
$ t hex abcd
0x61626364
```

### Piping
```
$ cat data.bin | t dec -js
String.fromCharCode(137,80,78,71,...)
```

## TODO
- add missing tests
- `--file` to set a file to read input from
- `c2b` command, converts lower/upper case to bits, outputs binary
- mono/bi-grams frequency table
- Index of Coincidence
- `--wrap <int>` to wrap safe output to defined col width
### `c2b`
> Converts lower/uppercase to bits
- `--byte-length` to set output byte length
- `--one <pattern>` to set the regex used to find 1s
- `--zero <pattern>` to set the regex used to find 0s
- `--case` Aa > 10 (make default)
### `url`
- `--depth` to encode/decode multiple times (double encoding)
### `b64`
- `--ignore-garbage` to strip non-compliant characters (make default)