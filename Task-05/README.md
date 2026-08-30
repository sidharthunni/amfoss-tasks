# Task 05: Grand Line Guardian

A terminal-based system monitor (like htop/btop++) that reads process
data directly from /proc — no psutil, no third-party library.
Every running process is a "ship"; this tool is the navigator's live radar
over the Grand Line (your machine).

## Features
- Live table of every process: PID, Name, CPU%, Memory%
- Total active process count shown in the header
- Refreshes every 500ms (< 1s, as required)
- Keyboard navigation: UP/DOWN to move the selection
- Terminate a troublesome ship: k (sends SIGTERM)
- q to quit

## Setup and Run
No external packages are needed — everything uses the Python standard library.
Run it with: python3 monitor.py

## My Approach
I parsed the /proc virtual filesystem by hand instead of using a library
like psutil, since the task specifically asks for an understanding of
the Linux kernel interface.

1. Listing processes: /proc contains one directory per running process,
   named after its PID. Filtering os.listdir("/proc") for numeric entries
   gives the live process list.
2. Name and CPU time (/proc/[pid]/stat): the process name sits inside
   parentheses and can contain spaces, so I split on the LAST close-paren
   to avoid corrupting the parse. Fields 14 and 15 are utime and stime,
   the CPU ticks spent in user mode and kernel mode.
3. CPU% is a rate, not a snapshot: it's derived from two time-stamped
   samples: cpu percent = 100 times (delta ticks divided by CLK_TCK)
   divided by elapsed seconds.
4. Memory (/proc/[pid]/status): the VmRSS line gives resident memory in
   KB; dividing by system MemTotal from /proc/meminfo gives MEM%.
5. Rendering with curses: handles raw terminal drawing and non-blocking
   key input, with a 500ms timeout driving the refresh loop.
6. Safety: every read is wrapped in try/except since a process can exit
   between being listed and being read.

## Concepts Learned
- procfs (/proc) is generated on the fly by the kernel, not a real disk
  filesystem — this is how ps, top, and htop get their data.
- CPU accounting uses ticks, not seconds — SC_CLK_TCK converts them.
- The stat file format is positional; the process-name field is the only
  variable-content field, so it needs careful parsing.
- VmRSS (actual RAM in use) vs virtual memory a process has reserved.
- Signals: SIGTERM politely asks a process to exit, vs a hard SIGKILL.
- Non-blocking terminal input via curses timeouts, without threads.

## Resources Used
- man proc: Linux manual page for the /proc filesystem
- Python curses official docs
- Python os module docs (os.sysconf)
- htop behavior as a UX reference
