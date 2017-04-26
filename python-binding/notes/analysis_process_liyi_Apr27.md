                  / [sync] B
C1  A - [fifo] - N
                  \ [sync] C
              
                  / [fifo] B
C2  A - [sync] - M
                  \ [fifo] C


C1 refines C2 ?
C1 => C2?

RAW - forall A,B,C,N (
  TDS(A) and TDS(B) and TDS(C) and TDS(D) and Fifo(A,N) and Sync(N,B) and Sync(N,C)
    => exists M, TDS(M) and Sync(A,M) and FIFO(M,B) and FIFO(M,C)
)

!RAW?

exists A,B,C,N (
  TDS(A) and TDS(B) and TDS(C) and TDS(D) and Fifo(A,N) and Sync(N,B) and Sync(N,C) and
  forall M, not TDS(M) or not (Sync(A,M) and ... )
)

counter - example

A DATA = [0, ..]
A TIME = [0,1,..,8]

B DATA = [0, ..]
B TIME = [1, .., 9]

C = B

N DATA = [0, ..]
N TIME = [1, .., 9]