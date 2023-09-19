#lang scheme

(display "Hello World\n")

(define name "Jane")
(string-append "hello " name "!")

(define (greet name)
    (string-append "hello " name "!"))

(greet "Bill")

((lambda (name) 
    (string-append "hello " name "!")) "Bob")

(let ((name "John")) ; why two sets of brackets
    (string-append "hello " name "!"))

(apply + '(1 2 3 4 5 6))

(define (chatty-add chatty-name nums)
    (format "<~a> If you add those numbers together you get ~a! \n"
        chatty-name (apply + nums)))

(chatty-add "Mack" '(1 3 5))


(define (shopkeeper thing-to-buy
                    [how-many 1]
                    (cost 20)
                    #:shopkeeper [shopkeeper "Sammy"]
                    (store "Plentiful Great Produce"))
  (display (format "You walk into ~s, grab something from the shelves,\n"
                   store))
  (display "and walk up to the counter.\n\n")
  (display (format "~a looks at you and says, "
                   shopkeeper))
  (display (format "'~a ~a, eh? That'll be ~a coins!'\n"
                   how-many thing-to-buy
                   (* cost how-many))))



;; access optional arguments in this form "#:<key> <value>"
(shopkeeper "shoes" 2 199)

(string? "apple")
(string? 128)
(string? '("apple" "bannana" "orange"))

(define (oh-man-do-i-love-strings obj)
    (if (string? obj) 
        (display "oh boy do i love strings \n")
        (display "ew yuck gross \n")))

(oh-man-do-i-love-strings "i love strings")
(oh-man-do-i-love-strings '(1 2 3))

;; return multiple values from one function
(define (add-and-multiply x y)
    (values (+ x y)(* x y)))

(define-values (added multiplied)
    (add-and-multiply 3 10))

;; Conditionals

(> 8 9) ; is 8 greater than 9? = f
(< 8 9) ; is 8 less than 9? = t
(> 8 8) ; is 8 greater than 8? = f
(>= 8 8) ; is 8 greater than or equal to 8? = t

;; goldilocks program that checks if one number is in between two other numbers
(define (goldilocks num largest smallest)
    (if (< num smallest)
        "too small!"
        (if (> num largest)
            "too big!"
            "just right!")))

;; instead of using if statements try using the condition block
;;(cond (<#t or #f> <BODY>) [(else <BODY>)])

(define (new-goldilocks num largest smallest)
    (cond ((< num smallest) 
    "too small")
    [else (cond ((> num largest)
                "too big")
                [else "just right"])]))

;; eq? vs equal?
#|
    eq? - eq? compares the identitiy of the two objects provided
    as in are they the same object by name (var1 == var1)

    equal? - compares the content of the two abjects as in are they
    equivilant (2 == 2)
|#
(define a-list '(1 2 3))
(define b-list '(1 2 3))
(equal? a-list a-list) ; ==> #t
(eq? a-list a-list) ; ==> #t
(equal? a-list b-list) ; ==> #t
(eq? a-list b-list) ; ==> #f