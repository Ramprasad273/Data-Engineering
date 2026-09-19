# Day 2: Partitioning Strategies, Replication Edge Cases, and Parquet Optimization

## Learning Objectives

### Distributed Systems Theory (DDIA Ch 5 & 6 Deep Dive)
* **Consistent Hashing:** Mechanics of adding/removing nodes with minimal data movement.
* **Hotspots & Skew:** Strategies for dealing with celebrity/hot keys (salting, compound routing keys).
* **Cross-Datacenter Replication:** Multi-leader replication topologies, conflict resolution (CRDTs vs. custom resolvers).
* **Partitioning Secondary Indexes:** Local vs. Global indexes (scatter/gather query routing vs. write-time index updates).
* **Rebalancing Operations:** Fixed number of partitions vs. dynamic partitioning (trade-offs during cluster scaling).

### Parquet Internals & Optimization
* **Schema Evolution:** How Parquet handles added, removed, or changed columns (schema merging).
* **Bloom Filters in Parquet:** How they complement min/max stats for point lookups to skip row groups.
* **Vectorized Query Execution:** How modern engines (Trino/Spark) process columnar batches instead of row-by-row.
* **Sorting & Z-Ordering:** Multi-dimensional clustering to maximize predicate pushdown efficiency.

## Common Issues & Gotchas
* **Rebalancing Storms:** Moving too much data when scaling out a partitioned database, causing network saturation.
* **Multi-Leader Conflicts:** Unintended overwrites in active-active topologies due to poorly designed conflict resolution.
* **Parquet Memory Overhead:** Having too many small row groups negates vectorized processing benefits and increases I/O.
* **Ineffective Bloom Filters:** Applying Bloom filters on low-cardinality or poorly distributed columns wastes storage space.

## Staff-Level Interview Questions
1. **Design a partitioning strategy for a global social media platform's activity feed.**
   * *Focus:* Handling celebrity hotspots (salting/scatter-gather), consistent hashing, and localized secondary indexes.
2. **How would you migrate a petabyte-scale database from single-leader to multi-leader without downtime?**
   * *Focus:* Replication lag during migration, dual-writes, conflict resolution planning, and application-level routing.
3. **Your Trino queries on a massive Parquet table are doing full table scans despite having partition keys. How do you fix it?**
   * *Focus:* Missing file statistics, mismatch in data types preventing predicate pushdown, missing Z-ordering/sorting, or tiny row groups.

## Medium Blog Details

**Title Options:**
1. Taming the Hot Key: Advanced Partitioning Strategies at Petabyte Scale
2. Beyond Min/Max: Maximizing Parquet Performance with Bloom Filters and Z-Ordering

**Blog Structure & Content:**
1. **Hook:** Start with a catastrophic failure scenario: a sudden viral trend causes a "hot key" that brings down an entire database partition, cascading failure across the cluster.
2. **Theory:** Explain Consistent Hashing and why standard modulo hashing breaks down during cluster scaling.
3. **Deep Dive:** Detail the "salting" technique for hot keys and the architectural trade-offs of Global vs. Local secondary indexes.
4. **Optimization:** Pivot to storage: how to structure Parquet files (sorting/Z-Ordering) to ensure point lookups on partitioned data remain blazingly fast using Bloom filters.
5. **Architectural Challenge:** Pose a scenario to the reader: "If your Parquet files are heavily Z-ordered but queries are still slow, what hidden memory overhead might be killing your vectorized execution?"
