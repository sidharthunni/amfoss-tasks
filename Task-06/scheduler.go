package main

import (
	"bufio"
	"fmt"
	"os"
	"sort"
)

type Process struct {
	ID          string
	Arrival     int
	Burst       int
	Remaining   int
	Start       int
	Finish      int
	Waiting     int
	Turnaround  int
}

type Segment struct {
	ID    string
	Start int
	End   int
}

func printGantt(segments []Segment) {
	fmt.Println("\nGantt Chart:")
	for _, s := range segments {
		fmt.Printf("| %-4s ", s.ID)
	}
	fmt.Println("|")
	fmt.Printf("%d", segments[0].Start)
	for _, s := range segments {
		fmt.Printf("%7d", s.End)
	}
	fmt.Println()
}

func printResults(procs []Process) {
	fmt.Println("\nID\tArrival\tBurst\tWaiting\tTurnaround")
	totalWT, totalTAT := 0, 0
	for _, p := range procs {
		fmt.Printf("%s\t%d\t%d\t%d\t%d\n", p.ID, p.Arrival, p.Burst, p.Waiting, p.Turnaround)
		totalWT += p.Waiting
		totalTAT += p.Turnaround
	}
	n := len(procs)
	fmt.Printf("\nAverage Waiting Time: %.2f\n", float64(totalWT)/float64(n))
	fmt.Printf("Average Turnaround Time: %.2f\n", float64(totalTAT)/float64(n))
}

func fcfs(procs []Process) {
	sort.Slice(procs, func(i, j int) bool { return procs[i].Arrival < procs[j].Arrival })
	time := 0
	var segments []Segment
	for i := range procs {
		if time < procs[i].Arrival {
			time = procs[i].Arrival
		}
		start := time
		time += procs[i].Burst
		procs[i].Finish = time
		procs[i].Turnaround = procs[i].Finish - procs[i].Arrival
		procs[i].Waiting = procs[i].Turnaround - procs[i].Burst
		segments = append(segments, Segment{procs[i].ID, start, time})
	}
	printGantt(segments)
	printResults(procs)
}

func sjf(procs []Process) {
	n := len(procs)
	completed := make([]bool, n)
	time := 0
	done := 0
	var segments []Segment

	for done < n {
		idx := -1
		for i := 0; i < n; i++ {
			if !completed[i] && procs[i].Arrival <= time {
				if idx == -1 || procs[i].Burst < procs[idx].Burst {
					idx = i
				}
			}
		}
		if idx == -1 {
			time++
			continue
		}
		start := time
		time += procs[idx].Burst
		procs[idx].Finish = time
		procs[idx].Turnaround = procs[idx].Finish - procs[idx].Arrival
		procs[idx].Waiting = procs[idx].Turnaround - procs[idx].Burst
		completed[idx] = true
		done++
		segments = append(segments, Segment{procs[idx].ID, start, time})
	}
	printGantt(segments)
	printResults(procs)
}

func roundRobin(procs []Process, quantum int) {
	n := len(procs)
	for i := range procs {
		procs[i].Remaining = procs[i].Burst
	}
	sort.Slice(procs, func(i, j int) bool { return procs[i].Arrival < procs[j].Arrival })

	queue := []int{}
	inQueue := make([]bool, n)
	time := 0
	done := 0
	var segments []Segment

	// start with processes that have arrived at time 0
	for i := 0; i < n; i++ {
		if procs[i].Arrival <= time {
			queue = append(queue, i)
			inQueue[i] = true
		}
	}

	for done < n {
		if len(queue) == 0 {
			time++
			for i := 0; i < n; i++ {
				if !inQueue[i] && procs[i].Remaining > 0 && procs[i].Arrival <= time {
					queue = append(queue, i)
					inQueue[i] = true
				}
			}
			continue
		}
		idx := queue[0]
		queue = queue[1:]

		run := quantum
		if procs[idx].Remaining < quantum {
			run = procs[idx].Remaining
		}
		start := time
		time += run
		procs[idx].Remaining -= run
		segments = append(segments, Segment{procs[idx].ID, start, time})

		// enqueue any newly arrived processes during this run
		for i := 0; i < n; i++ {
			if !inQueue[i] && procs[i].Remaining > 0 && procs[i].Arrival <= time && i != idx {
				queue = append(queue, i)
				inQueue[i] = true
			}
		}

		if procs[idx].Remaining > 0 {
			queue = append(queue, idx)
		} else {
			procs[idx].Finish = time
			procs[idx].Turnaround = procs[idx].Finish - procs[idx].Arrival
			procs[idx].Waiting = procs[idx].Turnaround - procs[idx].Burst
			inQueue[idx] = false
			done++
		}
	}
	printGantt(segments)
	printResults(procs)
}

func main() {
	reader := bufio.NewReader(os.Stdin)

	fmt.Print("Number of processes: ")
	var n int
	fmt.Fscan(reader, &n)

	procs := make([]Process, n)
	for i := 0; i < n; i++ {
		fmt.Printf("Process %d - ID Arrival Burst: ", i+1)
		fmt.Fscan(reader, &procs[i].ID, &procs[i].Arrival, &procs[i].Burst)
	}

	fmt.Println("\nChoose algorithm: 1) FCFS  2) SJF  3) Round Robin")
	var choice int
	fmt.Fscan(reader, &choice)

	switch choice {
	case 1:
		fcfs(procs)
	case 2:
		sjf(procs)
	case 3:
		fmt.Print("Time Quantum: ")
		var q int
		fmt.Fscan(reader, &q)
		roundRobin(procs, q)
	default:
		fmt.Println("Invalid choice")
	}
}
