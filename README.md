# Transcode
Simple CLI utility that converts data into various encodings.


```
Usage: transcode COMMAND [command options] <subject>

Options:
  -s, --separator <str>  String added in between each char.
  -S, --suffix <str>     String added at the end of the output.
  -P, --prefix <str>     String added in front of the output.
  -u, --unsafe           Prints raw output, can damage TTY !
  -r, --reverse          ie. transcode hex -r 0xDEADBEEF
  -v, --verbosity        Set verbosity level.
  -h, --help             Show this message and exit.

Commands:
  bin:
    -b, --byte-length <int>  Byte length  [default: 7]

  dec:
    -js, --fromCharCode  ie. String.fromCharCode(97,98,99) > abc

  hex:
    -C, --upper  Outputs uppercase hexadecimal
    -c, --lower  Outputs lowercase hexadecimal (default)

  url:
    -a, --all        Process every character
    -A, --non-ascii  Process only non-ASCII characters. Not available in reverse
                     mode. (default)

  zlib:
    -l, --level <int>  Compression level. 0: no compression, 1: best speed, 9:
                       best compression  [default: 6]
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
- `--charset` to set custom encoding charset