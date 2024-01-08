#lang racket/gui

(require racket/gui/base)

(define frame (new frame% [label "Window Title"]))

(define msg (new message% [parent frame]
						  [label "message body..."]))

(new button% [parent frame]
			 [label "button before click"]
			 ;; callback is executed on button click
			 [callback (lambda (button event)
			 				(send button set-label "button after click"))])

(send frame show #t)

#|

Notes:
frame is a equivalent to a application window as we can see when we send it to
the display, the application name is the same as the label of the frame

message seems to be just a text block and we can set the parent to the frame
that is going to be displayed to make it show up in the display

button is an object that has a 'callback' block of code that is executed when 
the button is clicked, it's parent is also the frame so it is displayed

|#