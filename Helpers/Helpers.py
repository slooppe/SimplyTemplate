#!/usr/bin/env python

import os
import sys
import types
import string
import textwrap
import subprocess
import re


def color(string, status=True, warning=False, bold=True, blue=False, firewall=False, green=False):
    """
    Change text color for the linux terminal, defaults to green.
    Set "warning=True" for red.
    stolen from Veil :)
    """
    attr = []
    if status:
        # green
        attr.append('34')
    if green:
        # green
        attr.append('32')
    if warning:
        # red
        attr.append('31')
    if bold:
        attr.append('1')
    if firewall:
        attr.append('33')
    if blue:
        # blue
        attr.append('34')
    return '\x1b[%sm%s\x1b[0m' % (';'.join(attr), string)


def FormatLong(title, message, frontTab=True, spacing=16):
    """
    Print a long title:message with our standardized formatting.
    Wraps multiple lines into a nice paragraph format.
    """

    lines = textwrap.wrap(textwrap.dedent(message).strip(), width=50)
    returnString = ""

    i = 1
    if len(lines) > 0:
        if frontTab:
            returnString += "\t%s%s" % (('{0: <%s}' %
                                         spacing).format(title), lines[0])
        else:
            returnString += " %s%s" % (('{0: <%s}' %
                                        (spacing-1)).format(title), lines[0])
    while i < len(lines):
        if frontTab:
            returnString += "\n\t"+' '*spacing+lines[i]
        else:
            returnString += "\n"+' '*spacing+lines[i]
        i += 1
    return returnString


def Reindent(s, numSpaces):
    # http://code.activestate.com/recipes/66055-changing-the-indentation-of-a-multi-line-string/
    s = string.split(s, '\n')
    s = [(numSpaces * ' ') + string.lstrip(line) for line in s]
    s = string.join(s, '\n')
    return s


def DirectoryListing(directory):
    # Returns a list of dir's of results
    dirs = []
    for (dir, _, files) in os.walk(directory):
        for f in files:
            path = os.path.join(dir, f)
            if os.path.exists(path):
                dirs.append(path)
    return dirs


def Exit():
    p = " [!] SimplyTemplate now exiting..."
    print color(p, warning=True)
    raise SystemExit


def SelfUpdate():
    p = " [!] SimplyTemplate now Updating.."
    print color(p, firewall=True)
    try:
        val = subprocess.check_output(("sudo", "git", "pull"))
        print val
    except Exception as e:
        print e
        print "Are we root?..."
    try:
        val2 = subprocess.check_output(("sudo", "sh", "Setup.sh"))
        print val2
    except Exception as e:
        print e
        print "Are we root?.."
    p = " [!] Please restart SimplyTemplate.."
    print color(p, firewall=True)
    Exit()


def GetWords(text):
    return re.compile('\w+').findall(text)
