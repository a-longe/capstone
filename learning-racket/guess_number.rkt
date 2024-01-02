#lang racket

(define (inquire-user number)
  (display "Insert a number: ")
  (define guess (string->number (read-line)))
  (cond [(> number guess) (displayln "Too low") (inquire-user number)]
        [(< number guess) (displayln "Too high") (inquire-user number)]
        [else (displayln "Correct!")]
  )
)