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

	for {
		line, err := scanner.ReadString('\n')
		if err != nil {
			log.Fatal(err)
		}
		if strings.Contains(line, "1-0:1.7.0") {
			kwUsage := strings.Split(strings.Split(line, "(")[1], "*")[0]
			fmt.Println(kwUsage)
		}
	}
}
