#lang racket

(require 2htdp/image)





; rocket hyper variables

(define (half x) (/ x 2))

(define WIDTH 100)

(define HEIGHT 200)

(define Velo 2)

(define x 50)

(define grass-height 20)

(define new-scene (place-image

                   (rectangle WIDTH grass-height "solid" "green") (half WIDTH) (- HEIGHT (half grass-height)); grass

                   (place-image

                    (rectangle WIDTH HEIGHT "solid" "light blue") (half WIDTH) (half HEIGHT); sky

                    (empty-scene WIDTH HEIGHT)))) ; short for empty scene

(define ROCKET (overlay

             (circle 10 "solid" "green")

             (circle 10 "solid" "green")))

(define UFO (overlay

             (circle 10 "solid" "green")

             (circle 10 "solid" "green")))



(define y-threshold

  (- (- HEIGHT (half(image-height ROCKET))) grass-height))



; ARITHMATIC AND ARITHMATIC

(string-append "hello" "world")

(string-append "hello" " " "world")

(define bool-operators (list (and #true #true)(and #true #false)(or #true #false)(or #false #false)(not #false) (not #true)))

(for-each (lambda (arg)(printf "Got ~a\n" arg)23) bool-operators)

(define (longer-string? word1 word2)

  (if (> (string-length word1) (string-length word2))

      (printf "true") ; if true

      (printf("false")))) ; else



(if (= (*(image-width ROCKET)(image-height ROCKET)) 1176)

    (printf "test immage as expected\n"); if true

    (printf "incorrect image!")) ; else

ROCKET ; evaluate line "ROCKET" becomes an image



(circle 15 "solid" "white")

(rectangle 30 30 "solid" "lime")

(overlay (circle 15 "solid" "black")

         (rectangle 30 30 "solid" "white"))



(empty-scene 10 10) ; blank white square



(define (place-on-empty-scene x y)(place-image

                                   (rectangle 10 10 "solid" "black"); image being placed

                                   x y ; @ cords (relative?)

                                   (empty-scene 100 100))); on top of image <--

(place-on-empty-scene 50 50)





(define sunny #true)

(define friday #false)



;; dont  do (or (equal? sunny #false)(equal? friday #true))

(or (not sunny) friday)



; INPUT AND OUTPUT

(define (square x)

  (* x x))



(square 2)

(square 4)

(square 5)

(square 6)



(place-image ROCKET 50 50 (empty-scene 100 80))



(define (image-of-rocket-v1 y)

  (place-image ROCKET 50 y (empty-scene 100 80)))



(image-of-rocket-v1 10)

(image-of-rocket-v1 20)

(image-of-rocket-v1 30)

(image-of-rocket-v1 40)

(image-of-rocket-v1 50)



(require 2htdp/universe)



;(printf "V1: ")

;(animate image-of-rocket-v1)



(define (image-of-rocket-v2 y)

  (cond

    [(<= y 80)

     (place-image ROCKET 50 y

                  (empty-scene 100 80))]

    [(> y 80)

     (place-image ROCKET 50 80

                  (empty-scene 100 80))]))



;(printf "V2: ")

;(animate image-of-rocket-v2)



(define (image-of-rocket-v3 y)

  (let ([y-threshold (- 80 (/(image-height ROCKET) 2))])

    (cond

      [(<= y y-threshold)

       (place-image ROCKET 50 y

                    (empty-scene 100 80))]

      [(> y y-threshold)

       (place-image ROCKET 50 (- 80 (/(image-height ROCKET) 2))

                    (empty-scene 100 80))])))



;(printf "V3: ")

;(animate image-of-rocket-v3)



; ONE PROGRAM MANY DEFINITIONS

;(define WIDTH 100) see top of program

;(define HEIGHT 400) see top of program



(define (image-of-rocket-v4 y)

  (let ([y-threshold (- HEIGHT (/(image-height ROCKET) 2))])

    (cond

      [(<= y y-threshold)

       (place-image ROCKET (/ WIDTH 2) y

                    (empty-scene WIDTH HEIGHT))]

      [(> y y-threshold)

       (place-image ROCKET (/ WIDTH 2) y-threshold

                    (empty-scene WIDTH HEIGHT))])))



;(printf "V4: ")

;(animate image-of-rocket-v4)





(define (image-of-rocket-v5 y)

  (cond

    [(<= y y-threshold)

     (place-image ROCKET x y new-scene)]

    [(> y y-threshold)

     (place-image ROCKET x y-threshold new-scene)]))



;(printf "V5: ")

;(animate image-of-rocket-v5)



; QUICK LOOPS TEST

(define max 1000000); 1 million

(for ([counter max])

  (when (= counter (- max 1))(printf "~a\n" counter)))



#|ONE MORE DEFINITION



add velocity and an x cord to hyper variables because the animate function passes the TIME to

image of a rocket and not the acctual hight - a phisics no no|#



(define (distance time) (* Velo time)) ; d = V * t



(define (image-of-rocket-v6 time)

  (cond

    [(<= (distance time) y-threshold)

     (place-image ROCKET x (distance time) new-scene)]

    [(> (distance time) y-threshold)

     (place-image ROCKET x y-threshold new-scene)]))



;(printf "V6: ")

;(animate image-of-rocket-v6)



#|YOU ARE A PROGRAMMER NOW... NOT!

just because you understand the basics of a language dosnt mean you are a

programmer. The important thing to learn is the conventions, or the 'right'

way to program. THat is what the rest of this book will be about|#



#|1 ARITHMATIC|#

(if (= 1 2)(printf "1 is = to ~a" 2)(printf "1 is not = to ~a\n" 2)) ; if((arg:bool) (if true) (else))

; lets write a test so when you try find the inverse of a number, test to make sure you dont divide by 0

(define (inverse x)

  (if (= x 0) 0

  (/ 1 x)))



(inverse 0)



; string arithmatic

(string=? "green" "red")

(string=? "red" "green")

(string<=? "green" "red")

(string<=? "red" "green")

(string>=? "green" "red")

(string>=? "red" "green")

; string<=? and string>=? checks if the string are ordered alphabeticaly

(define CAT (overlay

             (circle 10 "solid" "green")

             (circle 10 "solid" "green")))



(define (picture-orientation image) (if (>= (image-height image)(image-width image))

                                        (if (= (image-height image)(image-width image))

                                            "square" ; if true^

                                            "tall"); else

                                  #|^true|# "wide"))



; KNOW THY DATA

(define (get-value input)

  (cond

    [(number? input) (abs input)];number

    [(string? input) (string-length input)];string

    [(image? input) (*(image-width input)(image-height input))];image

    [(boolean? input) (if (eq? input #t) 10 20)];bool

    )

  )





#|2 FUNCTIONS AND PROGRAMS|#



(define (cube-volume length)

  (expt length 3))

(cube-volume 3)



;(define (string-first str)

  ;(first(string->list str)))





(define (string-last str)

  (last(string->list str)))



(string-last "hello world")



(define(dist-from-origin x y)

  (sqrt (+ (sqr x)(sqr y))))



(dist-from-origin 3 4)

;; could return to this unit later



#|2.2 COMPUTING|#



;better way to do string-first

(define (string-first s)

  (substring s 0 1))



(string-first "hello world")



(define (string-insert base new i)

  (string-append (substring base 0 i)

                 new

                 (substring base i)))

 

(string-insert "helloworld" "_" 5)



#|2.3 Composing Functions|#

; this is more complicated applications of functions, as in files where

; the task is large enough to be broken down into smaller functions.





;;------------------------------------------------------------------------------------------

; as an example, here's a set of functions that calculate the ticket profits by calculating

; revenue and costs, then subtracting





; HYPER VARIABLES

(define BASE-ATTENDANCE 120)

(define BASE-PRICE 5.0)

(define PRICE-CHANGE 0.1)

(define PEOPLE-LOST-PER-CHANGE 15)

(define BASE-COST 180)

(define COST-PER-PERSON 0.04)



; first find # of atendees with the ticket cost

(define (attendees price)

  (- BASE-ATTENDANCE (*(/ (- price BASE-PRICE) PRICE-CHANGE) PEOPLE-LOST-PER-CHANGE)))

(attendees 5)

(attendees 5.10)

(attendees 4.90)



; find how much money a price of ticket would return

(define (revenue price )

  (* price (attendees price)))



; find how much it would cost to host that many people

(define (cost price)

  (+ BASE-COST (* COST-PER-PERSON (attendees price))))



; main function, ties it together

(define (profit price)

  (- (revenue price)

     (cost price)))



(profit 1)

(profit 2)

(profit 3) ; <- most profitable

(profit 4)

(profit 5)



(set! BASE-COST 0)

(set! COST-PER-PERSON 1.5)



(profit 3)

(profit 4) ; <- most profitable

(profit 5)



(set! BASE-COST 180)

(set! COST-PER-PERSON 0.04)



#|2.4 GLOBAL CONSTANTS|#

; Already talked about this in every unit above



#|2.5 PROGRAMS|#



; farenhieght to celcius converter

(define (celcius f)

  (* 5/9 (- f 32)))



(celcius 32)

(celcius 212)

(celcius -40)



#|------------------------------------------------------------------

SIDE TOPIC - IRRATIONAL NUMBERS AND PROOF THAT SQRT(2) is irrational

-rational numbers are numbers that can be repersented by a fraction (1.5 = 3/2)

-irrarional numbers are numbers that cannot be repersented by a fraction (for example pi is one of the most famous irrational number and cannot be repersented by a fraction though

 22/7 is the most popular APROXIMATION)

- Pi is proven to be irrational in the 1760s using the tan() function which is an irrational

function or a continued fraction (which means that the fraction contains another fraction as the denominatior of the previous one that continues on forever)

and since the tangent of pi/4 = 1 that must mean that pi/4 is irrational too



- proof sqrt(2) is irrational

ok this is kind of hard to put into words but assume that √2 is rational, that means we would

be able to repersent it in a fraction a/b and lets make sure that fraction is in lowest terms

theirfor: √2 = a/b

ok great, now lets isolate 2,

2 = a^2/b^2

and better yet:

a^2 = 2 * b^2

theirfor: a is an even number

ok so a is even whick means some number * 2 = a, lets call that number c

2 = (2c)^2/b^2

2 = 4c^2/b^2

2*b^2 = 4c^2

b^2 = 2c^2

theirfor: b is also even? that definatly means that the original fraction a/b is not is lowest terms because both a and b are even

and thus the whole fraction is divisable by two

This is a Contradiction of the original assumption (√2 is rational) so that means

our assumption is not true so √2 is irratonal

------------------------------------------------------------------|#


#|2.5 PROGRAMS|#

#|batch vs interactive program:
batch - consumes all inputs and generates a result, the oporating system call the program, gives it it's inputs and wait for a result
interacctive - consumes some inputs, generates a result then waits for more input the produces and output and so on|#

(require 2htdp/batch-io)


(write-file "sample.dat" "212")
(read-file "sample.dat")

(write-file 'stdout "212\n") ; the printed result of this line (212\n'stdout) does not have quotes around the 212 because of the token 'stdout


(define (F-to-C-from-file in out)
  (write-file out ; write string to the file out
              (string-append
               (number->string ; change C number to string
               (celcius ; convert F number to C number
                (string->number ; convert string to number
                 (read-file in)))); take string input from file
               "\n"); add \newline char after each pass of program to differntiate the results from each other
  ) 
)

;; lets test the above program
(write-file "sample.dat" "212")
(F-to-C-from-file "sample.dat" 'stdout)
(F-to-C-from-file "sample.dat" "out.dat")
(read-file "out.dat")


(require 2htdp/universe)

(define (number->square i)
  (rectangle i i "solid" "red"))

(number->square 5)
(number->square 10)
(number->square 20)

;;(big-bang 100 (to-draw number->square))

(define (reset s key) 100)

;;(big-bang 100
  ;;[to-draw number->square]
  ;;[on-tick sub1]
  ;;[stop-when zero?]
  ;;[on-key reset])

(define BACKGROUND (empty-scene 100 100))
(define DOT (circle 3 "solid" "red"))
 
(define (main y)
  (big-bang y
    [on-tick sub1]
    [stop-when zero?]
    [to-draw place-dot-at]
    [on-key stop]))
 
(define (place-dot-at y)
  (place-image DOT 50 y BACKGROUND))
 
(define (stop y ke)
  0)
