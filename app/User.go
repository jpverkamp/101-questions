package main

type User struct {
    Email string
    Name string
    Password string
    Friends []User
    QuestionSets []QuestionSet
    QuestionRuns []QuestionRun
}
