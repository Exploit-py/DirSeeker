
# DirSeeker

This code uses the bruteforce technique to make HTTP GET requests to try to discover directories on a website.

Any misuse and unauthorized use of this code is considered a crime, any misuse / illegal I will not be responsible

## Author

- [@exploit-py](https://www.github.com/exploit-py)


## Suport

Contact me: .main.cpp

# Screenshots

## HELP

![App Screenshot](https://cdn.discordapp.com/attachments/933791098827059204/1135648711964364800/image.png)

## Running with Anchors in Wordlist
![App Screenshot](https://cdn.discordapp.com/attachments/933791098827059204/1135649429228097536/image.png)

## Running without Anchors in Wordlist
![App Screenshot](https://cdn.discordapp.com/attachments/933791098827059204/1135649714746949782/image.png)

## Verbose
![App Screenshot](https://cdn.discordapp.com/attachments/933791098827059204/1135650044394086470/image.png)

## Deploy

Download

```bash
  git clone https://github.com/Exploit-py/DirSeeker.git
```

Install requirements

```python
  pip install -r requirements.txt
```


Run
```python
  python3 DirSeeker.py <host> -w <wordlist>
```

Run with threads

```python
  python3 DirSeeker.py <host> -w <wordlist> -t <threads>
```

