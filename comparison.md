|   | Coq | Z3 |
|---|-----|----|
| Sync | `Definition Sync (Input Output:Stream TD) : Prop :=`<br>`Teq Input Output /\ Deq Input Output.` | .. |
| SyncDrain | `Definition SyncDrain (Input Output:Stream TD) : Prop :=`<br>`Teq Input Output.` | .. |
| FIFO1 | `Definition FIFO1(Input Output:Stream TD) : Prop :=`<br>`Tle Input Output /\ Tle Output (tl Input) /\ Deq Input Output.` | .. |
| FIFO1e | `Definition FIFO1e(Input Output:Stream TD)(e:Data) : Prop :=`<br> `Tgt Input Output /\ Tle Input (tl Output)`<br>`/\ PrR (hd` \ `Output) = e  /\ Deq Input (tl Output).` | .. |
| LossySync | `Parameter LossySync: Stream TD -> Stream TD -> Prop.`<br>`Axiom LossySync_coind: forall Input Output: Stream TD,`<br>`LossySync Input Output ->`<br>`(( hd Output = hd Input  /\ LossySync (tl Input)(tl Output)) \/`<br>`LossySync(tl Input) Output).`
