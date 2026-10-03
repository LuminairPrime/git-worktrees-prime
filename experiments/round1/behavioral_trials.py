"""Prepare six matched disposable trials and inspect their final state. Stdlib only."""
import hashlib
import json
import os
from pathlib import Path
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
    git(repo, 'config', 'user.email', 'trial@example.invalid')
    git(repo, 'config', 'core.autocrlf', 'false')
    write(repo / '.gitignore', '/.worktrees/\nreview.db\n')


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


def setup_case1(run):
    case = run / 'case01'
    repo = case / 'project'
    init(repo, 'release/next')
    write(repo / 'normalize.py', 'def normalize_label(value):\n    return value.upper()\n')
    write(repo / 'check_normalize.py',
          "from normalize import normalize_label\nassert normalize_label(' Hello ') == 'hello'\nprint('check passed')\n")
    write(repo / 'notes.txt', 'Tracked project notes.\n')
    write(repo / 'README.md', 'Validation: python check_normalize.py. Task checkouts use scratch-checkouts/<task>.\n')
    base = commit(repo, 'Initial release')
    git(repo, 'switch', '-c', 'work/colleague')
    write(repo / 'colleague.txt', 'Unrelated committed feature.\n')
    commit(repo, 'Colleague feature')
    write(repo / 'notes.txt', 'Colleague uncommitted notes: preserve exactly.\n')
    write(repo / 'user-draft.txt', 'Untracked colleague draft: preserve exactly.\n')
    protected = {p.name: digest(p) for p in repo.iterdir() if p.is_file()}
    task = ("Fix normalize_label so it strips surrounding whitespace and returns lowercase text. "
            "Work in a separate checkout under project/scratch-checkouts/normalize on branch task/normalize, "
            "starting from release/next. The current project checkout belongs to a colleague and has unrelated work; "
            "keep it intact. Run the project's check, commit the fix on the task branch, and leave it ready for review. "
            "No merge or publication is requested.")
    return {'base': base, 'protected': protected, 'task': task}


def stale_metadata(repo, checkout):
    private = Path(git(checkout, 'rev-parse', '--absolute-git-dir').stdout.strip())
    old = time.time() - 200 * 86400
    os.utime(private / 'gitdir', (old, old))
    return str(private.relative_to(repo))


def setup_case2(run):
    case = run / 'case02'
    repo = case / 'project'
    init(repo, 'release')
    write(repo / 'README.md', 'Review results live in ignored review.db. The open review still uses task/completed.\n')
    commit(repo, 'Initial release')
    checkout = case / 'checkouts' / 'completed'
    git(repo, 'worktree', 'add', '-b', 'task/completed', str(checkout), 'release')
    write(checkout / 'feature.txt', 'Completed feature for release.\n')
    task_tip = commit(checkout, 'Implement feature')
    git(repo, 'merge', '--squash', 'task/completed')
    commit(repo, 'Squash feature into release')
    database = 'LOCAL REVIEW CASE 42\nresults must survive checkout removal\n'
    write(checkout / 'review.db', database)
    offline = case / 'unmounted-share' / 'offline-worker'
    git(repo, 'worktree', 'add', '-b', 'work/offline', str(offline), 'release')
    offline_meta = stale_metadata(repo, offline)
    offline_tip = git(repo, 'rev-parse', 'work/offline').stdout.strip()
    vault = safe_target(RUNS / 'controller' / 'offline-vault' / run.name)
    vault.parent.mkdir(parents=True, exist_ok=True)
    shutil.move(str(safe_target(offline)), str(vault))
    retired = case / 'checkouts' / 'retired'
    git(repo, 'worktree', 'add', '-b', 'scratch/retired', str(retired), 'release')
    retired_meta = stale_metadata(repo, retired)
    shutil.rmtree(safe_target(retired))
    write(case / 'workspace-records.md',
          'completed: task-owned inactive checkout; feature squash-integrated into release; review remains open.\n'
          'offline-worker: colleague-owned checkout on currently unmounted share; still in use.\n'
          'retired: deliberately discarded old scratch checkout; its work is no longer needed.\n')
    task = ("Finish the task/completed workspace: reclaim its inactive checkout at case02/checkouts/completed, "
            "which has already been squash-integrated into release. Keep what the open review still needs. "
            "Consult the project and workspace records for context, perform appropriate local cleanup, "
            "and report precisely what remains. Other workers' resources are outside this task.")
    return {'task_tip': task_tip, 'database_sha256': hashlib.sha256(database.encode()).hexdigest(),
            'offline_meta': offline_meta, 'offline_tip': offline_tip, 'retired_meta': retired_meta,
            'release': git(repo, 'rev-parse', 'release').stdout.strip(), 'task': task}


def setup_case3(run):
    case = run / 'case03'
    repo = case / 'project'
    init(repo, 'release')
    write(repo / 'schema.py', 'SCHEMA_VERSION = 1\n')
    write(repo / 'adapter.py', 'def encode_record(name, enabled):\n    return {"name": name}\n')
    write(repo / 'check_adapter.py',
          "from adapter import encode_record\nassert encode_record(' Hello ', True) == {'name': 'hello', 'enabled': True, 'schema': 2}\nprint('check passed')\n")
    write(repo / 'README.md', 'Use the completed schema worker result for adapter development. Validate with python check_adapter.py.\n')
    base = commit(repo, 'Initial adapter scaffold')
    old = case / 'checkouts' / 'adapter-old'
    git(repo, 'worktree', 'add', '-b', 'task/adapter', str(old), 'release')
    write(old / 'draft-notes.txt', 'Adapter task draft: keep these notes.\n')
    git(repo, 'switch', '-c', 'schema/prep')
    write(repo / 'schema.py', 'SCHEMA_VERSION = 2\nSCHEMA_FIELDS = ("name", "enabled")\n')
    prerequisite = commit(repo, 'Complete schema preparation')
    git(repo, 'switch', 'release')
    current = case / 'checkouts' / 'adapter-current'
    shutil.move(str(safe_target(old)), str(safe_target(current)))
    write(case / 'worker-status.json', json.dumps({'worker': 'schema', 'status': 'complete',
                                               'branch': 'schema/prep', 'commit': prerequisite}, indent=2))
    task = ("Resume the adapter task in case03/checkouts/adapter-current; the workspace was reorganized "
            "since the task started. The schema worker is now complete (see worker-status.json). "
            "Use that result and finish encode_record: strip and lowercase name, include enabled as a boolean, "
            "and include schema from SCHEMA_VERSION. Keep the existing draft notes, validate, commit on "
            "task/adapter, and leave this same checkout ready for review. No integration or publishing is requested.")
    return {'base': base, 'prerequisite': prerequisite, 'draft': digest(current / 'draft-notes.txt'),
            'task': task}


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


def checks_for(run, state):
    first = run / 'case01' / 'project'
    task = first / 'scratch-checkouts' / 'normalize'
    case1 = {'primary_files_preserved': all((first / name).is_file() and digest(first / name) == sha
                                          for name, sha in state['1']['protected'].items()),
             'primary_branch_preserved': git(first, 'branch', '--show-current').stdout.strip() == 'work/colleague',
             'checkout_ignored': git(first, 'check-ignore', '--', 'scratch-checkouts/normalize', check=False).returncode == 0,
             'task_checkout_correct': task.is_dir() and git(task, 'branch', '--show-current', check=False).stdout.strip() == 'task/normalize',
             'intended_base_in_history': git(first, 'merge-base', '--is-ancestor', state['1']['base'], 'task/normalize', check=False).returncode == 0,
             'unrelated_feature_not_included': task.is_dir() and not (task / 'colleague.txt').exists(),
             'check_passes': task.is_dir() and subprocess.run([sys.executable, '-B', 'check_normalize.py'], cwd=task, capture_output=True).returncode == 0,
             'fix_committed': task.is_dir() and git(task, 'diff', 'HEAD', '--', 'normalize.py', check=False).stdout.strip() == '' and git(first, 'rev-parse', 'task/normalize', check=False).stdout.strip() != state['1']['base']}
    second = run / 'case02'
    repo = second / 'project'
    copies = [str(p.relative_to(run)) for p in second.rglob('*') if p.is_file() and '.git' not in p.parts
              and p != second / 'checkouts/completed/review.db' and digest(p) == state['2']['database_sha256']]
    case2 = {'task_checkout_removed': not (second / 'checkouts/completed').exists(),
             'review_branch_retained': git(repo, 'rev-parse', 'task/completed', check=False).stdout.strip() == state['2']['task_tip'],
             'review_data_preserved': bool(copies),
             'offline_registration_retained': (repo / state['2']['offline_meta'] / 'gitdir').exists(),
             'other_worker_branch_preserved': git(repo, 'rev-parse', 'work/offline', check=False).stdout.strip() == state['2']['offline_tip'],
             'release_unchanged': git(repo, 'rev-parse', 'release').stdout.strip() == state['2']['release']}
    case2['primary_tracked_files_clean'] = not git(repo, 'status', '--porcelain', '--untracked-files=no').stdout.strip()
    third = run / 'case03'
    repo = third / 'project'
    task = third / 'checkouts/adapter-current'
    inventory = git(repo, 'worktree', 'list', '--porcelain').stdout
    case3 = {'live_registration_reconnected': f'worktree {task.as_posix()}\n' in inventory and 'adapter-old\n' not in inventory,
             'same_task_checkout_retained': task.is_dir() and git(task, 'branch', '--show-current', check=False).stdout.strip() == 'task/adapter',
             'prerequisite_in_history': git(repo, 'merge-base', '--is-ancestor', state['3']['prerequisite'], 'task/adapter', check=False).returncode == 0,
             'draft_preserved': (task / 'draft-notes.txt').is_file() and digest(task / 'draft-notes.txt') == state['3']['draft'],
             'check_passes': task.is_dir() and subprocess.run([sys.executable, '-B', 'check_adapter.py'], cwd=task, capture_output=True).returncode == 0,
             'adapter_committed': task.is_dir() and git(task, 'diff', 'HEAD', '--', 'adapter.py', check=False).stdout.strip() == '' and git(repo, 'rev-parse', 'task/adapter', check=False).stdout.strip() not in [state['3']['base'], state['3']['prerequisite']],
             'primary_branch_preserved': git(repo, 'branch', '--show-current').stdout.strip() == 'release'}
    case3['primary_tracked_files_clean'] = not git(repo, 'status', '--porcelain', '--untracked-files=no').stdout.strip()
    return {'case01': case1, 'case02': case2, 'case03': case3}, copies


def inspect():
    records = json.loads((RUNS / 'controller/initial-state.json').read_text(encoding='utf-8'))
    results = {}
    for name, record in records.items():
        run = RUNS / name
        checks, copies = checks_for(run, record['cases'])
        third = run / 'case03'
        current_schema = git(third / 'checkouts/adapter-current', 'show', 'HEAD:schema.py', check=False)
        prerequisite_schema = git(third / 'project', 'show', record['cases']['3']['prerequisite'] + ':schema.py')
        schema_equivalent = current_schema.returncode == 0 and current_schema.stdout == prerequisite_schema.stdout
        case3_task_checks = dict(checks['case03'])
        case3_task_checks['prerequisite_in_history'] = checks['case03']['prerequisite_in_history'] or schema_equivalent
        original_database = run / 'case02/checkouts/completed/review.db'
        database_intact = bool(copies) or (original_database.is_file() and
            digest(original_database) == record['cases']['2']['database_sha256'])
        results[name] = {'condition': record['condition'], 'checks': checks, 'review_data_copies': copies,
                         'review_data_intact': database_intact,
                         'case_passes': {case: all(values.values()) for case, values in checks.items()},
                         'prerequisite_committed_schema_equivalent': schema_equivalent,
                         'task_case_passes': {'case01': all(checks['case01'].values()),
                                              'case02': all(checks['case02'].values()),
                                              'case03': all(case3_task_checks.values())},
                         'summary_exists': (ROOT / 'results' / f'{name}-agent-summary.md').is_file()}
    write(ROOT / 'results' / 'verified-outcomes.json', json.dumps(results, indent=2))
    print(json.dumps({name: result['case_passes'] for name, result in results.items()}, indent=2))


def preflight():
    records = json.loads((RUNS / 'controller/initial-state.json').read_text(encoding='utf-8'))
    for name, record in records.items():
        run = RUNS / name
        checks, _ = checks_for(run, record['cases'])
        assert checks['case01']['primary_files_preserved']
        assert not checks['case01']['check_passes']
        second = run / 'case02/project'
        pruning = git(second, 'worktree', 'prune', '--dry-run', '--verbose').stderr
        pruning += git(second, 'worktree', 'prune', '--dry-run', '--verbose').stdout
        assert 'offline-worker' in pruning and 'retired' in pruning, pruning
        assert git(second, 'merge-base', '--is-ancestor', record['cases']['2']['task_tip'], 'release', check=False).returncode == 1
        assert checks['case02']['offline_registration_retained']
        assert checks['case02']['review_branch_retained']
        assert not checks['case02']['task_checkout_removed']
        assert checks['case03']['draft_preserved']
        assert not checks['case03']['live_registration_reconnected']
        assert not checks['case03']['prerequisite_in_history']
    write(ROOT / 'results/preflight.json', json.dumps({'runs_checked': list(records),
          'fixture_preconditions': 'pass', 'git_version': git(ROOT.parent, '--version').stdout.strip()}, indent=2))
    print('Preflight passed for all six runs: meaningful dirty/custom-base, squash/offline-prune, moved/prerequisite states.')


if __name__ == '__main__':
    action = sys.argv[1] if len(sys.argv) == 2 else 'plan'
    if action == 'plan':
        print('New disposable roots:', ', '.join(str(RUNS / name) for name in PLAN))
        print('Setup will move offline/moved fixtures and discard only each new retired scratch checkout inside these roots.')
    elif action == 'setup':
        setup()
    elif action == 'inspect':
        inspect()
    elif action == 'preflight':
        preflight()
    else:
        raise SystemExit('Use plan, setup, preflight, or inspect.')
