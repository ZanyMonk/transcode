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