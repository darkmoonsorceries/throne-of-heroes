#!/usr/bin/env python3
"""
Tawhid Orchestrator v1 - Zero Context Bleed Architecture
12 Agents × 25 Iter × 64K Context × 60 RPS Throttle
"""
import subprocess, time, json, os, sys
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime

BASE_DIR = "/Users/moe/Programming/wahidOS"
WORKTREE_BASE = f"{BASE_DIR}/.worktrees"
RESULTS_DIR = f"{BASE_DIR}/results"
RPM_LIMIT = 60
MAX_AGENTS = 12
MAX_ITER = 25
MAX_WALL = 300

class RateLimiter:
    def __init__(self, rps):
        self.min_interval = 1.0 / rps
        self.last_call = 0
    
    def wait(self):
        elapsed = time.time() - self.last_call
        if elapsed < self.min_interval:
            time.sleep(self.min_interval - elapsed)
        self.last_call = time.time()

limiter = RateLimiter(RPM_LIMIT)

def run_agent(agent_id: str, sop_file: str):
    worktree = f"{WORKTREE_BASE}/kimi-{agent_id:02d}"
    
    if not os.path.exists(worktree):
        subprocess.run(["git", "worktree", "add", worktree, "-b", f"kimi/agent/{agent_id}"], 
                      cwd=BASE_DIR, capture_output=True)
    
    agent_script = f"""
import os, sys, json, time
sys.path.insert(0, "{BASE_DIR}")

results = []
for i in range({MAX_ITER}):
    start = time.time()
    
    # SOP execution placeholder
    elapsed = time.time() - start
    results.append({{
        "agent": "{agent_id}",
        "iter": i,
        "status": "ok" if elapsed < 60 else "slow",
        "timestamp": time.time()
    }})
    
    if time.time() - start > {MAX_WALL}:
        break

with open("{RESULTS_DIR}/agent_{agent_id}.tsv", "w") as f:
    f.write("agent\\titer\\tstatus\\ttimestamp\\n")
    for r in results:
        f.write(f"{{r['agent']}}\\t{{r['iter']}}\\t{{r['status']}}\\t{{r['timestamp']}}\\n")
"""
    
    script_path = f"{worktree}/agent_runner.py"
    with open(script_path, "w") as f:
        f.write(agent_script)
    
    limiter.wait()
    
    result = subprocess.run(
        [sys.executable, script_path],
        capture_output=True,
        text=True,
        timeout=MAX_WALL + 10
    )
    
    return {
        "agent": agent_id,
        "returncode": result.returncode,
        "stdout": result.stdout[:500],
        "stderr": result.stderr[:500]
    }

def main():
    os.makedirs(RESULTS_DIR, exist_ok=True)
    os.makedirs(WORKTREE_BASE, exist_ok=True)
    
    sop_files = [f for f in os.listdir(f"{BASE_DIR}/wahidSOPs/sops") 
                 if f.endswith(".md") and "META" not in f]
    sop_files = sop_files[:MAX_AGENTS]
    
    print(f"[FATIHA] Spawning {len(sop_files)} agents at {RPM_LIMIT} RPS max")
    start = time.time()
    
    with ThreadPoolExecutor(max_workers=MAX_AGENTS) as pool:
        futures = []
        for i, sop in enumerate(sop_files):
            future = pool.submit(run_agent, i+1, sop)
            futures.append((i+1, future))
        
        results = []
        for agent_id, future in futures:
            try:
                result = future.result(timeout=MAX_WALL + 30)
                results.append(result)
                print(f"  Agent-{agent_id:02d}: exit={result['returncode']}")
            except Exception as e:
                print(f"  Agent-{agent_id:02d}: ERROR {type(e).__name__}")
                results.append({"agent": agent_id, "error": str(e)[:200]})
    
    elapsed = time.time() - start
    
    with open(f"{RESULTS_DIR}/swarm_results.tsv", "w") as out:
        out.write("swarm_time\tagent\treturncode\tstatus\n")
        for r in results:
            status = "ok" if r.get("returncode") == 0 else "fail"
            out.write(f"{elapsed:.1f}\t{r['agent']}\t{r.get('returncode', -1)}\t{status}\n")
    
    print(f"\n[Baqarah] Complete: {len(results)} agents, {elapsed:.1f}s")
    print(f"[Results] {RESULTS_DIR}/swarm_results.tsv")
    
    with open(f"{RESULTS_DIR}/LAWH_SYNC", "w") as f:
        f.write(f"timestamp={datetime.now().isoformat()}\n")
        f.write(f"agents={len(results)}\n")
        f.write(f"wall_time={elapsed:.1f}\n")
        f.write(f"rpm_limit={RPM_LIMIT}\n")
        f.write(f"context_limit=65536\n")

if __name__ == "__main__":
    main()
