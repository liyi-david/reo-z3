(define-sort DS (D) (Array Int D))
(define-sort TS () (Array Int Real))

(declare-const dA (DS Int))
(declare-const tA (TS))

(declare-const dB (DS Int))
(declare-const tB (TS))

(declare-const dC (DS Int))
(declare-const tC (TS))

(assert (= dA dB))
(assert (= dB dC))
(assert (= tA tC))
(assert (= tB tC))
(assert (forall ((x Int)) (< (select tA x) (select tB x))))

(check-sat)