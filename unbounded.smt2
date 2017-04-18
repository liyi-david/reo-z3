; type declarations
; TODO: we should use real-arthimetic as time-dimension instead

(define-sort Index () Int) 

(define-sort DS (D) (Array Int D))
(define-sort TS () (Array Int Int))


; timed data stream declarations

(declare-datatypes (D) ((TDS (mk-pair (timeStream TS) (dataStream (DS D))))))

(define-sort TDS0 () (TDS Int))


; function declarations
; basic functions about time
; FIXME: assumption on time stream is not provided

(define-fun Tle ((a TS) (b TS)) Bool (forall ((ind Int)) (<= (select a ind) (select b ind))))
(define-fun Tlt ((a TS) (b TS)) Bool (forall ((ind Int)) (<  (select a ind) (select b ind))))
(define-fun Tge ((a TS) (b TS)) Bool (forall ((ind Int)) (>= (select a ind) (select b ind))))
(define-fun Tgt ((a TS) (b TS)) Bool (forall ((ind Int)) (>  (select a ind) (select b ind))))
(define-fun Teq ((a TS) (b TS)) Bool (forall ((ind Int)) (=  (select a ind) (select b ind))))

(define-fun Deq ((a (DS Int)) (b (DS Int))) Bool (forall ((ind Int)) (=  (select a ind) (select b ind))))

; definition of channels
(define-fun Sync ((a TDS0) (b TDS0)) Bool
	(and
		(Teq (timeStream a) (timeStream b))
		(Deq (dataStream a) (dataStream b))
	))

(define-fun Fifo1 ((a TDS0) (b TDS0)) Bool
	(and
		(Tlt (timeStream a) (timeStream b))
		(Deq (dataStream a) (dataStream b))
	))

; (assert (forall ((a TS)) (
;     and
;         (= (select a 0) 0)
;         (forall ((i Int)) (< (select a i) (select a (+ i 1))))
;  )))

; the idea is here
; if connector P is a refinement of Q, we assume that it should be proved by Coq
; basically, the complete form of P -> Q is
;
;     forall Port_1, ..., Port_n. P(Port_i) -> Q(Port_i)
;
; i.e. its negation is
;
;     exists Port_1, ..., Port_n. P and !Q
;
; which can be solved by SMT solvers like Z3
; once we find a model that satisfied (P and !Q), we know P is not a refinement of Q

(push)

(echo "Example 1. (P) Fifo1 is NOT a refinement of (Q) Sync ?")

(declare-const A TDS0)
(declare-const B TDS0)

(assert (Fifo1 A B))
(assert (not (Sync A B)))

(check-sat)
; (get-model)

(pop)

(push)
(echo "Example 2. (P) Double-Sync is NOT a refinement of (Q) single-Sync")

(declare-const A TDS0)
(declare-const B TDS0)

(assert (Sync A B))
(assert (not (exists ((M TDS0)) (and (Sync A M) (Sync M B)))))

(check-sat)
; (get-model)
(pop)

(push)
(echo "Example 3. (P) Double-Sync is NOT a refinement of (Q) Sync-Fifo1")

(declare-const A TDS0)
(declare-const B TDS0)

(assert (Sync A B))
(assert (not (exists ((M TDS0)) (and (Sync A M) (Fifo1 M B)))))

(check-sat)
; (get-model)
(pop)


(push)
(echo "Example 4. (P) Sync-2Fifo1 is NOT a refinement of (Q) Fifo1-2Sync")

(declare-const A TDS0)
(declare-const B TDS0)
(declare-const C TDS0)

(assert (exists ((M TDS0)) (and (Sync A M) (Fifo1 M B) (Fifo1 M C))))
(assert (not (exists ((M TDS0)) (and (Fifo1 A M) (Sync M B) (Sync M C)))))

; (declare-const M0 TDS0)
; (declare-const M1 TDS0)

; (assert (and (Sync A M0) (Fifo1 M0 B) (Fifo1 M0 C)))
; (assert (not (and (Fifo1 A M1) (Sync M1 B) (Sync M1 C))))

(check-sat)
; (get-model)
(pop)
