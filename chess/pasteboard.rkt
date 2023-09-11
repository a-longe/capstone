#lang racket/gui
(require embedded-gui)

(define chess-piece-snip-class
  (make-object
   (class snip-class%
     (super-new)
     (send this set-classname "chess-piece-snip"))))

(send (get-the-snip-class-list) add chess-piece-snip-class)

(define chess-piece%
  (class snip%
    (init-field name glyph font size moves [location #f])
    (super-new)
    (send this set-snipclass chess-piece-snip-class)

    (define/public (set-location l) (set! location l))
    (define/public (get-location) location)
    (define/public (color)
      (if (equal? (string-upcase name) name) 'white 'black))
    (define/public (valid-moves)
      (let ((admin (send this get-admin)))
        (if (and admin location)        ; can be #f is the snip is not owned
            (let ((board (send admin get-editor)))
              (moves board location))
            ;; Return an empty list if this piece is not on a board
            '())))

    (define/override (get-extent dc x y width height descent space lspace rspace)
      (when width (set-box! width size))
      (when height (set-box! height size))
      (when descent (set-box! descent 0.0))
      (when space (set-box! space 0.0))
      (when lspace (set-box! lspace 0.0))
      (when rspace (set-box! rspace 0.0)))

    (define/override (draw dc x y . other)
      (send dc set-font font)
      (send dc set-text-foreground "black")
      (define-values (glyph-width glyph-height baseline extra-space)
        (send dc get-text-extent glyph font #t))
      (let ((ox (/ (- size glyph-width) 2))
            (oy (/ (- size glyph-height 2))))
        (send dc draw-text glyph (+ x ox) (+ y oy))))
    ))

(define (valid-rank? rank) (and (>= rank 0) (< rank 8)))
(define (valid-file? file) (and (>= file 0) (< file 8)))

(define ((pawn-moves color) board location)
  (define direction (if (eq? color 'white) -1 1))
  (define-values (rank file) (location->rank-file location))
  (define moves '())
  (when (valid-rank? (+ rank direction))
    ;; can move forward if that square is not occupied
    (let ((candidate (rank-file->location (+ rank direction) file)))
      (unless (piece-at-location board candidate)
        (set! moves (cons candidate moves))
        (when (valid-rank? (+ rank direction direction))
          ;; can move two squares forward if the pawn is in its original location
          (when (or (and (eq? color 'white) (equal? rank 6))
                    (and (eq? color 'black) (equal? rank 1)))
            (let ((candidate (rank-file->location (+ rank direction direction) file)))
              (unless (piece-at-location board candidate)
                (set! moves (cons candidate moves))))))))
    ;; can move forward left if that square is occupied
    (when (valid-file? (sub1 file))
      (let ((candidate (rank-file->location (+ rank direction) (sub1 file))))
        (let ((piece (piece-at-location board candidate)))
          (when (and piece (not (eq? color (send piece color))))
            (set! moves (cons candidate moves))))))
    ;; can move forward right if that square is occupied
    (when (valid-file? (add1 file))
      (let ((candidate (rank-file->location (+ rank direction) (add1 file))))
        (let ((piece (piece-at-location board candidate)))
          (when (and piece (not (eq? color (send piece color))))
            (set! moves (cons candidate moves)))))))

  moves)

(define (valid-moves-by-offset color board location offsets)
  (define-values (rank file) (location->rank-file location))
  (for/fold ([moves '()])
            ([offset (in-list offsets)])
    (match-define (list roffset foffset) offset)
    (define-values (nrank nfile) (values (+ rank roffset) (+ file foffset)))
    (if (and (valid-rank? nrank) (valid-file? nfile))
        (let ((candidate (rank-file->location nrank nfile)))
          (let ((piece (piece-at-location board candidate)))
            (if (or (not piece) (not (eq? (send piece color) color)))
                (cons candidate moves)
                moves)))
        moves)))

(define (valid-moves-by-direction color board location rank-direction file-direction)
  (define-values (rank file) (location->rank-file location))
  (define moves '())
  (define (check rank file)
    (let ((candidate (rank-file->location rank file)))
      (let ((target-piece (piece-at-location board candidate)))
        (when (or (not target-piece) (not (eq? (send target-piece color) color)))
          (set! moves (cons candidate moves)))
        (if target-piece #f #t))))
  (let loop ((nrank (+ rank rank-direction))
             (nfile (+ file file-direction)))
    (when (and (valid-rank? nrank) (valid-file? nfile) (check nrank nfile))
      (loop (+ nrank rank-direction) (+ nfile file-direction))))
  moves)

(define ((knight-moves color) board location)
  (valid-moves-by-offset
   color board location
   '((-1 -2) (-1 2) (1 -2) (1 2) (-2 -1) (-2 1) (2 -1) (2 1))))

(define ((king-moves color) board location)
  (valid-moves-by-offset
   color board location
   '((-1 -1) (-1 0) (-1 1) (0 -1) (0 1) (1 -1) (1 0) (1 1))))

(define ((rook-moves color) board location)
  (append
   (valid-moves-by-direction color board location 1 0)
   (valid-moves-by-direction color board location -1 0)
   (valid-moves-by-direction color board location 0 1)
   (valid-moves-by-direction color board location 0 -1)))

(define ((bishop-moves color) board location)
  (append
   (valid-moves-by-direction color board location 1 1)
   (valid-moves-by-direction color board location -1 1)
   (valid-moves-by-direction color board location 1 -1)
   (valid-moves-by-direction color board location -1 -1)))

(define ((queen-moves color) board location)
  (append
   (valid-moves-by-direction color board location 1 0)
   (valid-moves-by-direction color board location -1 0)
   (valid-moves-by-direction color board location 0 1)
   (valid-moves-by-direction color board location 0 -1)
   (valid-moves-by-direction color board location 1 1)
   (valid-moves-by-direction color board location -1 1)
   (valid-moves-by-direction color board location 1 -1)
   (valid-moves-by-direction color board location -1 -1)))

(define chess-piece-data
  (hash
   "K" (cons #\u2654 (king-moves 'white))
   "Q" (cons #\u2655 (queen-moves 'white))
   "R" (cons #\u2656 (rook-moves 'white))
   "B" (cons #\u2657 (bishop-moves 'white))
   "N" (cons #\u2658 (knight-moves 'white))
   "P" (cons #\u2659 (pawn-moves 'white))
   "k" (cons #\u265A (king-moves 'black))
   "q" (cons #\u265B (queen-moves 'black))
   "r" (cons #\u265C (rook-moves 'black))
   "b" (cons #\u265D (bishop-moves 'black))
   "n" (cons #\u265E (knight-moves 'black))
   "p" (cons #\u265F (pawn-moves 'black))))

(define (make-chess-piece id [location #f])
  (match-define (cons glyph moves) (hash-ref chess-piece-data id))
  (define font (send the-font-list find-or-create-font 20 'default 'normal 'normal))
  (new chess-piece%
       [name id]
       [glyph (string glyph)]
       [font font]
       [size 35]
       [location location]
       [moves moves]))

(define chess-board%
  (class pasteboard%
    (super-new)

    (define drag-dx 0)
    (define drag-dy 0)
    (define highlight-location #f)
    (define valid-move-locations '())
    (define opponent-move-locations '())
    (define turn 'white)
    (define message #f)
    (define message-timer
      (new timer%
           [notify-callback (lambda ()
                              (set! message #f)
                              (send (send this get-canvas) refresh))]))

    (define (set-message m)
      (set! message m)
      (send message-timer start 2000)
      (send (send this get-canvas) refresh))

    (define/override (on-paint before? dc . other)
      (if before?
          (begin
            (draw-chess-board dc)
            (for ((location (in-list valid-move-locations)))
              (highlight-square dc location #f "seagreen"))
            (for ((location (in-list opponent-move-locations)))
              (highlight-square dc location "firebrick" #f))
            (when highlight-location
              (highlight-square dc highlight-location #f "indianred")))
          ;; message is drawn after the snips
          (when message
            (display-message dc message))))
    
    (define/augment (after-insert chess-piece . rest)
      (position-piece this chess-piece))
    
    (define/augment (on-display-size)
      (send this begin-edit-sequence)
      (let loop ([snip (send this find-first-snip)])
        (when snip
          ;; Reposition the piece, since the location is stored as text
          ;; (e.g. d3) its new coordinates will be recomputed to the correct
          ;; place
          (position-piece this snip)
          (loop (send snip next))))
      (send this end-edit-sequence))

    (define/augment (on-move-to snip x y dragging?)
      (when dragging?
        (let ((location (xy->location this (+ x drag-dx) (+ y drag-dy))))
          (unless (equal? highlight-location location)
            (set! highlight-location location)
            (send (send this get-canvas) refresh)))))

    (define/augment (can-interactive-move? event)
      (define piece (send this find-next-selected-snip #f))
      ;; The user tried to move a piece of the opposite color, remind them
      ;; again.
      (unless (eq? turn (send piece color))
        (set-message (format "It's ~a turn to move"
                      (if (eq? turn 'white) "white's" "black's"))))
      (eq? turn (send piece color)))

    (define/augment (on-interactive-move event)
      (define piece (send this find-next-selected-snip #f))
      (define-values (x y) (values (box 0) (box 0)))
      (send this get-snip-location piece x y #f)
      (set! drag-dx (- (send event get-x) (unbox x)))
      (set! drag-dy (- (send event get-y) (unbox y))))

    (define/augment (after-interactive-move event)
      (define piece (send this find-next-selected-snip #f))
      (define location (xy->location this (send event get-x) (send event get-y)))
      (define valid-moves (send piece valid-moves))
      (when (member location valid-moves)
        ;; This is a valid move, remove any target piece and update the piece
        ;; location
        (let ((target-piece (piece-at-location this location)))
          (when (and target-piece (not (eq? piece target-piece)))
            (send target-piece set-location #f)
            (send this remove target-piece)))
        (set! turn (if (eq? turn 'white) 'black 'white))
        (send piece set-location location))
      ;; If the move is not valid it will be moved back.
      (position-piece this piece)
      (set! highlight-location #f)
      ;; Note: piece is still selected, but the valid moves are relative to
      ;; the new position
      (set! valid-move-locations (send piece valid-moves))
      (send (send this get-canvas) refresh))

    (define/augment (after-select snip on?)
      (if on?
          (begin
            (unless (eq? turn (send snip color))
              (set-message (format "It's ~a turn to move"
                            (if (eq? turn 'white) "white's" "black's"))))
            (set! valid-move-locations (send snip valid-moves))
            (set! opponent-move-locations
                  (collect-opponent-moves this (send snip color))))
          (begin
            (set! opponent-move-locations '())
            (set! valid-move-locations '())))
      (send (send this get-canvas) refresh))

    ))

(define (collect-opponent-moves board color)
  (define moves '())
  (let loop ((snip (send board find-first-snip)))
    (when snip
      (unless (eq? (send snip color) color)
        (set! moves (append moves (send snip valid-moves))))
      (loop (send snip next))))
  (remove-duplicates moves))

(define (position-piece board piece)
  (define-values (canvas-width canvas-height)
    (let ((c (send board get-canvas)))
      (send c get-size)))
  (define-values (square-width square-height)
    (values (/ canvas-width 8) (/ canvas-height 8)))
  (define-values (rank file)
    (location->rank-file (send piece get-location)))
  (define-values (square-x square-y)
    (values (* file square-width) (* rank square-height)))
  (define piece-width (snip-width piece))
  (define piece-height (snip-height piece))
  (send board move-to piece
        (+ square-x (/ (- square-width piece-width) 2))
        (+ square-y (/ (- square-height piece-height) 2))))

(define (location->rank-file location)
  (unless (and (string? location) (= (string-length location) 2))
    (raise-argument-error 'location "valid chess position a1 .. h8" location))
  (define file
    (index-of '(#\a #\b #\c #\d #\e #\f #\g #\h) (string-ref location 0)))
  (define rank
    (index-of '(#\8 #\7 #\6 #\5 #\4 #\3 #\2 #\1) (string-ref location 1)))
  (unless (and rank file)
    (raise-argument-error 'location "valid chess position a1 .. h8" location))
  (values rank file))

(define (rank-file->location rank file)
  (unless (<= 0 rank 8)
    (raise-argument-error 'rank "integer between 0 and 7" rank))
  (unless (<= 0 file 8)
    (raise-argument-error 'rank "integer between 0 and 7" file))
  (string
   (list-ref '(#\a #\b #\c #\d #\e #\f #\g #\h) file)
   (list-ref '(#\8 #\7 #\6 #\5 #\4 #\3 #\2 #\1) rank)))

(define (xy->location board x y)
  (define-values (canvas-width canvas-height)
    (let ((c (send board get-canvas)))
      (send c get-size)))
  (define-values (square-width square-height)
    (values (/ canvas-width 8) (/ canvas-height 8)))
  (define-values (rank file)
    (values (exact-truncate (/ y square-height)) (exact-truncate (/ x square-width))))
  (rank-file->location rank file))

(define (piece-at-location board location)
  (let loop ((snip (send board find-first-snip)))
    (if snip
        (if (equal? location (send snip get-location))
            snip
            (loop (send snip next)))
        #f)))

(define (display-message dc message)
  (define font (send the-font-list find-or-create-font 24 'default 'normal 'normal))
  (define-values [w h _1 _2] (send dc get-text-extent message font #t))
  (define-values (dc-width dc-height) (send dc get-size))
  (define-values (x y) (values (/ (- dc-width w) 2) (/ (- dc-height h) 2)))

  (define brush (send the-brush-list find-or-create-brush "bisque" 'solid))
  (define pen (send the-pen-list find-or-create-pen "black" 1 'transparent))
  (send dc set-brush brush)
  (send dc set-pen pen)
  (send dc draw-rectangle 0 y dc-width h)
  (send dc set-font font)
  (send dc set-text-foreground "firebrick")
  (send dc draw-text message x y))

(define (draw-chess-board dc)
  (define brush (send the-brush-list find-or-create-brush "gray" 'solid))
  (define pen (send the-pen-list find-or-create-pen "black" 1 'transparent))
  (define font (send the-font-list find-or-create-font 8 'default 'normal 'normal))
  (define-values (dc-width dc-height) (send dc get-size))
  (define cell-width (/ dc-width 8))
  (define cell-height (/ dc-height 8))
  (define margin 3)
    
  (send dc clear)
  (send dc set-brush brush)
  (send dc set-pen pen)
  (send dc set-font font)
  
  (for* ([row (in-range 8)] [col (in-range 8)]
         #:when (or (and (odd? row) (even? col))
                    (and (even? row) (odd? col))))
    (define-values [x y] (values (* col cell-width) (* row cell-height)))
    (send dc draw-rectangle x y cell-width cell-height))

  (for ([(rank index) (in-indexed '("8" "7" "6" "5" "4" "3" "2" "1"))])
    (define-values [_0 h _1 _2] (send dc get-text-extent rank font #t))
    (define y (+ (* index cell-height) (- (/ cell-height 2) (/ h 2))))
    (send dc draw-text rank margin y))
  
  (for ([(file index) (in-indexed '("a" "b" "c" "d" "e" "f" "g" "h"))])
    (define-values [w h _1 _2] (send dc get-text-extent file font #t))
    (define x (+ (* index cell-width) (- (/ cell-width 2) (/ w 2))))
    (send dc draw-text file x (- dc-height h margin))))

(define (highlight-square dc location color-name border-color-name)
  (define-values (rank file) (location->rank-file location))
  (define brush
    (if color-name
        (let* ((base (send the-color-database find-color color-name))
               (color (make-object color% (send base red) (send base green) (send base blue) 0.3)))
          (send the-brush-list find-or-create-brush color 'solid))
        (send the-brush-list find-or-create-brush "black" 'transparent)))
  (define pen
    (if border-color-name
        (send the-pen-list find-or-create-pen border-color-name 4 'solid)
        (send the-pen-list find-or-create-pen "black" 1 'transparent)))
  (send dc set-pen pen)
  (send dc set-brush brush)
  (define-values (dc-width dc-height) (send dc get-size))
  (define-values (cell-width cell-height) (values (/ dc-width 8) (/ dc-height 8)))
  (send dc draw-rectangle (* file cell-width) (* rank cell-height) cell-width cell-height))

;; A test program for our chess-piece% objects:

;; The pasteboard% that will hold and manage the chess pieces
(define board (new chess-board%))
;; Toplevel window for our application
(define toplevel (new frame% [label "Chess Board"] [width (* 50 8)] [height (* 50 8)]))
;; The canvas which will display the pasteboard contents
(define canvas (new editor-canvas%
                    [parent toplevel]
                    [style '(no-hscroll no-vscroll)]
                    [horizontal-inset 0]
                    [vertical-inset 0]
                    [editor board]))
(send toplevel show #t)


(define initial
  (string-append
   "Ra1Nb1Bc1Qd1Ke1Bf1Ng1Rh1"
   "Pa2Pb2Pc2Pd2Pe2Pf2Pg2Ph2"
   "pa7pb7pc7pd7pe7pf7pg7ph7"
   "ra8nb8bc8qd8ke8bf8ng8rh8"))

(define (setup-board board position)
  (send board clear)
  (define piece-count (/ (string-length position) 3))
  (for ([index (in-range piece-count)])
    (define pos (* index 3))
    (define name (substring position pos (add1 pos)))
    (define location (substring position (add1 pos) (+ (add1 pos) 2)))
    (send board insert (make-chess-piece name location))))

(setup-board board initial)
