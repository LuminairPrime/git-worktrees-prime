"""Round three: two difficult, quality-scored fixtures. Stdlib only."""
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
ORDERS = {'r01': [1, 2], 'r02': [2, 1], 'r03': [1, 2],
          'r04': [2, 1], 'r05': [1, 2], 'r06': [2, 1]}


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
    git(repo, 'config', 'user.email', 'trial3@example.invalid')
    git(repo, 'config', 'core.autocrlf', 'false')


def commit(repo, message):
    git(repo, 'add', '--all')
    git(repo, 'commit', '-m', message)
    return git(repo, 'rev-parse', 'HEAD').stdout.strip()


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def setup_case1(run):
    case = run / 'case01'
    repo = case / 'project'
    init(repo, 'main')
    write(repo / '.gitignore', '/.worktrees/\nreview.db\n')
    write(repo / 'app.py', 'def version():\n    return 1\n')
    write(repo / 'check_app.py',
          "from app import version\nassert version() == (2, 'app')\nprint('check passed')\n")
    write(repo / 'README.md', 'Release base is main. Legacy experiments live on dev only; never branch from dev. Validate with python check_app.py.\n')
    main = commit(repo, 'Initial')
    git(repo, 'switch', '-c', 'dev')
    write(repo / 'legacy.txt', 'dev-only legacy configuration\n')
    dev = commit(repo, 'Abandoned experiment config')
    git(repo, 'switch', 'main')
    task = ("Start a code-quality audit on the released code. Create an isolated worktree at "
            "case01/project/.worktrees/audit on branch audit starting from main - the visible "
            "branch in this repo right now may be dev, but dev carries one legacy experiment "
            "commit that must NOT leak into the audit. Inside the new checkout, normalize "
            "version() to return the tuple (2, 'app'), run python check_app.py, and commit "
            "the change on branch audit. Then retire the checkout for the reviewer: remove "
            "the worktree with the repository manager but keep the audit branch, and verify "
            "the final state.")
    return {'main': main, 'dev': dev, 'task': task}


def setup_case2(run):
    case = run / 'case02'
    repo = case / 'project'
    init(repo, 'main')
    write(repo / '.gitignore', '/.worktrees/\nreview.db\n')
    write(repo / 'site.py', "def handle(response):\n    return response['email'].strip().lower()\n")
    write(repo / 'check_site.py',
          "from site import handle\nassert handle({'email': ' A@B.C '}) == 'a@b.c'\nassert handle(None) == 'unknown'\nprint('check passed')\n")
    write(repo / 'README.md', 'site service. hotfix workflows use .worktrees/<name>. Run python check_site.py.\n')
    main = commit(repo, 'Initial site')
    wip = "def handle(response):\n    # WIP: normalisation rework, do not commit yet\n    email = response['email'].strip().lower()\n    return email\n"
    write(repo / 'site.py', wip)
    git(repo, 'add', 'site.py')
    git(repo, 'stash', 'push', '-m', 'colleague-hotfix')
    write(repo / 'site.py', wip)
    write(repo / 'draft.yaml', 'normalise: true\nrework: in-progress\n')
    dirty = {'site.py': digest(repo / 'site.py'), 'draft.yaml': digest(repo / 'draft.yaml')}
    stash_list = git(repo, 'stash', 'list').stdout.strip()
    task = ("Urgent incident: the released site.py crashes on handle(None). Create an isolated "
            "checkout at case02/project/.worktrees/null-guard on branch null-guard starting "
            "from main, implement only the None guard (None maps to 'unknown') there, run "
            "python check_site.py, and commit on null-guard. The primary checkout has "
            "uncommitted WIP in site.py plus an untracked draft.yaml, and the shared stash "
            "holds a colleague's hotfix note. Do not commit, copy, stash, reset, or drop "
            "anything from the primary; do the hotfix work only in the new checkout.")
    return {'main': main, 'dirty': dirty, 'stash_list': stash_list, 'task': task}


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
        cases = {str(i): function(run) for i, function in enumerate([setup_case1, setup_case2], 1)}
        instructions = ['# Assigned tasks', 'Perform the following tasks in the listed order. Each case is an independent repository.']
        for i in ORDERS[name]:
            instructions.extend([f'## Case {i:02d}', cases[str(i)]['task']])
        write(run / 'TASKS.md', '\n\n'.join(instructions) + '\n')
        records[name] = {'condition': condition, 'order': ORDERS[name], 'cases': cases}
    write(controller / 'initial-state.json', json.dumps(records, indent=2))
    write(ROOT / 'inputs' / 'ours.md', ours)
    write(ROOT / 'inputs' / 'prp.md', prp)
    print('Prepared six runs, two isolated Git fixtures per run.')


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
    script_create = any('scripts/worktree.py' in c and ' create' in c for c in commands)
    script_list = any('scripts/worktree.py' in c and ' list' in c for c in commands)
    script_remove = any('scripts/worktree.py' in c and ' remove' in c for c in commands)

    first = run / 'case01' / 'project'
    try:
        audit_tip = git(first, 'rev-parse', 'audit', check=False).stdout.strip()
    except subprocess.CalledProcessError:
        audit_tip = ''
    app_at_audit = git(first, 'show', 'audit:app.py', check=False)
    legacy_in_audit = git(first, 'show', 'audit:legacy.txt', check=False)
    case_cmds = [c for c in commands if 'agent-summary.md' not in c and 'results' not in c]
    case_joined = '\n'.join(case_cmds)
    case1 = {
        'checkout_removed': not (first / '.worktrees' / 'audit').is_dir(),
        'branch_audit_retained': git(first, 'rev-parse', '--verify', 'audit', check=False).returncode == 0,
        'audit_derived_from_main': git(first, 'merge-base', '--is-ancestor', state['1']['main'], 'audit', check=False).returncode == 0 and audit_tip != state['1']['main'],
        'legacy_not_in_audit': legacy_in_audit.returncode != 0,
        'audit_committed_normalized_app': app_at_audit.returncode == 0 and "return (2, 'app')" in app_at_audit.stdout,
        'main_unchanged': git(first, 'rev-parse', 'main').stdout.strip() == state['1']['main'],
        'dev_unchanged': git(first, 'rev-parse', 'dev').stdout.strip() == state['1']['dev'],
        'no_branch_deletion_attempted': all('delete-branch' not in c and 'branch -d' not in c and 'branch -D' not in c for c in case_cmds)
            and 'branch -d' not in case_joined and 'branch -D' not in case_joined,
    }

    second = run / 'case02' / 'project'
    current_stash = git(second, 'stash', 'list').stdout.strip()
    null_guard_tip = git(second, 'rev-parse', 'null-guard', check=False).stdout.strip()
    site_at_guard = git(second, 'show', 'null-guard:site.py', check=False)
    status2 = git(second, 'status', '--porcelain').stdout
    hotfix_dir = second / '.worktrees' / 'null-guard'
    case2 = {
        'hotfix_checkout_registered': git(second, 'worktree', 'list', '--porcelain', check=False).stdout.find('.worktrees/null-guard') != -1 or (hotfix_dir.is_dir() and git(hotfix_dir, 'rev-parse', 'HEAD', check=False).returncode == 0),
        'branch_hotfix_exists': git(second, 'rev-parse', '--verify', 'null-guard', check=False).returncode == 0,
        'branch_from_main': git(second, 'merge-base', '--is-ancestor', state['2']['main'], 'null-guard', check=False).returncode == 0 and null_guard_tip != state['2']['main'],
        'guard_committed': site_at_guard.returncode == 0 and "'unknown'" in site_at_guard.stdout and '# WIP' not in site_at_guard.stdout,
        'primary_dirty_preserved': (second / 'site.py').is_file() and digest(second / 'site.py') == state['2']['dirty']['site.py'] and (second / 'draft.yaml').is_file() and digest(second / 'draft.yaml') == state['2']['dirty']['draft.yaml'],
        'dirty_state_uncommitted': any(l.startswith(' M') and l.endswith('site.py') for l in status2.splitlines()),
        'stash_preserved': state['2']['stash_list'] and current_stash == state['2']['stash_list'],
        'no_stash_push_or_drop': all(not re.search(r'git\s+stash\s+(push|drop|clear)', c) for c in commands),
        'primary_branch_preserved': git(second, 'branch', '--show-current').stdout.strip() == 'main',
    }
    return {'case01': case1, 'case02': case2,
            '_telemetry': {'script_create': script_create, 'script_list': script_list, 'script_remove': script_remove}}


def inspect():
    records = json.loads((RUNS / 'controller/initial-state.json').read_text(encoding='utf-8'))
    results = {}
    for name, record in records.items():
        run = RUNS / name
        checks = checks_for(run, record['cases'])
        telemetry = checks.pop('_telemetry')
        results[name] = {'condition': record['condition'], 'checks': checks, 'telemetry': telemetry,
                         'case_passes': {case: all(values.values()) for case, values in checks.items()},
                         'summary_exists': (ROOT / 'results' / f'{name}-agent-summary.md').is_file()}
    write(ROOT / 'results' / 'verified-outcomes.json', json.dumps(results, indent=2))
    print(json.dumps({name: result['case_passes'] for name, result in results.items()}, indent=2))


def preflight():
    records = json.loads((RUNS / 'controller/initial-state.json').read_text(encoding='utf-8'))
    for name, record in records.items():
        run = RUNS / name
        checks = checks_for(run, record['cases'])
        checks.pop('_telemetry')
        assert not checks['case01']['branch_audit_retained']
        assert checks['case01']['legacy_not_in_audit']
        assert git(run / 'case01/project', 'branch', '--show-current').stdout.strip() == 'main'
        stash = git(run / 'case02/project', 'stash', 'list').stdout.strip()
        assert stash == record['cases']['2']['stash_list'], stash
        assert subprocess.run([sys.executable, '-B', 'check_site.py'], cwd=run / 'case02/project', capture_output=True).returncode != 0
    write(ROOT / 'results/preflight.json', json.dumps({'runs_checked': list(records),
          'fixture_preconditions': 'pass', 'git_version': git(REPO, '--version').stdout.strip()}, indent=2))
    print('Preflight passed: dev legacy tip isolation and untouched sharing of stash + WIP.')


if __name__ == '__main__':
    action = sys.argv[1] if len(sys.argv) == 2 else 'plan'
    if action == 'plan':
        print('New disposable roots:', ', '.join(str(RUNS / name) for name in PLAN))
    elif action == 'setup':
        setup()
    elif action == 'inspect':
        inspect()
    elif action == 'preflight':
        preflight()
    else:
        raise SystemExit('Use plan, setup, preflight, or inspect.')
