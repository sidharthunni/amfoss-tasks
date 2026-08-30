#!/usr/bin/env python3
"""
Grand Line Guardian - a terminal process monitor reading directly from /proc.

Every process is a "ship" sailing the Grand Line. This tool reads the
Linux /proc virtual filesystem directly (no psutil) to show, in real time:
    - PID, Process Name, CPU%, Memory%
    - Total active process count

Controls:
    UP / DOWN    - move selection
    k            - terminate (SIGTERM) the selected process
    q            - quit
"""
import curses
import os
import time
import signal

CLK_TCK = os.sysconf("SC_CLK_TCK")  # clock ticks per second, usually 100
REFRESH_MS = 500                     # < 1s refresh interval, as required


def get_process_list():
    """Return list of numeric PIDs currently in /proc."""
    return [int(e) for e in os.listdir("/proc") if e.isdigit()]


def read_proc_stat(pid):
    """Read /proc/[pid]/stat and return (name, utime, stime)."""
    with open(f"/proc/{pid}/stat", "r") as f:
        data = f.read()
    rparen = data.rfind(")")
    name = data[data.find("(") + 1:rparen]
    fields = data[rparen + 2:].split()
    utime = int(fields[11])  # field 14 (1-indexed): user-mode CPU ticks
    stime = int(fields[12])  # field 15 (1-indexed): kernel-mode CPU ticks
    return name, utime, stime


def read_proc_mem_kb(pid):
    """Read VmRSS (resident set size) from /proc/[pid]/status, in KB."""
    try:
        with open(f"/proc/{pid}/status", "r") as f:
            for line in f:
                if line.startswith("VmRSS:"):
                    return int(line.split()[1])
    except FileNotFoundError:
        pass
    return 0


def get_total_mem_kb():
    with open("/proc/meminfo", "r") as f:
        for line in f:
            if line.startswith("MemTotal:"):
                return int(line.split()[1])
    return 1


def sample_processes(prev_times, prev_wall):
    """Take one sample of all processes; returns (procs, new_times, now)."""
    now_wall = time.time()
    elapsed = now_wall - prev_wall if prev_wall else 0.1
    total_mem_kb = get_total_mem_kb()

    procs = []
    new_times = {}
    for pid in get_process_list():
        try:
            name, utime, stime = read_proc_stat(pid)
        except (FileNotFoundError, ProcessLookupError, ValueError, IndexError):
            continue

        total_ticks = utime + stime
        new_times[pid] = total_ticks

        prev_ticks = prev_times.get(pid, total_ticks)
        delta_ticks = total_ticks - prev_ticks
        cpu_percent = 100.0 * (delta_ticks / CLK_TCK) / elapsed if elapsed > 0 else 0.0

        mem_kb = read_proc_mem_kb(pid)
        mem_percent = 100.0 * mem_kb / total_mem_kb if total_mem_kb else 0.0

        procs.append({
            "pid": pid,
            "name": name,
            "cpu": cpu_percent,
            "mem_kb": mem_kb,
            "mem_pct": mem_percent,
        })

    return procs, new_times, now_wall


def draw(stdscr, procs, selected_idx, total_count, message=""):
    stdscr.erase()
    height, width = stdscr.getmaxyx()

    title = " GRAND LINE GUARDIAN - /proc Process Monitor "
    stdscr.addstr(0, 0, title.center(width, "="), curses.A_BOLD)
    stdscr.addstr(1, 0, (f" Active Ships (processes): {total_count}   "
                         f"[UP/DOWN] move  [k] terminate  [q] quit")[:width - 1])

    col_header = f"{'PID':>7}  {'NAME':<20}  {'CPU%':>7}  {'MEM(MB)':>9}  {'MEM%':>6}"
    stdscr.addstr(3, 0, col_header[:width - 1], curses.A_UNDERLINE)

    max_rows = height - 5
    top = max(0, selected_idx - max_rows + 1) if selected_idx >= max_rows else 0

    for i, p in enumerate(procs[top:top + max_rows]):
        row = 4 + i
        idx = top + i
        line = (f"{p['pid']:>7}  {p['name'][:20]:<20}  "
                f"{p['cpu']:>6.1f}%  {p['mem_kb']/1024:>8.1f}  {p['mem_pct']:>5.1f}%")
        attr = curses.A_REVERSE if idx == selected_idx else curses.A_NORMAL
        try:
            stdscr.addstr(row, 0, line[:width - 1], attr)
        except curses.error:
            pass

    if message:
        try:
            stdscr.addstr(height - 1, 0, message[:width - 1], curses.A_BOLD)
        except curses.error:
            pass

    stdscr.refresh()


def main(stdscr):
    curses.curs_set(0)
    stdscr.nodelay(True)
    stdscr.timeout(REFRESH_MS)

    prev_times = {}
    prev_wall = None
    selected_idx = 0
    message = ""
    procs = []

    while True:
        procs, prev_times, prev_wall = sample_processes(prev_times, prev_wall)
        procs.sort(key=lambda p: p["cpu"], reverse=True)
        total_count = len(procs)
        selected_idx = max(0, min(selected_idx, len(procs) - 1)) if procs else 0

        draw(stdscr, procs, selected_idx, total_count, message)
        message = ""

        key = stdscr.getch()
        if key == ord('q'):
            break
        elif key == curses.KEY_UP:
            selected_idx = max(0, selected_idx - 1)
        elif key == curses.KEY_DOWN:
            selected_idx = min(len(procs) - 1, selected_idx + 1) if procs else 0
        elif key == ord('k'):
            if procs:
                target = procs[selected_idx]
                try:
                    os.kill(target["pid"], signal.SIGTERM)
                    message = f"Sent SIGTERM to '{target['name']}' (PID {target['pid']})"
                except ProcessLookupError:
                    message = f"PID {target['pid']} no longer exists"
                except PermissionError:
                    message = f"Permission denied to kill PID {target['pid']}"


if __name__ == "__main__":
    curses.wrapper(main)
