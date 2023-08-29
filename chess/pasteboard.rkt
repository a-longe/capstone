#lang racket/gui
(define chess-piece-width 50)
(define chess-piece-height 50)

;; chess piece snip class
(define chess-piece-snip-class
  (make-object
      (class snip-class%
        (super-new)
        (send this set-classname "chess-piece-snip"))))
;; register class above with racket gui
(send (get-the-snip-class-list) add chess-piece-snip-class)