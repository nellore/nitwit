# nitwit v0.1.0
Search Twitter or Github for available usernames from a word list. Requires Python 2.x and <a href="http://docs.python-requests.org/en/latest/">requests<a>.
# Possibilities
Search for "TheReal" + top 100 most-followed Twitter handles:
```
curl -vs "http://twittercounter.com/pages/100" 2>&1 \
    | grep "analytics.track('Viewed Profile'" \
    | awk -F 'href' '{print $2}'\
    | awk -F '"' '{print $2}' \
    | cut -c 2- \
    | uniq \
    | awk '{print "TheReal" $0 }' \
    | python nitwit.py -d - >nitwits.txt
```
Search for all three-letter Twitter handles in a random order:
```
for i in {a..z}{a..z}{a..z} 
    do echo $i
done \
  | perl -MList::Util=shuffle -e 'print shuffle(<STDIN>);' \
  | python nitwit.py -d - >nitwits.txt
```
Output only handles from default dictionary that can be registered on both Twitter and Github:
```
comm <(python nitwit.py -m no -g) <(python nitwit.py -m no)
```
# Usage details
Source Twitter search with `/usr/share/dict/words`, writing live stats to `stderr` and available usernames to `nitwits.txt`:
```
python nitwit.py >nitwits.txt
```
Search Github, not Twitter:
```
python nitwit.py -g >nitwits.txt
```
If "<tab>m" follows a username written, then while the username has no account associated with it, Twitter/Github is currently blocking its registration. This may mean the username will be available soon.

Search only for whether usernames have no associated accounts:
```
python nitwit.py -m yes >nitwits.txt
```
Search only for whether usernames can be registered:
```
python nitwit.py -m no >nitwits.txt
```
Search for words in `mydict.txt`, a text file with a single word per line, in a random order:
```
cat mydict.txt | perl -MList::Util=shuffle -e 'print shuffle(<STDIN>);' | python nitwit.py -g -d - >nitwits.txt
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
