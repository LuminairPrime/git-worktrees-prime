import json, re, datetime
for rnd in ['round1', 'round2']:
    recs = json.load(open(f'experiments/{rnd}/.runs/controller/initial-state.json'))
    print('##', rnd)
    for r in sorted(recs):
        cmds = []
        with open(f'experiments/{rnd}/.runs/{r}/commands.jsonl', encoding='utf-8') as f:
            for line in f:
                cmds.append(json.loads(line))
        if len(cmds) > 1:
            a = datetime.datetime.fromisoformat(cmds[0]['utc'].replace('Z', '+00:00'))
            b = datetime.datetime.fromisoformat(cmds[-1]['utc'].replace('Z', '+00:00'))
            span = (b - a).total_seconds() / 60
        else:
            span = 0
        full = ' '.join(c['command'] for c in cmds)
        print(f"{r} {recs[r]['condition']:4s} cmds={len(cmds):3d} span={span:5.1f}m "
              f"uv={full.count('uv run'):2d} repair={full.count('worktree repair'):2d} "
              f"check-ignore={full.count('check-ignore'):2d} branchD={full.count('branch -D'):1d} "
              f"force={full.count('--force'):2d} stashrefs={full.count('stash'):2d}")
