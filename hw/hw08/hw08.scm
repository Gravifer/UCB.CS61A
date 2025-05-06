(define (ascending? s)
  (if (null? s)
      #t
      (let ((first (car s))
            (rest (cdr s)))
        (if (null? rest)
            #t
            (and
              (>= (car rest) first)
              (ascending? rest))))))

(define (my-filter pred s)
  (if (null? s)
      '()
      (let ((first (car s))
            (rest (cdr s)))
        (if (pred first)
            (cons first (my-filter pred rest))
            (my-filter pred rest)))))

(define (interleave lst1 lst2)
  (if (null? lst1)
      lst2
      (if (null? lst2)
          lst1
          (cons (car lst1)
                (cons (car lst2) (interleave (cdr lst1) (cdr lst2)))))))

(define (no-repeats s)
  (if (null? s)
      '()
      (let ((first (car s))
            (rest (cdr s)))
        (cons first
              (no-repeats 
                (my-filter
                  (lambda (x) (not (equal? x first)))
                  rest))))))
