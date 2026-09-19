# 30-Day Staff Data Engineer Study Plan

## Curriculum Breakdown
| Topic | Sub-topic | Est. % Frequency | Success Criteria | Hours |
| :--- | :--- | :--- | :--- | :--- |
| Distributed Systems Theory | Consensus, CAP, Replication, Partitioning | 15% | Explain split-brain, vector clocks, leader election, network partitions. | 40 |
| Massive Scale Streaming | Kafka Internals, Flink State, Watermarks | 25% | Architect exactly-once, tune RocksDB, watermark delays, Kafka zero-copy/ISR. | 60 |
| Storage & File Internals | LSM Trees, B-Trees, Parquet, Iceberg | 15% | Explain dictionary encoding vs RLE, Bloom filters, Iceberg snapshot isolation. | 40 |
| Compute & Low-Level Tuning | Spark/Trino Internals, CBO, JVM | 20% | Debug OOMs via heap dumps, Catalyst optimizer, broadcast joins, G1GC tuning. | 50 |
| Data-Intensive System Design | Multi-tenancy, CQRS, Event Sourcing | 20% | Architect 1M RPS ingestion. Token bucket, sharding, idempotent consumers. | 80 |
| The Staff Narrative | Impact, Trade-offs, Behavioral | 5% | AWS->GCP migration story highlighting extreme trade-offs and org influence. | 50 |

## Daily Execution Plan
**Constraints:** Mon-Fri (8h/day), Sat-Sun (16h/day).

### Week 1: Distributed Systems & Storage (Days 1-7)
* Days 1-2: DDIA Ch 5 (Replication) & Ch 6 (Partitioning). Parquet internals (Encoding, Predicate Pushdown).
* Days 3-4: DDIA Ch 7 (Transactions) & Ch 8 (Trouble). Iceberg spec (metadata trees, concurrency).
* Day 5: DDIA Ch 9 (Consensus). Re-map CQRS architecture to Iceberg/Trino.
* Days 6-7: Raft Whitepaper. Implement Bloom Filter in Python. System Design Mock: Distributed KV store.

### Week 2: Massive Scale Streaming (Days 8-14)
* Days 8-9: Kafka Internals (Zero-Copy, Page Cache, KRaft, Partitions, ISRs).
* Days 10-11: Flink Concepts (Watermarks, Windows). RocksDB state backend. Chandy-Lamport algorithm.
* Day 12: Delivery Guarantees (Exactly-once, Kafka Txns, Flink 2PC). Redesign ingestion for 100K/sec.
* Days 13-14: System Design Mock: Uber Surge Pricing (temporal joins). Diagram Flink backpressure.

### Week 3: Compute Internals & Resiliency (Days 15-21)
* Days 15-16: Spark/Trino Catalyst Optimizer, Tungsten. Join Strategies (Broadcast vs Sort-Merge, Memory).
* Days 17-18: JVM Internals (Heap vs Off-Heap, G1GC). Token Bucket/Leaky Bucket rate limiting.
* Day 19: Circuit Breakers, Retry with Jitter. Whiteboard AWS->GCP migration failure modes.
* Days 20-21: System Design Mock: Ad-hoc query platform for 1000 users. Write OOM debugging playbook.

### Week 4: System Design & Narrative (Days 22-30)
* Days 22-24: Read Uber/Netflix Tech Blogs (Hudi, Keystone). System Design Mock: Video Viewing Pipeline.
* Days 25-26: Refine AWS->GCP Migration narrative using STAR method. Focus on CAP trade-offs and consistency.
* Days 27-29: System Design Mocks (Fraud Detection, Message Queue, CDC system).
* Day 30: Final review of notes and narrative.
