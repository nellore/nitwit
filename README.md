# nitwit v0.1.0
Scans Twitter or Github for available handles from a word list. Requires Python 2.x and <a href="http://docs.python-requests.org/en/latest/">requests<a>.
# Important note
`-m no` is a quick fix if the server starts returning <a href="http://en.wikipedia.org/wiki/List_of_HTTP_status_codes#4xx_Client_Error">429</a>s. Some handles may then be false positives if they are reserved keywords.
# Possibilities
Search for "TheReal" + top 100 most-followed Twitter handles:
```
curl -vs "http://twittercounter.com/pages/100" 2>&1 \
    | grep "analytics.track('Viewed Profile'" \
    | awk -F 'href' '{print $2}'\
    | awk -F '"' '{print $2}' \
    | cut -c 2- \
    | uniq \
    | awk '{ print "TheReal" $0 }' \
    | python nitwit.py -d - >nitwits.txt
```
5x (mutate one letter of each of the top 100 most-followed Twitter handles at random and check availability):
```
curl -vs "http://twittercounter.com/pages/100" 2>&1 \
    | grep "analytics.track('Viewed Profile'" \
    | awk -F 'href' '{print $2}'\
    | awk -F '"' '{print $2}' \
    | cut -c 2- \
    | uniq \
    | python -c \
'import random
import sys
import string
import copy
for word in sys.stdin:
    word = list(word.strip());
    for i in xrange(5):
        new_word = copy.deepcopy(word)
        new_word[random.randint(0, len(new_word) - 1)] = \
            random.choice(string.ascii_lowercase)
        print "".join(new_word)' \
    | python nitwit.py -d - >nitwits.txt
```
Search for all three-letter Twitter handles in random order:
```
for i in {a..z}{a..z}{a..z} 
do
    echo $i
done \
    | perl -MList::Util=shuffle -e 'print shuffle(<STDIN>);' \
    | python nitwit.py -d - >nitwits.txt
```
Output only handles from `/usr/share/dict/words` that can be registered on both Twitter and Github:
```
comm <(python nitwit.py -m no -g -s) <(python nitwit.py -m no -s)
```
Check the Twitter handle `i` every five seconds and beep insistently when it's available:
```
while true
do
    if [[ $(echo i | python nitwit.py -m no -d - -s) == "i" ]]; then
        while true
        do
            tput bel
            sleep 1
        done
    fi
    sleep 5
done
```
# Usage details
Display help:
```
python nitwit.py -h
```
Source Twitter search with `/usr/share/dict/words`, writing live stats to `stderr` and available handles to `nitwits.txt`:
```
python nitwit.py >nitwits.txt
```
Search Github, not Twitter:
```
python nitwit.py -g >nitwits.txt
```
If "<tab>m" follows a handle written to stdout, then while the handle has no account associated with it, Twitter/Github is currently blocking its registration. This could mean the handle will be available soon; it could also mean the handle is a reserved word.

Search only for handles that have no associated accounts:
```
python nitwit.py -m yes >nitwits.txt
```
Search only for whether handles can be registered:
```
python nitwit.py -m no >nitwits.txt
```
Search for words in `mydict.txt`, a text file with a single word per line, in random order:
```
cat mydict.txt \
    | perl -MList::Util=shuffle -e 'print shuffle(<STDIN>);' \
    | python nitwit.py -g -d - >nitwits.txt
```
Use proxy `P` (useful in conjunction with Tor if getting <a href="http://en.wikipedia.org/wiki/List_of_HTTP_status_codes#4xx_Client_Error">429</a>'d):
```
python nitwit.py -p P >nitwits.txt
```
Above, `P` is, for example, `http://10.10.1.10:1080`.

Wait for 1.25 seconds between successive server requests:
```
python nitwit.py -w 1.25 >nitwits.txt
```
Suppress status messages written to stderr:
```
python nitwit.py -s >nitwits.txt
```
# License
MIT. See `LICENSE` for details.

# Disclaimer
The author is not responsible for misuse or abuse of this product by other users.
