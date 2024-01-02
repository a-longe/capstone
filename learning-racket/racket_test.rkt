#lang racket

(define billion 1000000000)
(for ([i billion])
  (+ i 1))
(display "Done!")