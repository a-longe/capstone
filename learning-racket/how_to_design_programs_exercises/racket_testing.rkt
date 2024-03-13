#lang racket

(require rackunit)

; WorldState -> WorldState
; Increments the given value by three,
; to be called every clock tick
(define (tock x) 
  (+ x 3))

(define (a-check input expected msg)
  (cond
    [(equal? input expected) (display ".")]
    [else (check-eq? input expected msg)])
)

(a-check (tock 23) 24 "will return false")
(a-check (tock 23) 26 "will return true")
(a-check (tock 23) 26 "will return true")
(a-check (tock 23) 26 "will return true")
(a-check (tock 23) 26 "will return true")

;(check-eq? (tock 23) 24 "tock func does not increment by 3")
