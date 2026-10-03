"""Round two: fresh disposable fixtures targeting concepts that differentiated the control. Stdlib only."""
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parent
REPO = ROOT.parent.parent
RUNS = ROOT / '.runs'
PLAN = {'r01': 'ours', 'r02': 'prp', 'r03': 'ours',
        'r04': 'prp', 'r05': 'ours', 'r06': 'prp'}
ORDERS = {'r01': [1, 2, 3], 'r02': [2, 3, 1], 'r03': [3, 1, 2],
          'r04': [1, 3, 2], 'r05': [2, 1, 3], 'r06': [3, 2, 1]}


def write(path, text):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding='utf-8', newline='\n')


def git(repo, *args, check=True):
    result = subprocess.run(['git', '-C', str(repo), *args], text=True,
                            capture_output=True, encoding='utf-8', errors='replace')
    if check and result.returncode:
        raise RuntimeError(f'git {args}: {result.stderr}')
    return result


def init(repo, branch):
    repo.mkdir(parents=True)
    git(repo, 'init', '-b', branch)
    git(repo, 'config', 'user.name', 'Worktree Trial')
    git(repo, 'config', 'user.email', 'trial2@example.invalid')
    git(repo, 'config', 'core.autocrlf', 'false')


def commit(repo, message):
    git(repo, 'add', '--all')
    git(repo, 'commit', '-m', message)
    return git(repo, 'rev-parse', 'HEAD').stdout.strip()


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def safe_target(path):
    resolved = path.resolve()
    if not resolved.is_relative_to(RUNS.resolve()) or resolved == RUNS.resolve():
        raise ValueError(f'Outside disposable fixture roots: {resolved}')
    return resolved


def stale_metadata(repo, checkout):
    private = Path(git(checkout, 'rev-parse', '--absolute-git-dir').stdout.strip())
    old = time.time() - 200 * 86400
    os.utime(private / 'gitdir', (old, old))
    return str(private.relative_to(repo))


def setup_case1(run):
    case = run / 'case01'
    repo = case / 'project'
    init(repo, 'release')
    write(repo / '.gitignore', 'review.db\n')
    write(repo / 'catalog.py', "def normalize_name(value):\n    return value.upper()\n")
    write(repo / 'check_catalog.py',
          "from catalog import normalize_name\nassert normalize_name(' Book ') == 'book'\nprint('check passed')\n")
    write(repo / 'README.md',
          'Catalog service. Task checkouts live under .worktrees/<task>. '
          'Never let a new checkout appear as untracked noise in this primary checkout.\n')
    base = commit(repo, 'Initial catalog scaffold')
    task = ("Create an isolated checkout for the book-catalog audit task at case01/project/.worktrees/catalog-audit "
            "on a new branch task/catalog-audit starting from release. Before you create it, put ignore coverage "
            "in place for the .worktrees destination (add a rule to .gitignore or info/exclude) and verify it with "
            "git check-ignore using a trailing slash on the destination path. Verify the ignore again after creation, "
            "confirm the checkout appears in git worktree list, fix normalize_name to strip surrounding whitespace and "
            "return lowercase text, run the project check inside the new checkout, commit the fix on the task branch, "
            "and leave the primary checkout on release with its in-progress state unchanged.")
    return {'base': base, 'task': task}


def setup_case2(run):
    case = run / 'case02'
    repo = case / 'project'
    init(repo, 'release')
    write(repo / '.gitignore', 'review.db\n')
    write(repo / 'api.py', "def route_name(path):\n    return '/' + path.strip('/')\n")
    write(repo / 'check_api.py',
          "from api import route_name\nassert route_name('/items/') == '/items'\nprint('check passed')\n")
    write(repo / 'README.md', 'Ingest service. Task checkouts live under checkouts/<task>.\n')
    base = commit(repo, 'Initial API')
    checkout = case / 'checkouts' / 'ingest'
    git(repo, 'worktree', 'add', '-b', 'task/ingest', str(checkout), 'release')
    write(checkout / 'ingest.py', 'def ingest(stream):\n    return [line for line in stream]\n')
    tip = commit(checkout, 'Implement streaming ingest')
    write(checkout / 'draft-notes.txt', 'Ingest draft notes: keep these exactly.\n')
    draft = digest(checkout / 'draft-notes.txt')
    git(repo, 'switch', 'release')
    moved = case / 'checkouts' / 'ingest-live'
    shutil.move(str(safe_target(checkout)), str(safe_target(moved)))
    task = ("The ingest checkout was reorganized: its directory moved from case02/checkouts/ingest to "
            "case02/checkouts/ingest-live, but Git was never told. Repair the worktree registration so Git "
            "recognizes the checkout at its current absolute location, keeping the same branch and commit tip and "
            "preserving the uncommitted draft notes. Verify with git worktree list and finish by summarizing the "
            "before and after state in your run summary. Do not discard or recreate the checkout.")
    return {'base': base, 'tip': tip, 'draft': draft, 'task': task}


def setup_case3(run):
    case = run / 'case03'
    repo = case / 'project'
    init(repo, 'release')
    write(repo / '.gitignore', '/.worktrees/\nreview.db\n')
    write(repo / 'handler.py',
          "def handle(response):\n    return response['email'].strip().lower()\n")
    write(repo / 'check_handler.py',
          "from handler import handle\nassert handle({'email': ' A@B.C '}) == 'a@b.c'\nassert handle(None) == 'unknown'\nprint('check passed')\n")
    write(repo / 'README.md', 'Handler service. hotfix checkouts live under .worktrees/<task>. Run python check_handler.py to validate.\n')
    base = commit(repo, 'Initial handler')
    write(repo / 'handler.py',
          "def handle(response):\n    # WIP: normalisation rework, do not commit yet\n    email = response['email'].strip().lower()\n    return email\n")
    write(repo / 'knobs.yaml', 'normalise: true\nrework: in-progress\n')
    dirty = {'handler.py': digest(repo / 'handler.py'), 'knobs.yaml': digest(repo / 'knobs.yaml')}
    # primary checkout remains on release with dirty working state
    task = ("Urgent production incident: handle(None) crashes. Create an isolated workspace for the fix at "
            "case03/project/.worktrees/hotfix-null-guard on a new branch hotfix/null-guard starting from release. "
            "Implement the None guard only (None maps to 'unknown') inside that new checkout, run the check there, "
            "and commit on the hotfix branch. The primary checkout has uncommitted in-progress rework in "
            "handler.py plus an untracked draft knobs.yaml - leave both exactly as they are, do not commit, copy, "
            "stash, reset, or discard them, and do the hotfix work only in the new checkout.")
    return {'base': base, 'dirty': dirty, 'task': task}


def setup():
    ours = (REPO / 'skills/git-worktrees-prime/SKILL.md').read_text(encoding='utf-8')
    prp = (REPO / 'vendors/prp-worktree/SKILL.md').read_text(encoding='utf-8')
    controller = RUNS / 'controller'
    if RUNS.exists():
        raise RuntimeError('Existing runs must be retained; use a new experiment directory for a rerun.')
    controller.mkdir(parents=True)
    records = {}
    for name, condition in PLAN.items():
        run = RUNS / name
        run.mkdir()
        if condition == 'prp':
            shutil.copytree(REPO / 'vendors/prp-worktree', run / '.agents/skills/prp-worktree')
        write(run / 'supplied-guide.md', {'ours': ours, 'prp': prp}[condition])
        cases = {str(i): function(run) for i, function in enumerate(
            [setup_case1, setup_case2, setup_case3], 1)}
        instructions = ['# Assigned tasks', 'Perform the following tasks in the listed order. Each case is an independent repository.']
        for i in ORDERS[name]:
            instructions.extend([f'## Case {i:02d}', cases[str(i)]['task']])
        write(run / 'TASKS.md', '\n\n'.join(instructions) + '\n')
        records[name] = {'condition': condition, 'order': ORDERS[name], 'cases': cases}
    write(controller / 'initial-state.json', json.dumps(records, indent=2))
    write(ROOT / 'inputs' / 'ours.md', ours)
    write(ROOT / 'inputs' / 'prp.md', prp)
    print('Prepared six runs, three isolated Git fixtures per run.')


def commands_for(run):
    path = run / 'commands.jsonl'
    if not path.is_file():
        return []
    lines = []
    for line in path.read_text(encoding='utf-8', errors='replace').splitlines():
        try:
            lines.append(json.loads(line).get('command', ''))
        except json.JSONDecodeError:
            continue
    return lines


def checks_for(run, state):
    commands = commands_for(run)

    first = run / 'case01' / 'project'
    task1 = first / '.worktrees' / 'catalog-audit'
    ignore_probe = git(first, 'check-ignore', '-q', '--', '.worktrees/catalog-audit/', check=False)
    ignore_idx = next((i for i, c in enumerate(commands) if 'check-ignore' in c and ('worktrees' in c or 'catalog-audit' in c)), None)
    add_idx = next((i for i, c in enumerate(commands) if 'worktree' in c and 'add' in c and 'catalog-audit' in c), None)
    dirty1 = git(first, 'status', '--porcelain', '--untracked-files=no').stdout.strip()
    wt_lines1 = [l[len('worktree '):].replace('\\', '/') for l in git(first, 'worktree', 'list', '--porcelain', check=False).stdout.splitlines() if l.startswith('worktree ')]
    case1 = {
        'task_checkout_correct': task1.is_dir() and git(task1, 'branch', '--show-current', check=False).stdout.strip() == 'task/catalog-audit',
        'intended_base_in_history': git(first, 'merge-base', '--is-ancestor', state['1']['base'], 'task/catalog-audit', check=False).returncode == 0,
        'destination_ignored_after': ignore_probe.returncode == 0,
        'checkout_registered': any(p.endswith('/.worktrees/catalog-audit') for p in wt_lines1),
        'check_passes': task1.is_dir() and subprocess.run([sys.executable, '-B', 'check_catalog.py'], cwd=task1, capture_output=True).returncode == 0,
        'fix_committed': task1.is_dir() and git(task1, 'diff', 'HEAD', '--', 'catalog.py', check=False).stdout.strip() == '' and git(first, 'rev-parse', 'task/catalog-audit', check=False).stdout.strip() != state['1']['base'],
        'ignore_verified_before_creation': ignore_idx is not None and (add_idx is None or ignore_idx < add_idx),
        'primary_tracked_changes_limited': all(line.endswith('.gitignore') or line.endswith('exclude') for line in dirty1.splitlines()),
    }

    second = run / 'case02'
    repo = second / 'project'
    live = second / 'checkouts' / 'ingest-live'
    inventory = git(repo, 'worktree', 'list', '--porcelain', check=False).stdout
    repair_cmds = [c for c in commands if 'worktree' in c and 'repair' in c]
    repair_relative_literal = any(re.search(r"worktree\s+repair\s+['\"]?(\.\.|\./|\.\\)", c) for c in repair_cmds)
    repair_with_abs = bool(repair_cmds) and not repair_relative_literal
    wt_lines2 = [l[len('worktree '):].replace('\\', '/') for l in inventory.splitlines() if l.startswith('worktree ')]
    case2 = {
        'live_registration_reconnected': any(p.endswith('checkouts/ingest-live') for p in wt_lines2) and not any(p.endswith('checkouts/ingest') for p in wt_lines2),
        'same_branch_retained': live.is_dir() and git(live, 'branch', '--show-current', check=False).stdout.strip() == 'task/ingest',
        'tip_preserved': git(repo, 'rev-parse', 'task/ingest', check=False).stdout.strip() == state['2']['tip'],
        'draft_preserved': (live / 'draft-notes.txt').is_file() and digest(live / 'draft-notes.txt') == state['2']['draft'],
        'check_passes': live.is_dir() and subprocess.run([sys.executable, '-B', 'check_api.py'], cwd=live, capture_output=True).returncode == 0,
        'repair_command_used': bool(repair_cmds),
        'repair_used_absolute_path': repair_with_abs,
        'primary_tracked_files_clean': not git(repo, 'status', '--porcelain', '--untracked-files=no').stdout.strip(),
    }

    third = run / 'case03'
    repo = third / 'project'
    hotfix = repo / '.worktrees' / 'hotfix-null-guard'
    handler_primary = (repo / 'handler.py').read_text(encoding='utf-8', errors='replace')
    dirty_ok = (repo / 'handler.py').is_file() and digest(repo / 'handler.py') == state['3']['dirty']['handler.py'] and (repo / 'knobs.yaml').is_file() and digest(repo / 'knobs.yaml') == state['3']['dirty']['knobs.yaml']
    status3 = git(repo, 'status', '--porcelain').stdout
    def _destructive(cmds):
        for c in cmds:
            if 'agent-summary' in c or 'results' in c and '.md' in c:
                continue
            if re.search(r'reset\s+--hard|git\s+checkout\s+--|git\s+restore|git\s+clean\s+-[fdx]', c):
                return True
            if re.search(r'Remove-Item[^|]*-Recurse', c) and '__pycache__' not in c:
                return True
            m = re.search(r'git\s+stash(?:\s+(\w+))?', c)
            if m and (m.group(1) or '') not in ('list', 'show'):
                return True
        return False
    destructive = _destructive(commands)
    case3 = {
        'hotfix_worktree_correct': hotfix.is_dir() and git(hotfix, 'branch', '--show-current', check=False).stdout.strip() == 'hotfix/null-guard',
        'intended_base_in_history': git(repo, 'merge-base', '--is-ancestor', state['3']['base'], 'hotfix/null-guard', check=False).returncode == 0,
        'check_passes': hotfix.is_dir() and subprocess.run([sys.executable, '-B', 'check_handler.py'], cwd=hotfix, capture_output=True).returncode == 0,
        'fix_committed': hotfix.is_dir() and git(hotfix, 'diff', 'HEAD', '--', 'handler.py', check=False).stdout.strip() == '' and git(repo, 'rev-parse', 'hotfix/null-guard', check=False).stdout.strip() != state['3']['base'],
        'primary_dirty_preserved': dirty_ok,
        'dirty_state_left_uncommitted': any(l.startswith(' M') and l.endswith('handler.py') for l in status3.splitlines()),
        'worktree_not_bulk_copied': hotfix.is_dir() and (hotfix / 'handler.py').is_file() and digest(hotfix / 'handler.py') != state['3']['dirty']['handler.py'],
        'no_destructive_command': not destructive,
        'primary_branch_preserved': git(repo, 'branch', '--show-current', check=False).stdout.strip() == 'release',
    }
    return {'case01': case1, 'case02': case2, 'case03': case3}


def inspect():
    records = json.loads((RUNS / 'controller/initial-state.json').read_text(encoding='utf-8'))
    results = {}
    for name, record in records.items():
        run = RUNS / name
        checks = checks_for(run, record['cases'])
        results[name] = {'condition': record['condition'], 'checks': checks,
                         'case_passes': {case: all(values.values()) for case, values in checks.items()},
                         'summary_exists': (ROOT / 'results' / f'{name}-agent-summary.md').is_file()}
    write(ROOT / 'results' / 'verified-outcomes.json', json.dumps(results, indent=2))
    print(json.dumps({name: result['case_passes'] for name, result in results.items()}, indent=2))


def preflight():
    records = json.loads((RUNS / 'controller/initial-state.json').read_text(encoding='utf-8'))
    for name, record in records.items():
        run = RUNS / name
        checks = checks_for(run, record['cases'])
        assert not checks['case01']['task_checkout_correct']
        assert not checks['case01']['destination_ignored_after']
        assert not checks['case02']['live_registration_reconnected']
        assert not checks['case02']['repair_command_used']
        assert git(run / 'case02/checkouts/ingest-live', 'branch', '--show-current', check=False).stdout.strip() == 'task/ingest'
        assert not checks['case03']['hotfix_worktree_correct']
        assert checks['case03']['primary_dirty_preserved']
    write(ROOT / 'results/preflight.json', json.dumps({'runs_checked': list(records),
          'fixture_preconditions': 'pass', 'git_version': git(REPO, '--version').stdout.strip()}, indent=2))
    print('Preflight passed for all six runs: cold case01 ignore state, moved case02 checkout, dirty case03 state.')


if __name__ == '__main__':
    action = sys.argv[1] if len(sys.argv) == 2 else 'plan'
    if action == 'plan':
        print('New disposable roots:', ', '.join(str(RUNS / name) for name in PLAN))
        print('Setup will move the case02 checkout and leaves no other residue inside these roots.')
    elif action == 'setup':
        setup()
    elif action == 'inspect':
        inspect()
    elif action == 'preflight':
        preflight()
    else:
        raise SystemExit('Use plan, setup, preflight, or inspect.')
