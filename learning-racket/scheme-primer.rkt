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