(define (over-or-under num1 num2)
  ; (if (< num1 num2) -1
  ;     (if (> num1 num2) 1  0))
  ; cond is not documented in the CS61A spec though
  (cond ((< num1 num2) -1)
        ((> num1 num2) 1)
        (else 0)))

(define (make-adder num)
  (lambda (inc) (+ num inc)))

(define (composed f g)
  (lambda (x) (f (g x))))

(define (repeat f n)
  ;; naive version
  ; (if (= n 0)
  ;     (lambda (x) x)
  ;     (composed f (repeat f (- n 1))))
  ;; fast pow version
  ; however, this just makes constructing the lambda efficient, which is not much.
  (if (= n 0)
      (lambda (x) x)
      (if (= (modulo n 2) 0)
          (composed (repeat f (/ n 2)) (repeat f (/ n 2)))
          (composed f (composed (repeat f (/ (- n 1) 2)) (repeat f (/ (- n 1) 2)))))))

(define (max a b)
  (if (> a b)
      a
      b))

(define (min a b)
  (if (> a b)
      b
      a))

(define (gcd a b)
  (if (= b 0)
      a
      (gcd b (modulo a b))))
