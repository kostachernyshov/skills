# Numbers come only from files. The agent never types a number into the frame.
#
#   from pixel_kit import data
#   v = data.value({"file": "runs/R01-x/out/cox.tsv", "column": "HR", "where": {"term": "score_high"}})
#   xs = data.column("runs/R01-x/out/scores.tsv", "score", where={"group": "high"})
#   data.write_log("runs/R01-x/out/animation-numbers.tsv")
#
# Each call adds a line to LOG: what was read, from which file, column, and row.
# Files: CSV or TSV with a header row (the delimiter comes from the extension), or YAML (run.yaml)
# with a dotted key ("results.hr"). Gzip files (.gz) are allowed.

import csv, gzip, io, os, re

LOG = []
_cache = {}


def _open(path):
    if path.endswith(".gz"):
        return io.TextIOWrapper(gzip.open(path), encoding="utf-8")
    return open(path, encoding="utf-8-sig")


def table(path):
    """Rows of a CSV/TSV file as a list of dicts (cached)."""
    if path not in _cache:
        if not os.path.exists(path):
            raise FileNotFoundError(f"data file not found: {path}")
        base = path[:-3] if path.endswith(".gz") else path
        delim = "\t" if base.endswith((".tsv", ".txt", ".tab")) else ","
        with _open(path) as f:
            _cache[path] = list(csv.DictReader(f, delimiter=delim))
    return _cache[path]


def _match(row, where):
    return all(str(row.get(k, "")).strip() == str(v).strip() for k, v in (where or {}).items())


def _rows(path, where):
    rows = [r for r in table(path) if _match(r, where)]
    if not rows:
        raise KeyError(f"no row in {path} matches {where}")
    return rows


def _yaml_value(path, key):
    import yaml
    d = yaml.safe_load(open(path, encoding="utf-8"))
    for part in key.split("."):
        if isinstance(d, list):
            d = d[int(part)]
        else:
            if part not in d:
                raise KeyError(f"no key {key} in {path}")
            d = d[part]
    return d


def _num(s, where):
    try:
        return float(s)
    except (TypeError, ValueError):
        raise ValueError(f"not a number: {s!r} ({where})")


def value(ref):
    """One number. ref: {file, column, where?, row?} for a table, or {file, key} for YAML.
    row is a 0-based row index after the where filter; without row the filter must give one row."""
    path = ref["file"]
    if path.endswith((".yaml", ".yml")):
        v = _num(_yaml_value(path, ref["key"]), path)
        LOG.append(dict(value=v, file=path, column=ref["key"], row="", text=""))
        return v
    rows = _rows(path, ref.get("where"))
    if "row" in ref:
        rows = [rows[int(ref["row"])]]
    if len(rows) != 1:
        raise ValueError(f"{len(rows)} rows in {path} match {ref.get('where')}: add 'where' or 'row'")
    col = ref["column"]
    if col not in rows[0]:
        raise KeyError(f"no column {col!r} in {path}")
    v = _num(rows[0][col], f"{path}:{col}")
    LOG.append(dict(value=v, file=path, column=col, row=_where_txt(ref), text=""))
    return v


def count(ref):
    """Number of rows that match a filter: {file, where?}. Use it for n per group."""
    rows = _rows(ref["file"], ref.get("where")) if ref.get("where") else table(ref["file"])
    n = len(rows)
    LOG.append(dict(value=n, file=ref["file"], column="(rows)", row=_where_txt(ref), text=""))
    return n


def column(path, col, where=None, dropna=True):
    """All numbers of one column (a series for a chart). Empty cells and NA are left out."""
    out = []
    for r in table(path):
        if not _match(r, where):
            continue
        s = str(r.get(col, "")).strip()
        if s == "" or s.upper() in ("NA", "NAN", "NONE", "NULL"):
            if dropna:
                continue
            out.append(float("nan"))
            continue
        out.append(_num(s, f"{path}:{col}"))
    if not out:
        raise ValueError(f"no numbers in {path}:{col} with {where}")
    LOG.append(dict(value=f"series n={len(out)}", file=path, column=col, row=_where_txt({"where": where}), text=""))
    return out


def shown(text, value, path, col, where=None):
    """Records a number that a chart shows (for example "HIGH n=224")."""
    LOG.append(dict(value=value, file=path, column=col, row=_where_txt({"where": where}), text=text))


def strings(path, col, where=None):
    """All text values of one column (labels, gene names)."""
    return [str(r.get(col, "")).strip() for r in table(path) if _match(r, where)]


def _where_txt(ref):
    w = ref.get("where")
    s = ";".join(f"{k}={v}" for k, v in (w or {}).items())
    if "row" in ref:
        s += f"#row{ref['row']}"
    return s


def fmt(v, spec=None):
    """Formats a number for the frame. spec: a Python format ("{:.2f}") or None (smart default)."""
    if spec:
        return spec.format(v)
    if isinstance(v, int) or (isinstance(v, float) and v.is_integer() and abs(v) < 1e6):
        return str(int(v))
    if abs(v) >= 100:
        return f"{v:.0f}"
    if abs(v) >= 1:
        return f"{v:.2f}"
    if abs(v) >= 0.001:
        return f"{v:.3f}"
    return f"{v:.1e}"


def note_text(text, names):
    """Records that a text on screen used these number names."""
    for e in LOG:
        if e.get("name") in names and not e["text"]:
            e["text"] = text


def write_log(path):
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write("name\tvalue\ttext\tfile\tcolumn\trow\n")
        for e in LOG:
            f.write(f"{e.get('name', '')}\t{e['value']}\t{e['text']}\t{e['file']}\t{e['column']}\t{e['row']}\n")
    return path


TOKEN = re.compile(r"[A-Za-z0-9.,+\-%]+")


def has_digit(s):
    """True if the text has a typed number: a token with digits and no letters ("470", "0.52", "50%").
    Names with digits ("CD8A", "PRF1", "IL-6", "MHC-I") are not numbers."""
    for tok in TOKEN.findall(s or ""):
        if any(c.isdigit() for c in tok) and not any(c.isalpha() for c in tok):
            return True
    return False
