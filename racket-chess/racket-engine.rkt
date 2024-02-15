#lang racket

(define (divmod num divisor)
  (define div (quotient num divisor))
  (define mod (modulo num divisor))
  (values div mod)
)

(divmod 7 8)
(divmod 8 8)
(divmod 9 8)
