# Elegant Awk usage

Source: <https://sanctum.geek.nz/arabesque/elegant-awk-usage/>

```bash
# Get a list of all the IP addresses and ports with open TCP connections
netstat -ant | awk '{print $5}'
```

## Matching patterns

```bash
# Only include results with at least one number
netstat -ant | awk '{print $5}' | grep '[0-9]'
netstat -ant | awk '/[0-9]/ {print $5}'
# Ensure that the regular expression should only match data in the 5th column of the output
netstat -ant | awk '$5 ~ /[0-9]/ {print $5}'
```

## Skipping lines

```bash
# Strip the headers out might be to use sed to skip the first two lines of the output
netstat -ant | awk '{print $5}' | sed 1,2d
netstat -ant | awk 'NR>2 {print $5}'
# Get columnar data from the output, in this case the 2nd column containing the process ID
ps -ef | awk '/tilix/ && !/awk/ {print $2}'
```

## Further reading

[Awk Primer](http://en.wikibooks.org/wiki/An_Awk_Primer)
