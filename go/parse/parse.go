package main

import (
	"bufio"
	"fmt"
	"log"
	"os"
	"strings"
)

func main() {
	scanner := bufio.NewReader(os.Stdin)

	var timestamp string
	for {
		line, err := scanner.ReadString('\n')
		if err != nil {
			log.Fatal(err)
		}
		if strings.Contains(line, "0-0:1.0.0") {
			timestamp = strings.Split(line, "(")[1][:12]
		} else if strings.Contains(line, "1-0:1.7.0") {
			kwUsage := strings.Split(strings.Split(line, "(")[1], "*")[0]
			fmt.Printf("%s, %s\n", timestamp, kwUsage)
		}
	}
}
