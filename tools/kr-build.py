#!/usr/bin/env python3
"""한국어 패치 플러스 빌드.
  python3 kr-build.py fill            # kr-map-*.json 대응표로 kr-missing-*.json 을 채워 kr-plus/assets/<mod>/lang/ko_kr.json 생성, 미번역 집계
  python3 kr-build.py pending <mod>   # 아직 대응표에 없는 고유 영어 문장만 출력 (번역용)
  python3 kr-build.py pack            # 원본 패치 + kr-plus 를 합쳐 NightfallCraft-KRtrans-plus.zip 생성 (sha1 출력)
"""
import glob
import hashlib
import json
import os
import shutil
import sys
import zipfile

S = os.path.dirname(os.path.abspath(__file__))
ORIG = os.path.expanduser("~/minecraft/nightfall/_download/kr")      # 원본 패치 풀어 둔 곳
PLUS = os.path.join(S, "kr-plus")
OUT = os.path.join(S, "NightfallCraft-KRtrans-plus.zip")


def load_maps():
    m = {}
    for f in sorted(glob.glob(os.path.join(S, "kr-map-*.json"))):
        m.update(json.load(open(f, encoding="utf-8")))
    return m


def missing_files():
    return sorted(glob.glob(os.path.join(S, "kr-missing-*.json")))


def mod_of(path):
    return os.path.basename(path)[len("kr-missing-"):-len(".json")]


def fill():
    maps = load_maps()
    total_done = total_left = 0
    for f in missing_files():
        mod = mod_of(f)
        src = json.load(open(f, encoding="utf-8"))
        out, left = {}, {}
        for k, v in src.items():
            if v in maps:
                out[k] = maps[v]
            else:
                left[k] = v
        # 원본 패치에 같은 모드 ko_kr 이 있으면 그 위에 얹는다 (aether 등 부분 번역)
        base_path = os.path.join(ORIG, "assets", mod, "lang", "ko_kr.json")
        merged = json.load(open(base_path, encoding="utf-8-sig")) if os.path.exists(base_path) else {}
        merged.update(out)
        if merged:
            d = os.path.join(PLUS, "assets", mod, "lang")
            os.makedirs(d, exist_ok=True)
            json.dump(merged, open(os.path.join(d, "ko_kr.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=2)
        total_done += len(out); total_left += len(left)
        print(f"  {mod:22} 번역 {len(out):5} · 남음 {len(left):5}")
    print(f"합계 번역 {total_done} · 남음 {total_left}")


def pending(mod, limit=400):
    maps = load_maps()
    src = json.load(open(os.path.join(S, f"kr-missing-{mod}.json"), encoding="utf-8"))
    seen = []
    for k, v in src.items():
        if v not in maps and v not in seen:
            seen.append(v)
    print(f"# {mod}: 고유 미번역 문장 {len(seen)}개 (키 {sum(1 for v in src.values() if v not in maps)}개)")
    for v in seen[:limit]:
        print(json.dumps(v, ensure_ascii=False))


def pack():
    if os.path.exists(OUT):
        os.remove(OUT)
    with zipfile.ZipFile(OUT, "w", zipfile.ZIP_DEFLATED) as z:
        # 1) 원본 패치 전부
        for root, _, files in os.walk(ORIG):
            for fn in files:
                p = os.path.join(root, fn)
                arc = os.path.relpath(p, ORIG)
                if arc == "pack.mcmeta":
                    continue
                if arc.startswith("__MACOSX") or fn == ".DS_Store":
                    continue
                z.write(p, arc)
        # 2) 플러스 (같은 경로면 덮어쓴다 — 원본과 합쳐진 파일이므로 안전)
        names = set(z.namelist())
        for root, _, files in os.walk(PLUS):
            for fn in files:
                p = os.path.join(root, fn)
                arc = os.path.relpath(p, PLUS)
                if arc in names:
                    # zipfile 은 중복을 허용하므로, 원본 항목을 빼고 다시 쓴다: 간단히 임시 재구성
                    pass
                z.write(p, arc)
        meta = {"pack": {"pack_format": 15,
                         "description": "NightfallCraft KRtrans (원본: 디시 steve/372364) + 누락분 보강 (KR 패치 플러스)"}}
        z.writestr("pack.mcmeta", json.dumps(meta, ensure_ascii=False, indent=2))
    # 중복 항목 제거: 다시 읽어 마지막 것만 남긴다
    tmp = OUT + ".tmp"
    with zipfile.ZipFile(OUT) as zin, zipfile.ZipFile(tmp, "w", zipfile.ZIP_DEFLATED) as zout:
        last = {}
        for info in zin.infolist():
            last[info.filename] = info
        for name, info in last.items():
            zout.writestr(name, zin.read(info))
    os.replace(tmp, OUT)
    sha1 = hashlib.sha1(open(OUT, "rb").read()).hexdigest()
    print(f"{OUT}  {os.path.getsize(OUT)/1024:.0f}KB  sha1={sha1}")
    with zipfile.ZipFile(OUT) as z:
        langs = [n for n in z.namelist() if n.endswith("ko_kr.json")]
        print(f"ko_kr.json {len(langs)}개 · pack.mcmeta OK" if "pack.mcmeta" in z.namelist() else "pack.mcmeta 없음!")


if __name__ == "__main__":
    a = sys.argv[1:]
    if a[:1] == ["fill"]:
        fill()
    elif a[:1] == ["pending"] and len(a) >= 2:
        pending(a[1], int(a[2]) if len(a) > 2 else 400)
    elif a[:1] == ["pack"]:
        pack()
    else:
        sys.exit(__doc__)
