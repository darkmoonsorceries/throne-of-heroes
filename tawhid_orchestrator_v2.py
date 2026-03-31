#!/usr/bin/env python3
"""
Tawhid Orchestrator v2.0 — Real AutoResearch
12 Agents × 25 Iter × Git Branches × Actual SOP Execution
"""
import subprocess, time, json, os, sys, shutil
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime

BASE = "/Users/moe/Programming/wahidOS"
WORKTREE_BASE = f"{BASE}/.worktrees"
RESULTS_DIR = f"{BASE}/results"
AUTO_BRANCH_PREFIX = "autoresearch"
RPM_LIMIT = 60
MAX_AGENTS = 12
MAX_ITER = 25
MAX_WALL = 300  # 5 minutes

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

def read_sop(sop_path):
    """Read SOP content for agent execution"""
    try:
        with open(sop_path) as f:
            return f.read()
    except:
        return "# No SOP content\necho 'Agent running'"

def run_agent(agent_id, sop_file, sop_content):
    """Execute real SOP work in isolated worktree"""
    worktree = f"{WORKTREE_BASE}/auto-{agent_id:02d}"
    branch = f"{AUTO_BRANCH_PREFIX}/{agent_id:02d}"
    
    # KUN: Ensure worktree exists
    if not os.path.exists(worktree):
        result = subprocess.run(
            ["git", "worktree", "add", worktree, "-b", branch],
            capture_output=True, cwd=BASE + "/hermes-src"
        )
        if result.returncode != 0:
            return {"agent": agent_id, "error": "worktree_create_failed"}
    
    # FAYA: Execute SOP iterations
    results = []
    start_time = time.time()
    
    for i in range(MAX_ITER):
        iter_start = time.time()
        
        # Write SOP runner script
        runner = f"""#!/bin/bash
cd {worktree}

# Execute SOP content
{sop_content}

# SOP result
echo "ITERATION_{i}_COMPLETE"
"""
        script_path = f"/tmp/agent_{agent_id:02d}_iter_{i}.sh"
        with open(script_path, "w") as f:
            f.write(runner)
        os.chmod(script_path, 0o755)
        
        limiter.wait()
        
        result = subprocess.run(
            ["/bin/bash", script_path],
            capture_output=True, text=True, timeout=60
        )
        
        results.append({
            "iter": i,
            "status": result.returncode,
            "elapsed": time.time() - iter_start,
            "output": result.stdout[:200]  # Truncate
        })
        
        # Check wall time
        if time.time() - start_time > MAX_WALL:
            break
    
    # UNI: Auto-commit results
    commit_msg = f"auto: agent-{agent_id} completed {len(results)} iters"
    subprocess.run(
        ["git", "add", "-A"],
        capture_output=True, cwd=worktree
    )
    subprocess.run(
        ["git", "commit", "-m", commit_msg, "--allow-empty"],
        capture_output=True, cwd=worktree
    )
    
    return {
        "agent": agent_id,
        "iterations": len(results),
        "duration": time.time() - start_time,
        "success": len([r for r in results if r["status"] == 0]),
        "failures": len([r for r in results if r["status"] != 0]),
        "branch": branch
    }

def main():
    os.makedirs(RESULTS_DIR, exist_ok=True)
    os.makedirs(WORKTREE_BASE, exist_ok=True)
    
    # Find SOPs
    sop_dir = f"{BASE}/wahidSOPs/sops"
    sop_files = [f for f in os.listdir(sop_dir) 
                 if f.endswith(".md") and "META" not in f]
    sop_files = sop_files[:MAX_AGENTS]
    
    print(f"[KUN] Spawning {len(sop_files)} agents")
    print(f"      BASE: {BASE}")
    print(f"      SOPs: {sop_dir}")
    
    # Read SOP contents
    sops_data = [(i+1, f, read_sop(f"{sop_dir}/{f}")) 
                 for i, f in enumerate(sop_files)]
    
    start = time.time()
    
    # Execute swarm
    with ThreadPoolExecutor(max_workers=MAX_AGENTS) as pool:
        futures = [pool.submit(run_agent, aid, sop, content) 
                   for aid, sop, content in sops_data]
        results = [f.result(timeout=MAX_WALL + 30) for f in futures]
    
    elapsed = time.time() - start
    
    # UNI: Aggregate TSV
    with open(f"{RESULTS_DIR}/autoresearch_results.tsv", "w") as out:
        out.write("agent\tbranch\titerations\tsuccess\tfailures\tduration\n")
        for r in results:
            out.write(f"{r.get('agent',0)}\t{r.get('branch','none')}\t{r.get('iterations',0)}\t{r.get('success',0)}\t{r.get('failures',0)}\t{r.get('duration',0):.1f}\n")
    
    print(f"\n[UNI] Complete: {len(results)} agents, {elapsed:.1f}s")
    print(f"      Avg: {sum(r.get('iterations',0) for r in results)/len(results)/elapsed:.1f} iter/s")
    
    # LAWH Sync
    with open(f"{RESULTS_DIR}/LAWH_AUTORESEARCH", "w") as f:
        f.write(f"timestamp={datetime.now().isoformat()}\n")
        f.write(f"agents={len(results)}\n")
        f.write(f"iterations={sum(r.get('iterations',0) for r in results)}\n")
        f.write(f"wall_seconds={elapsed:.1f}\n")
        f.write(f"rpm_limit={RPM_LIMIT}\n")
    
    print(f"      Results: {RESULTS_DIR}/autoresearch_results.tsv")

if __name__ == "__main__":
    main()
