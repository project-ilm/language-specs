#!/usr/bin/env python3
# parse_hindawi_lex.py — extract the canonical<->native keyword table from a Hindawi lex .uhin file.
# The Hindawi system (A. Choudhary, 2003-06, GPL) is the authoritative mapping. We READ it, never reinvent it.
# c2h.uhin: LHS = host (C) token (lex-escaped), printf RHS = native (Devanagari).  h2c.uhin: the reverse.
# context: https://ilm.codes/context/
import re, sys, json
RULE = re.compile(r'^(\S+)\s+\{printf\("(.*?)"\);\}')
def unescape(s):  # collapse lex/printf backslash escapes:  \#->#  \.->.  \{->{  \\n->\n
    return re.sub(r'\\(.)', r'\1', s)
def parse(path, direction):
    """direction 'c2h' => canonical=LHS, native=RHS ; 'h2c' => canonical=RHS, native=LHS"""
    table={}
    for ln in open(path, encoding='utf-8'):
        m = RULE.match(ln.rstrip('\n'))
        if not m: continue
        lhs, rhs = unescape(m.group(1)), unescape(m.group(2))
        if '%s' in rhs or rhs=='' : continue          # skip the yytext string passthrough rules
        if direction=='c2h': canon, nat = lhs, rhs
        else:                canon, nat = rhs, lhs
        if canon and nat: table[canon]=nat
    return table
if __name__=='__main__':
    t=parse(sys.argv[1], sys.argv[2] if len(sys.argv)>2 else 'c2h')
    print(f"entries: {len(t)}")
    for k in ['main','stdio.h','#include','#define','{','\\n','\\t']:
        if k in t: print(f"  {k!r:14} -> {t[k]}")
    json.dump(t, open(sys.argv[3],'w'), ensure_ascii=False, indent=0) if len(sys.argv)>3 else None
