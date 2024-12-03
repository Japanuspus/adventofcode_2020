# ---
# jupyter:
#   jupytext:
#     formats: py:percent
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

# %%
with open("input.txt") as f:
    input =f.read().strip()


# %%
matches=re.findall(r"mul\((\d+),(\d+)\)", input)
print(sum(int(a)*int(b) for (a,b) in matches))

# %%
matches=re.findall(r"(mul\((\d+),(\d+)\))|(don't)|(do)", input)
s = 0
d = True
for m in matches:
    if m[4]:
        d=True
    elif m[3]:
        d=False
    elif d:
        s+=int(m[1])*int(m[2])
print(s)

# %% [markdown]
# Alternative based on [structural pattern matching](https://peps.python.org/pep-0636/)

# %%
matches=re.findall(r"(mul\((\d+),(\d+)\))|(don't)|(do)", input)
s = 0
d = True
for m in matches:
    match m:
        case (_,_,_,_,"do"):
            d=True
        case (_,_,_,"don't",_):
            d=False
        case (_,a,b,_,_):
            if d:
                s+=int(a)*int(b)
s

# %%
