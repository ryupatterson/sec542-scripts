#!/usr/bin/python3

import argparse
import re
import subprocess
import shlex
import os

def strip_ffuf_control_chars(line):
    return re.sub("\x1b\[[0-9][a-zA-Z]", "", line)

def enumerate_subdomain(url, wordlist):
    print("[+] Enumerating subdomains...")
    protocol = re.search(r"https*://", url)
    protocol = protocol.group(0) if protocol else ""
    strip_url = re.sub(r"https*://", '', url)
    command = f'ffuf -w {wordlist} -u {url} -H "Host: FUZZ.{strip_url}"'
    
    ffuf = subprocess.Popen(shlex.split(command), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output = ffuf.communicate()[0].decode("utf-8")

    for line in output.splitlines():
        line = strip_ffuf_control_chars(line)
        if line:
            print(line)
            arr = line.split()
            status = arr[2].replace(",","").strip()
            dir = arr[0]

            if status in ["200", "301", "302"]:
                subprocess.run(shlex.split(f"xdg-open {protocol}{dir}.{strip_url}"))

    print()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog='website_enum.py', description='Wraps ffuf for easier use')
    
    parser.add_argument('-m', '--mode', action='extend', nargs='+', choices=['domain', 'endpoint', 'wordlist'], required=True)
    parser.add_argument('-dW', '--domain-wordlist', required=False)
    parser.add_argument('-eW', '--endpoint-wordlist', required=False)
    parser.add_argument('-eE', '--endpoint-extensions', required=False)
    parser.add_argument('-wO', '--wordlist-output', required=False)
    parser.add_argument('-o', '--output', required=False)

    parser.add_argument('-u', '--uri', type=str)

    args = parser.parse_args()
    print(args)

    for mode in args.mode:
        if mode == 'domain':
            if not args.domain_wordlist:
                raise argparse.ArgumentError(None, message="Missing domain wordlist")
            enumerate_subdomain(args.uri, args.domain_wordlist)
        if mode == 'endpoint':
            if not args.endpoint_wordlist:
                raise argparse.ArgumentError(None, message='Missing endpoint wordlist')
        if mode == 'wordlist':
            if not args.wordlist_output:
                raise argparse.ArgumentError(None, message='Missing wordlist output path')
     
