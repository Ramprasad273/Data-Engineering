# Day 1: Replication, Partitioning, and Parquet Internals

## Learning Objectives

### Distributed Systems Theory (DDIA Ch 5 & 6)
* **Replication:** Synchronous vs. Asynchronous (Durability vs. Latency).
* **Node Outages:** Catch-up recovery and split-brain mitigation.
* **Leaderless Replication:** Quorums ($W + R > N$), hinted handoff.
* **Concurrency:** Vector clocks, Last-Write-Wins (LWW).
* **Partitioning:** Key Range vs. Hash of Key (Consistent Hashing).
* **Secondary Indexes:** Document-partitioned vs. Term-partitioned.
* **Rebalancing:** Dynamic partition rebalancing.

### Parquet Internals
* **Columnar vs Row-based:** Performance differences for OLAP.
* **Encoding:** Dictionary Encoding, Run-Length Encoding (RLE), Bit-packing.
* **Predicate Pushdown:** Using Parquet footers (min/max stats) to skip row groups.

## Common Issues & Gotchas
* **Replication Lag:** Causes "Read Your Own Writes" anomalies.
* **Sloppy Quorums:** Increases availability but breaks strict consistency.
* **High Cardinality:** Breaks Parquet dictionary encoding, inflating file size.
* **Small Files:** Parquet metadata overhead exceeds data processing time.

## Staff-Level Interview Questions
1. **Resolve and prevent cluster split-brain.**
   * *Focus:* Leader election epochs, fencing tokens, Raft/Paxos.
2. **Achieve 'Read Your Own Writes' in asynchronous replication.**
   * *Focus:* Routing reads to leader briefly post-write, or client-side logical timestamps.
3. **Debug a Spark job reading Parquet that suddenly takes 3x longer.**
   * *Focus:* File size changes (small files), schema changes breaking pushdown, high-cardinality blowing out dictionary encoding.

## Medium Blog Details

**Title Options:**
1. Architectural Trade-offs: Why High Cardinality Kills Parquet Performance
2. Designing for Failure: Mitigating Split-Brain in Distributed Data Systems

**Blog Structure & Content:**
1. **Hook:** An advanced architectural observation or common misconception at scale (e.g., "Many engineers assume Parquet dictionary encoding is universally optimal, until they hit extreme cardinality at the Petabyte scale").
2. **Theory:** System-level trade-offs of asynchronous replication and sloppy quorums.
3. **Deep Dive:** Parquet byte-level layout (Row Groups, Column Chunks) and Dictionary Encoding mechanics.
4. **Takeaway:** How Predicate Pushdown saves millions of compute cycles and reduces network I/O bottlenecks.
5. **Architectural Challenge:** Pose the split-brain mitigation strategy (leader election epochs, fencing) as a system design thought exercise for the reader.
