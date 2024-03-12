#lang racket

(require rackunit)

; WorldState -> WorldState
; Increments the given value by three,
; to be called every clock tick
(define (tock x) 
  (+ x 3))

(check-eq? (tock 23) 24 "tock func does not increment by 3")
