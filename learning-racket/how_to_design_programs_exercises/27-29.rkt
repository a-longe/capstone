#lang racket

;; Andres mentioned the idea of creating a graphing function
;; so lets try that out

;; Procedure -> Image
;; given an procedure with one argument (x)
;; creates an image black screen with white
;; pixels at coordinates that corespond to the procedure
;; Procedure must return a number
(require 2htdp/image)
(define (num-func->img proc size)
  (for/fold ([img (rectangle size size "solid" "gray")])
            ([x-value (in-range (* (quotient size 2) -1) (quotient size 2) 0.1)])
    (place-image (square 2 "solid" "black")
                 (+ x-value (quotient size 2))
                 (+ (* (proc x-value) -1) (quotient size 2))
                 img)
    ))

(define (disp x)
  (abs x))

;; NOTES after completing:
;; probably the 'nicer' way of doing it is by recursion where the
;; result of the previous is passed into the next recusion but
;; using rackets build in way of storing state between loops seemed easier

;; 27
(define (avg-attendance price)
  (- 120 (* (/ price 0.10) 15)))

(define (revenue price)
  (* (avg-attendance price) price))

(define (cost price)
  (+ 180 (* 0.04 (avg-attendance price))))

(define (profit price)
  (- (revenue price)
     (cost price)))


(num-func->img profit 400)

