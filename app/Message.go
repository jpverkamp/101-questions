package main

import (
    "time"
)

type Message struct {
    Date time.Time
    Author User
    Text string
    Responses []Message
}
