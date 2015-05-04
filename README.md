# nitwit v0.1.0
Search Twitter for available usernames from a word list.
# Usage
Source search with `/usr/share/dict/words`, writing live stats to `stderr` and words found to `nitwits.txt`:
```
python nitwit.py >nitwits.txt
```
Search for words in `/usr/share/dict/words` in a random order:
```
cat /usr/share/dict/words | perl -MList::Util=shuffle -e 'print shuffle(<STDIN>);' | python nitwit.py -d >nitwits.txt
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
# Disclaimer
The author is not responsible for misuse or abuse of this product by other users.
