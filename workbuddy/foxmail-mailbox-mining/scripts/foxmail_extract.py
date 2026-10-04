import os, re, mmap, json, sys, struct, datetime, collections

ROOT = "/Volumes/wuj-data/Jasonwu/Foxmail 7.2/Storage"
OUT = "/tmp/foxmails3.jsonl"
RUN = re.compile(rb'[\x20-\xff]{8,}')
HDR, REC = 51, 512
TODAY = datetime.date.today()

def dec(b):
    for enc in ('utf-8', 'gbk'):
        try:
            return b.decode(enc)
        except Exception:
            pass
    return b.decode('latin-1')

def clean(s):
    return re.sub(r'\s+', ' ', s).strip()

def load_dates(acc):
    m = {}
    for fn in ('recvdate.ind', 'senddate.ind'):
        p = os.path.join(ROOT, acc, 'Indexes', fn)
        if not os.path.isfile(p):
            continue
        d = open(p, 'rb').read()
        n = (len(d) - 32) // 16
        for off in range(32, 32 + 16 * n, 16):
            i = struct.unpack('>I', d[off+4:off+8])[0]
            day = struct.unpack('>I', d[off+8:off+12])[0]
            ms = struct.unpack('>I', d[off+12:off+16])[0]
            if day <= 0 or day > 800000:
                continue
            try:
                dt = datetime.date.fromordinal(day)
            except Exception:
                continue
            if i not in m or (fn == 'recvdate.ind'):
                m[i] = dt.isoformat()
    return m

def fields_for(mm, s, L):
    if s < 2 or mm[s-1] != 0:
        return None
    p = s - 2
    lim = max(0, s - 80)
    while p > lim and mm[p] != 0:
        p -= 1
    if mm[p] != 0:
        return None
    seg = mm[p+1:s-1]
    if not seg or len(seg) > 40:
        return None
    for k in range(len(seg), 0, -1):
        if sum(seg[-k:]) == L:
            out, pos = [], s
            for n in seg[-k:]:
                out.append(mm[pos:pos+n]); pos += n
            return out
    return None

def main():
    total = 0
    with open(OUT, 'w') as fo:
        for acc in sorted(os.listdir(ROOT)):
            idx = os.path.join(ROOT, acc, 'Mails', 'Index')
            if not os.path.isfile(idx):
                continue
            dates = load_dates(acc)
            with open(idx, 'rb') as f:
                mm = mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ)
            cnt = nd = 0
            for m in RUN.finditer(mm):
                g = m.group(); s, L = m.start(), len(g)
                if b'@' not in g:
                    continue
                flds = fields_for(mm, s, L)
                if not flds or len(flds) < 3 or len(flds) % 2 == 0:
                    continue
                vals = [dec(x) for x in flds]
                rcpts = [clean(vals[i+1]).lower() for i in range(2, len(vals) - 1, 2)]
                dt = dates.get((s - HDR) // REC, '')
                if dt:
                    nd += 1
                fo.write(json.dumps({
                    'account': acc,
                    'sender_name': clean(vals[0]),
                    'from': clean(vals[1]).lower(),
                    'to': ';'.join(sorted(set(rcpts))),
                    'subject': clean(vals[-1]),
                    'date': dt,
                }, ensure_ascii=False) + '\n')
                cnt += 1
            mm.close()
            print(f"{acc}: {cnt} dated={nd}", file=sys.stderr)
            total += cnt
    print("TOTAL", total, file=sys.stderr)

if __name__ == '__main__':
    main()
