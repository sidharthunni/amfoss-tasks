# Task 06: Pirate King's Scheduler

A CPU scheduling simulator in Go implementing FCFS, SJF (non-preemptive),
and Round Robin. Takes process ID, arrival time, and burst time as input
(plus time quantum for RR), then prints a Gantt chart and calculates
waiting time, turnaround time, and their averages.

## Approach

- **FCFS**: sort processes by arrival time, run them strictly in that
  order, tracking when the CPU becomes free.
- **SJF (non-preemptive)**: at each point the CPU is free, look at all
  processes that have arrived but haven't run yet, and pick the one
  with the smallest burst time. Once picked, it runs to completion.
- **Round Robin**: maintain a queue of arrived processes. Each process
  runs for at most one time quantum; if it still has remaining burst
  time, it goes back to the end of the queue. Newly arrived processes
  are added to the queue as time passes.
- All three compute Waiting Time = Turnaround Time - Burst Time, and
  Turnaround Time = Finish Time - Arrival Time, then average both
  across all processes.

## How to run

    go run scheduler.go

Follow the prompts: number of processes, then ID/arrival/burst for
each, then pick 1 (FCFS), 2 (SJF), or 3 (Round Robin - also asks for
time quantum).

## Resources used
- https://go.dev/tour/list (Go tour, slices reference)
- Go documentation for bufio and fmt packages for input handling

## Concepts learned
- Go slices and how they grow/shrink (used heavily for the RR queue)
- Struct usage in Go and passing slices of structs to functions
- Basic CPU scheduling algorithms and how waiting/turnaround time are
  derived from arrival, burst, and finish times
- Simulating a time-stepped queue (Round Robin) versus event-driven
  simulation (FCFS/SJF)

## Review
## Review
This one was pretty confusing at first, especially figuring out how
Round Robin should handle newly arriving processes while also cycling
through the queue. Once it clicked though, it made a lot more sense.
The biggest things I picked up were how waiting time and turnaround
time are actually calculated from just arrival, burst, and finish
times, and how differently each algorithm decides "what runs next" -
FCFS just goes by arrival order, SJF looks at burst time, and Round
Robin is really just a queue with a time limit per turn. Also got more
comfortable with Go slices and structs along the way.
