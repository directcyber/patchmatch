# PatchMatch

Matching painful version requirements for a patched/unpatched versions using a simple rule engine.

The semver versioning scheme is used, meaning `1.2.3` is bigger than `1.2.2` is bigger than `0.0.8` etc.

## Rule specification file

Lines beginning with `#` are comments.

Each rule starts with a comparison operator, followed by a space, then the version number.

- `>` for bigger than
- `<` smaller than
- `>=` for bigger or eq
- `<=` smaller or eq
- `==` equal
- `!=` not equal

each statement on a line separated by a commna is treated as an AND combination.

e.g. 

`>= 7.2.0,< 7.2.2` means bigger or equal to version 7.2.0 AND smaller than 7.2.2, in other words "from version 7.2.0 through to 7.2.2". A real example is the bug is introduced in version 7.2.0, and 7.2.2 is the patched version.

If a version number like `1.2.x` is in a CVE description, it should be translated to `>= 1.2`

## Usage

Write a rule file, and have an input file in CSV/TSV/any delimited file format.

If your file is in a custom delimited format (e.g. psv with pipes `|`), then specify the delimiter via `-d` like `-d '|'`

Otherwise the default format is CSV, and the program detects if you are using TSV using file extension (`.tsv`)

`./patchmatch.py example.rule data.csv`

The version should always be the **last column** of the csv file e.g. `http://example.com,1.2.3`, other than that the other columns dont matter and are not read.


You can specify an output file like so:

`./patchmatch.py -o out.csv example.rule data.csv`

## Example use case

This example input file test.csv contains IP addresses separated by version number of software running:

```
192.168.1.2,1.2.3
192.168.1.13,1.2.0
192.168.1.4,1.2.8
192.168.2.4,1.3.1
192.168.2.9,1.3.0.4
```

The security bulletin for the example software says "version 1.2.0 onwards up to 1.2.7, and version 1.3.x up to 1.3.1 are vulnerable to a vulnerability ..."

which translates to a rules file (test.rules)

```
>= 1.2.0, < 1.2.7
>= 1.3, < 1.3.1
```

```
./patchmatch.py test.csv test.rules
```

outputs these vulnerable hosts:

```
192.168.1.2,1.2.3
192.168.1.13,1.2.0
192.168.2.9,1.3.0.4
```

which means only those 3 hosts are vulnerable.



