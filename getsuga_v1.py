#!/usr/bin/env python3
"""
MUGEN GETSUGA TENSHOU — The Infinite Crescent
12-agent wave execution (Phase 2 of Tawhid)
"""
import subprocess
import json
import time
import os
from datetime import datetime

BASE_DIR = "/Users/moe/Programming/wahidOS/hermes-src"
WORKTREE_BASE = f"{BASE_DIR}/.git/worktrees"
RESULTS_DIR = f"{BASE_DIR}/results"
RPM_LIMIT = 60  # Under Together 75 RPS ceiling
MAX_AGENTS = 12
MAX_ITER = 25
MAX_WALL = 300  # 5 minutes

def ensure_dirs():
    os.makedirs(RESULTS_DIR, exist_ok=True)
    os.makedirs(f"{BASE_DIR}/.witness", exist_ok=True)

def execute_wave(cycle: int, wave: int):
    """Execute 12 agents in parallel, one per worktree"""
    timestamp = datetime.now().isoformat()
    results = []
    
    print(f"\n☾ Cycle {cycle}, Wave {wave} — Spawning 12 agents...")
    
    # Spawn 12 agents via subprocess (zero context bleed)
    processes = []
    for i in range(1, 13):
        worktree = f"{WORKTREE_BASE}/kimi-{i:02d}"
        agent_name = f"agent-{i:02d}"
        
        # Each agent gets a task (from Kimi's plan in reality)
        # For now: heartbeat + result template
        script = f'''
import time
import json
start = time.time()
iterations = 0
# Simulate work (replace with actual SOP execution)
for i in range({MAX_ITER}):
    iterations += 1
    time.sleep(0.1)  # Throttle
    if time.time() - start > {MAX_WALL}:
        break
result = {{
    "agent": "{agent_name}",
    "cycle": {cycle},
    "wave": {wave},
    "iterations": iterations,
    "duration": time.time() - start,
    "status": "complete",
    "timestamp": time.time()
}}
print(json.dumps(result))
'''
        # Write script to worktree
        script_path = f"{worktree}/agent_runner.py"
        with open(script_path, 'w') as f:
            f.write(script)
        
        # Execute in subprocess (isolated)
        proc = subprocess.Popen(
            ["python3", script_path],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        processes.append((agent_name, proc))
        time.sleep(1/5)  # Throttle to ~5 RPS spawn rate
    
    # Collect results
    print(f"☾ Collecting results...")
    for agent_name, proc in processes:
        try:
            stdout, stderr = proc.communicate(timeout=MAX_WALL + 10)
            if proc.returncode == 0:
                result = json.loads(stdout.strip())
                results.append(result)
                print(f"  ✓ {agent_name}: {result['iterations']} iter")
            else:
                results.append({"agent": agent_name, "status": "failed", "error": stderr[:100]})
                print(f"  ✗ {agent_name}: failed")
        except Exception as e:
            results.append({"agent": agent_name, "status": "error", "error": str(e)[:100]})
            print(f"  ✗ {agent_name}: {e}")
    
    # Write to TSV
    tsv_path = f"{RESULTS_DIR}/cycle-{cycle:03d}-wave-{wave}.tsv"
    with open(tsv_path, 'w') as f:
        f.write("agent\tcycle\twave\titerations\tduration\tstatus\ttimestamp\n")
        for r in results:
            f.write(f"{r.get('agent','unknown')}\t{r.get('cycle',cycle)}\t{r.get('wave',wave)}\t"
                   f"{r.get('iterations',0)}\t{r.get('duration',0):.2f}\t{r.get('status','unknown')}\t"
                   f"{r.get('timestamp',0)}\n")
    
    # Append to witness log
    with open(f"{BASE_DIR}/.witness_log", 'a') as f:
        f.write(f"{timestamp}\tCycle-{cycle:03d}\tWave-{wave}\t{len([r for r in results if r.get('status')=='complete'])}\n")
    
    return results

def main():
    """Execute one Getsuga wave"""
    ensure_dirs()
    
    # Arguments: getsuga.py <cycle> <wave>
    import sys
    cycle = int(sys.argv[1]) if len(sys.argv) > 1 else 1
    wave = int(sys.argv[2]) if len(sys.argv) > 2 else 1
    
    print(f"\n╔════════════════════════════════════════════════════════════════╗")
    print(f"║  MUGEN GETSUGA TENSHOU — Wave Execution                        ║")
    print(f"║  Cycle {cycle:03d} | Wave {wave} | Agents 1-12                       ║")
    print(f"╚════════════════════════════════════════════════════════════════╝\n")
    
    results = execute_wave(cycle, wave)
    
    complete = len([r for r in results if r.get('status') == 'complete'])
    print(f"\n☾ Wave complete: {complete}/{len(results)} agents done")
    print(f"   Results: {RESULTS_DIR}/cycle-{cycle:03d}-wave-{wave}.tsv")
    
    return complete == 12

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
