(define (if-program condition if-true if-false)
  `(if ,condition
     (begin ,if-true)
     (begin ,if-false)))

(define (square n) (* n n))

(define (pow-expr base exp) ; fast pow constructed
  (cond 
    ((= exp 0) 1)
    ((= exp 1) `(* ,base 1))
    ((= (remainder exp 2) 0) `(square ,(pow-expr base (/ exp 2))))
    (else `(* ,base ,(pow-expr base (- exp 1))))
  ))

(define-macro (repeat n expr)
  `(repeated-call ,n (lambda () ,expr))) ; use a thunk to defer
; the interface of repeated-call dictates this; otherwise one may also use a 

; Call zero-argument procedure f n times and return the final result.
(define (repeated-call n f)
  (if (= n 1)
      (f)
      (begin (f) (repeated-call (- n 1) f))))
