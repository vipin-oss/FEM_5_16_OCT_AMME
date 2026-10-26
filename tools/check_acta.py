"""Static checks only; this does not replace LaTeX compilation/visual review."""
import re
from pathlib import Path
from collections import Counter
root = Path(__file__).resolve().parents[1]
s = (root / 'manuscript_ActaMechanica.tex').read_text()
bib = (root / 'references.bib').read_text()
keys = set(re.findall(r'@\w+\s*\{\s*([^,]+),', bib))
cited = {k.strip() for group in re.findall(r'\\cite\{([^}]+)\}', s) for k in group.split(',')}
assert not cited - keys, f'Missing bibliography keys: {cited-keys}'
labels = re.findall(r'\\label\{([^}]+)\}', s)
assert all(v == 1 for v in Counter(labels).values()), 'Duplicate labels'
refs = set(re.findall(r'\\(?:eqref|ref)\{([^}]+)\}', s))
assert not refs - set(labels), f'Undefined labels: {refs-set(labels)}'
stack = []
for action, env in re.findall(r'\\(begin|end)\{([^}]+)\}', s):
    if action == 'begin':
        stack.append(env)
    else:
        assert stack and stack.pop() == env, f'Unbalanced environment: {env}'
assert not stack
assert len(re.findall(r'(?<!\\)\$', s)) % 2 == 0, 'Unbalanced dollar delimiters'
figures = re.findall(r'\\includegraphics(?:\[[^]]*\])?\{([^}]+)\}', s)
for figure in figures:
    assert any((root / 'figures' / (figure + ext)).exists() for ext in ('', '.pdf', '.png', '.jpg'))
print(f'PASS: {len(cited)} cited keys, {len(labels)} unique labels, {len(figures)} figures.')
print('NOTE: static checks only. PDF compilation and visual inspection still required.')

# Cross-check cover letter against the submission source.
letter = (root / 'cover_letter_ActaMechanica.tex').read_text()
title = re.search(r'\\title\[[^]]*\]\{([^\n]+)\}', s).group(1)
assert title in re.sub(r'\s+', ' ', letter), 'Cover-letter/manuscript title mismatch'
assert 'p\_anjali@blr.amrita.edu' in letter and 'p\_anjali@blr.amrita.edu' in s
authors = re.findall(r'\\author(\*?)\[(\d+)\]\{\\fnm\{([^}]+)\} \\sur\{([^}]+)\}\}', s)
assert authors == [('', '1', 'Vipin', 'Gupta'), ('', '2', 'Sandeep', 'Kumar'), ('', '3', 'Mohd', 'Vasiulla'), ('', '4', 'Arun Kumar', 'Yadav'), ('*', '5', 'Anjali', 'Patel')], 'Author order/corresponding marker mismatch'
assert 'Corresponding author, on behalf of all authors' in letter
assert 'Anjali Patel' in letter
assert 'Dr. Vipin Gupta' not in letter
for value in ('35.05', '57.75', '-0.22', '+0.19', '-3.43865', '-1.49960', '+0.19321'):
    assert value in letter and value in s, f'Cover-letter value mismatch: {value}'
assert 'Applied Mathematics and Mechanics' not in letter
print('PASS: cover-letter title, corresponding email, journal and numerical claims agree with manuscript.')
