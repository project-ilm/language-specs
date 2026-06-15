#!/usr/bin/env python3
# gen_release.py — generate per-language Shaili packages from the keyword registries.
# Data-driven: Perso-Arabic multi-column CSVs (ilm-<host>-keywords-mapping.csv) + per-language
# triple CSVs (construct,native_keyword,romenagri). context: https://ilm.codes/context/
# Usage: gen_release.py <ilm_data_dir> <langspec_data_dir> <out_packages_dir>
import sys, os, csv, json, glob, datetime
ILM, LSP, OUT = sys.argv[1], sys.argv[2], sys.argv[3]
os.makedirs(OUT, exist_ok=True)
NAMES={"ar":"Arabic","ur":"Urdu","fa":"Persian","prs":"Dari","haz":"Hazaragi","sd":"Sindhi",
 "pa_sh":"Punjabi (Shahmukhi)","skr":"Saraiki","bal":"Balochi","brh":"Brahui","hnd":"Hindko",
 "ks":"Kashmiri","khw":"Khowar","scl":"Shina","bft":"Balti","wbl":"Wakhi","ku_sor":"Kurdish (Sorani)",
 "ku_kmr_pa":"Kurdish (Kurmanji, PA)","ota":"Ottoman Turkish","ug":"Uyghur","ha_aj":"Hausa (Ajami)",
 "sw_aj":"Swahili (Ajami)","wo_aj":"Wolof (Ajami)","ff_aj":"Fula (Ajami)","mnk_aj":"Mandinka (Ajami)",
 "jrb":"Judeo-Arabic","jpr":"Judeo-Persian","tg_pa":"Tajik (PA)","lrc":"Northern Luri","mzn":"Mazanderani",
 "glk":"Gilaki","tat":"Tatar","syr_gar":"Syriac (Garshuni)","ms_jawi":"Malay (Jawi)","azb":"South Azerbaijani",
 "kk_arab":"Kazakh (Arabic)","ky_arab":"Kyrgyz (Arabic)","tk_arab":"Turkmen (Arabic)","so_arab":"Somali (Arabic)",
 "kr_arab":"Kanuri (Arabic)","rhg":"Rohingya","hi":"Hindi","bhojpuri":"Bhojpuri","zephyr":"Zephyr (idiolect)"}
EXT={"c":"c","cpp":"cpp","js":"js","python":"py","basic":"bas","lex":"l","yacc":"y","logo":"logo","gcc-x86_64-asm":"s"}
# sample templates per host: placeholders {kw} filled from the language's native map (fallback to canonical)
TEMPLATES={
 "c":'// {NAME} — Shaili (C). context: https://ilm.codes/context/\n{int} main(void) {{\n  {int} n = 5;\n  {if} (n > 0) {{ n = n - 1; }} {else} {{ n = 0; }}\n  {while} (n > 0) {{ n = n - 1; }}\n  {return} 0;\n}}\n',
 "cpp":'// {NAME} — Shaili (C++). context: https://ilm.codes/context/\n{int} main() {{\n  {int} n = 5;\n  {if} (n > 0) {{ n = n - 1; }} {else} {{ n = 0; }}\n  {while} (n > 0) {{ n = n - 1; }}\n  {return} 0;\n}}\n',
 "python":'# {NAME} — Shaili (Python). context: https://ilm.codes/context/\n{def} main():\n    n = 5\n    {if} n > 0:\n        n = n - 1\n    {else}:\n        n = 0\n    {while} n > 0:\n        n = n - 1\n    {return} n\n',
 "js":'// {NAME} — Shaili (JS). context: https://ilm.codes/context/\n{function} main() {{\n  {let} n = 5;\n  {if} (n > 0) {{ n = n - 1; }} {else} {{ n = 0; }}\n  {while} (n > 0) {{ n = n - 1; }}\n  {return} n;\n}}\n',
 "_generic":'# {NAME} — Shaili (generic control sample). context: https://ilm.codes/context/\n{if} (n > 0):\n    n = n - 1\n{else}:\n    n = 0\n{while} (n > 0):\n    n = n - 1\n{return} n\n',
}
PH={"c":["int","if","else","while","return"],"cpp":["int","if","else","while","return"],
 "python":["def","if","else","while","return"],"js":["function","let","if","else","while","return"]}

def host_of(fn): return os.path.basename(fn).replace("ilm-","").replace("-keywords-mapping.csv","")
# packages[langid] = {"name":..,"hosts":{host:{canon:native}}}
pkgs={}
# --- schema A: Perso-Arabic multi-column ---
for f in sorted(glob.glob(os.path.join(ILM,"ilm-*-keywords-mapping.csv"))):
    host=host_of(f)
    with open(f,encoding="utf-8") as fh:
        rd=csv.reader(fh); hdr=next(rd); cols=hdr[2:]
        rows=[r for r in rd if r]
    for ci,lang in enumerate(cols):
        lang=lang.strip()
        if not lang: continue
        m=pkgs.setdefault(lang,{"name":NAMES.get(lang,lang),"family":"Perso-Arabic","hosts":{}}).setdefault("hosts",{}).setdefault(host,{})
        for r in rows:
            canon=r[0].strip(); nat=(r[2+ci].strip() if 2+ci<len(r) else "")
            if canon and nat: m[canon]=nat
# --- schema B: per-language triples (Devanagari/Brahmi) ---
for f in sorted(glob.glob(os.path.join(LSP,"lang_*.csv"))) + sorted(glob.glob(os.path.join(LSP,"dialect_*.csv"))):
    base=os.path.basename(f); langid={"lang_hindi":"hi","dialect_bhojpuri":"bhojpuri"}.get(base[:-4], base[:-4].split("_")[-1])
    with open(f,encoding="utf-8") as fh:
        rd=csv.DictReader(fh); m=pkgs.setdefault(langid,{"name":NAMES.get(langid,langid),"family":"Brahmi (Devanagari)","hosts":{}})["hosts"].setdefault("generic",{})
        for row in rd:
            c=(row.get("construct") or "").strip(); nat=(row.get("native_keyword") or "").strip()
            if c and nat: m[c]=nat
# --- emit packages ---
manifest=[]; now=datetime.date.today().isoformat()
for langid,info in sorted(pkgs.items()):
    pd=os.path.join(OUT,langid); os.makedirs(os.path.join(pd,"keywords"),exist_ok=True); os.makedirs(os.path.join(pd,"samples"),exist_ok=True)
    total=0; hosts=sorted(info["hosts"])
    for host,m in info["hosts"].items():
        if not m: continue
        total+=len(m)
        with open(os.path.join(pd,"keywords",host+".tsv"),"w",encoding="utf-8") as o:
            o.write("canonical\tnative\n")
            for c,n in sorted(m.items()): o.write(f"{c}\t{n}\n")
        tmpl=TEMPLATES.get(host, TEMPLATES["_generic"]); fill={"NAME":info["name"]}
        for kw in PH.get(host, ["if","else","while","return"]): fill[kw]=m.get(kw,kw)
        try: code=tmpl.format(**fill)
        except Exception: code=tmpl.replace("{NAME}",info["name"])
        open(os.path.join(pd,"samples",host+"."+EXT.get(host,"txt")),"w",encoding="utf-8").write(code)
    spec=f"""<!-- context: https://ilm.codes/context/ -->
# Shaili Specification — {info['name']} ({langid})
**Family:** {info['family']} · **Status:** Draft · **Traces to:** ILM Architecture Specification (IAS)
## Abstract
This document specifies the {info['name']} realization of the Shaili localized programming-language family.
It is defined as a **delta** over the normatively-cited host-language standards (C, C++, Python, JavaScript,
BASIC, Lex, Yacc, Logo, x86-64 GNU assembly): the host standards are referenced, not reproduced; the localized
keyword mapping in `keywords/` is the emergent, copyrighted contribution; and an apply tool projects host source
to/from the localized form over the fixed Romenagri canonical identity. Sample programs are in `samples/`.
## 1. Scope  ## 2. Normative references (host standards, by citation)  ## 3. Keyword mapping (see keywords/)
## 4. Conformance (round-trip canonical identity)  ## 5. IP & licensing
GPL-3.0-or-later / CC-BY-4.0 · © 1993-2026 Abhishek Choudhary."""
    open(os.path.join(pd,"SPEC.md"),"w",encoding="utf-8").write(spec)
    pkg={"id":langid,"name":info["name"],"family":info["family"],"hosts":hosts,"keyword_count":total,"updated":now}
    json.dump(pkg,open(os.path.join(pd,"package.json"),"w"),indent=1,ensure_ascii=False)
    manifest.append(pkg)
json.dump({"generated":now,"packages":manifest},open(os.path.join(OUT,"release_manifest.json"),"w"),indent=1,ensure_ascii=False)
print(f"packages: {len(manifest)}  | total keyword entries: {sum(p['keyword_count'] for p in manifest)}")
print("families:", sorted(set(p['family'] for p in manifest)))
