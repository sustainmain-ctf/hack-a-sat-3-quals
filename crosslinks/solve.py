#!/usr/bin/env python3

from pwn import *
import pwnlib
import string


# get ticket
with open("ticket.txt", "rb") as f:
    ticket = f.read()
ticket = ticket.strip()

answers = []

# load previously guessed answers
# answers.append("156")
# answers.append("132")
# answers.append("148")
# answers.append("166")
# answers.append("112")

done = False


# get all possible satellite numbers
with open("sats.txt", "rb") as f:
    sats = f.read()

def restart():
    # submit ticket
    conn.recvuntil(b'Ticket please:\n')
    conn.send(ticket + b'\n')

    # submit all known answers
    for i in answers:
        print(i)
        conn.recvuntil(b'What satellite am I:\n')
        conn.send(b'SATELLITE ' + i.encode() + b'\n')
        conn.recvline()
        conn.recvline()

conn = remote("crosslinks.satellitesabove.me", 5300)
restart()

while not done:
    for i in sats.split(b'\n'):
        # check if there's another round
        if (conn.recvline() == b'TLE\n'):
            print(i.decode())
            conn.recvuntil(b'What satellite am I:\n')
            conn.send(b'SATELLITE ' + i + b'\n')
            conn.recvline()
            result = conn.recvline().decode()[:-1]
            print(result)
            if (result == "Correct"):
                answers.append(i.decode())
                break
            elif (result == "Incorrect...bye"):
                conn.close()
                conn = remote("crosslinks.satellitesabove.me", 5300)
                restart()
        else:
            print(conn.recvuntil(b'flag{').decode(), end="")
            print(conn.recvline().decode())
            conn.close()
            done = True
            break