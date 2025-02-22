# ---
# jupyter:
#   jupytext:
#     formats: ipynb,py:percent
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.16.1
#   kernelspec:
#     display_name: Python 3 (ipykernel)
#     language: python
#     name: python3
# ---

# %%
import re
import numpy as np
import itertools

# %%
obst = set()
g0=None
bounds = [0,0]
with open("input.txt") as f:
    for p, c in (((x,y), c) for y, ln in enumerate(f.read().strip().split("\n")) for x,c in enumerate(ln)):
        bounds[0] = max(bounds[0], p[0])
        bounds[1] = max(bounds[1], p[1])
        match c:
            case "#":
                obst.add(p)
            case "^":
                g0=p
obst = frozenset(obst)

# %%
dirs = [(0,-1),(1,0),(0,1),(-1,0)]
di=0
g = tuple(g0)
visited=[]
while all(pi>=0 and pi<=bi for pi,bi in zip(g, bounds)):
    visited.append(g)
    gg = None
    while not gg:
        gg = (g[0]+dirs[di][0], g[1]+dirs[di][1])
        if gg in obst:
            gg = None
            di = (di+1)%4
        else:
            break
    assert gg
    g=gg

mod_candidates = set(visited)-{g0}
len(set(visited))


# %%
# %%time
# -> 8.3s 
def check_loop(bl) -> bool:
    di=0
    g = tuple(g0)
    visited=set()
    while all(pi>=0 and pi<=bi for pi,bi in zip(g, bounds)):
        if (g, di) in visited:
            return True
        visited.add((g, di))
        gg = None
        while not gg:
            gg = (g[0]+dirs[di][0], g[1]+dirs[di][1])
            if gg in obst or gg==bl:
                gg = None
                di = (di+1)%4
            else:
                break
        g=gg
    return False

len(list(filter(check_loop, mod_candidates)))


# %%
# %%time
#-> 19.7s
def check_loop(bl) -> bool:
    di=0
    g = tuple(g0)
    visited=set()
    while all(pi>=0 and pi<=bi for pi,bi in zip(g, bounds)):
        if (g, di) in visited:
            return True
        visited.add((g, di))
        g, di = next((gg, ddi) for gg, ddi in (
            ((g[0]+dirs[ddi][0], g[1]+dirs[ddi][1]), ddi)
            for ddi in ((di+k)%4 for k in range(4)))
            if not (gg in obst or gg==bl)
        )
    return False

len(list(filter(check_loop, mod_candidates)))

# %%
# obstacles in all columns and rows
print(
    [len(set(p[i] for p in obst)) for i in range(2)], 
    bounds
)



# %% [markdown]
# * * *
# Complex numbers for point! 
# - Real axis is y (downward, lines),
# - Imaginary axis is x (left, chars),
# - 
# (x,y) -> y + I x 

# %%
obst = set()
g0=None
bounds = (0,0)
with open(["input.txt", "test00.txt"][0]) as f:
    for p, c in ((y+1j*x, c) for y, ln in enumerate(f.read().strip().split("\n")) for x,c in enumerate(ln)):
        bounds = tuple(max(bi, pi) for bi,pi in zip(bounds, [p.imag, p.real]))
        match c:
            case "#":
                obst.add(p)
            case "^":
                g0=p
obst = frozenset(obst)

# %%
d, g = -1, g0
visited=set()
while 0<=g.real<=bounds[1] and 0<=g.imag<=bounds[0]:
    visited.add(g)
    if (gg := g+d) in obst:
        d *= -1j
    else:
        g=gg

mod_candidates = visited-{g0}
print(len(visited))


# %%
# %%time -> 3.7s
def check_loop(bl) -> bool:
    d, g = -1, g0
    visited=set()
    all_obst = frozenset(obst.union({bl}))
    while 0<=g.real<=bounds[1] and 0<=g.imag<=bounds[0]:
        if (g,d) in visited:
            return True
        visited.add((g,d))
        if (gg := g+d) in all_obst:
            d *= -1j
        else:
            g=gg
    return False

len(list(filter(check_loop, mod_candidates)))

# %%
