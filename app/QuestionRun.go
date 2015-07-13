package main

import (
    "time"
)

type QuestionRun struct {
    ID string
    Targets []User
    Date time.Time
    Frequency string
    CurrentQuestion int
    Threads []Message
}
