#lang racket

;; Andres mentioned the idea of creating a graphing function
;; so lets try that out
(require 2htdp/image)
(define polls 0.1)
;; Number -> Image
;; Slope is a Number
;; Using the slope, create a line with given slope
;; at the give coordinates
(define (slope->img slope)
  (add-line (empty-scene polls (abs slope))
            0 0
            polls slope
            "black"))

;; Procedure -> Image
;; given an procedure with one argument (x)
;; creates an image black screen with white
;; pixels at coordinates that correspond to the procedure
;; Procedure must return a number
(define (num-func->img func size)
  (for/fold ([img (rectangle size size "solid" "gray")])
            ([x-value (in-range (* (quotient size 2) -1) (quotient size 2) polls)])
    (place-image (slope->img (/ (- (func (+ x-value polls)) (func x-value)) polls))
                 (+ x-value (quotient size 2))
                 (+ (* (func x-value) -1) (quotient size 2))
                 img)
    ))

(define (disp x)
  (expt (* 2 x) 2))

;; NOTES after completing:
;; probably the 'nicer' way of doing it is by some recursion where the
;; result of the previous is passed into the next recusion but
;; using rackets build in way of storing state between loops seemed easier

(define BASE-ATTENDIES 120)
(define BASE-PRICE 5)
(define CHANGE-PRICE 0.1)
(define CHANGE-PEOPLE 15)

(define BASE-COST 180)
(define COST-PER-PERSON 1.50)

(define (avg-attendance price)
  (- BASE-ATTENDIES (* (- price BASE-PRICE) (/ CHANGE-PEOPLE CHANGE-PRICE))))

(define (revenue price)
  (* (avg-attendance price) price))

(define (cost price)
  (* COST-PER-PERSON (avg-attendance price)))
;;(define (cost price)
;;  (+ BASE-COST (* COST-PER-PERSON (avg-attendance price))))

(define (profit price)
  (- (revenue price)
     (cost price)))

;; 27
;; refactor the code so that all 'magic' numbers are
;; changed into global constants


;; 28
;; Find the most profitable ticket price 1, 2, 3, 4, 5

(profit 1)
(profit 2)
(profit 3)
(profit 4)
(profit 5)

;; Results:
;;511.2
;;937.2
;;1063.2
;;889.2
;;415.2
;; 3 is the most proitable

;; 29
;; cost equasion has changed, there is no longer a fixed cost
;; only 1.50$ per person, ow does this change profitability?

;; -360.0
;; 285.0
;; 630.0
;; 675.0
;; 420.0

;; Now the most profitable ticket option is 4$

(num-func->img profit 400)

