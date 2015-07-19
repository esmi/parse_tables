<pre>
usage: parse_tables.py [-h] [-s SOURCE] [-a] [-d] [-f] [-r] [-i] [-b] [-m]
                       [-n NUMBER] [-F SEPARATOR] [-t]

This program is a parser utility for html tables.

optional arguments:
  -h, --help            show this help message and exit
  -s SOURCE, --source SOURCE
                        source html
  -a, --show-attr       show table attributes
  -d, --show-data       show table attributes
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
  -t, --assist          source html
</pre>
