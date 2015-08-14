<pre>
usage: parse_tables.py [-h] [-s SOURCE] [-a] [-d] [-w] [-g] [-f] [-r] [-i]
                       [-b] [-m] [-n NUMBER] [-F SEPARATOR] [-t]

This program is a parser utility for html tables.

optional arguments:
  -h, --help            show this help message and exit
  -s SOURCE, --source SOURCE
                        source html
  -a, --show-attr       show table attributes
  -d, --show-data       show table data.
  -w, --show-raw        show table raw data, only support on --number is
                        specify.
  -g, --debug           show debug info.
  -f, --show-form       show table embeded form
  -r, --show-href       show data's hyper link.
  -i, --show-input      show <input.../input> tag's attributes.
  -b, --show-button     show <button.../button> tag's attributes.
  -m, --remove-not-digit
                        remove not digit char in number field. Ex: thousand
                        comma, space char in pre-fix , or post-fix position,
                        and plus sign
  -n NUMBER, --number NUMBER
                        which number table to show, default is 0 for all
                        table.
  -F SEPARATOR, --separator SEPARATOR
                        field spearator charactar.
  -t, --assist          show assist message


</pre>
