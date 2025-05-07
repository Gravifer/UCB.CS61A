(define (curry-cook formals body)
  (if (null? formals) (error "No arguments") ; asserted not to happen
      (let ((formal (car formals))
            (rest-formals (cdr formals)))
        `(lambda (,formal)
            ,(if (null? rest-formals) body
                 (curry-cook rest-formals body))))))
        ; (if (null? rest-formals)
        ;     `(lambda (,formal) ,body)
        ;     `(lambda (,formal) ,(curry-cook rest-formals body))))))
  ; (if (null? (cdr formals))
  ;     (begin (displayln "DEBUG: [innermost] formal =" (car formals) ", body =" body)
  ;       `(lambda (,(car formals)) ,body))
  ;     (let ((formal (car formals))
  ;           (rest-formals (cdr formals)))
  ;       (begin (displayln "DEBUG: formal =" formal ", body =" body)
  ;         `(lambda (,formal) ,(curry-cook rest-formals body))))))

(define (curry-consume curry args)
  (if (null? args) curry
      (let ((partial (curry (car args)))
            (rest-args (cdr args)))
        (curry-consume partial rest-args))))

(define-macro (switch expr options)
  (switch-to-cond (list 'switch expr options)))

(define (switch-to-cond switch-expr)
  (cons 'cond
        (map (lambda (option)
               (cons (list 'equal? (car (cdr switch-expr)) (car option)) (cdr option)))
             (car (cdr (cdr switch-expr))))))
