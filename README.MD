# MongoDB Consistency and Replication Demo

This project demonstrates various consistency models and replication behaviors in MongoDB using a replica set configuration with Docker.

## Project Overview

This lab explores MongoDB's distributed system features including:
- **Eventual Consistency**: Demonstrating read operations that may return stale data
- **Strong Consistency**: Using majority read/write concerns for linearizable reads
- **Failover Simulation**: Testing MongoDB's automatic failover mechanisms
- **Replication**: Observing data propagation across replica set members

## Prerequisites

- Docker and Docker Desktop
- Python 3.11+
- PowerShell or Command Prompt (Windows) or Terminal (Mac/Linux)

## Project Structure

```
Lab-2/
├── docker-compose.yml           # Docker configuration for MongoDB replica set
├── seed.py                      # Seeds initial data into MongoDB
├── utils.py                     # Utility functions for client connection
├── eventual_consistency_demo.py # Demonstrates eventual consistency behavior
├── strong_consistency_demo.py   # Demonstrates strong consistency with majority concerns
├── failover_demo.py            # Simulates primary node failure and failover
├── requirements.txt            # Python dependencies
└── README.md                   # This file
```

## Installation and Setup

### Step 1: Install Python Dependencies

```bash
pip install -r requirements.txt
```

Or install manually:
```bash
pip install pymongo dnspython
```

### Step 2: Start MongoDB Replica Set

Make sure Docker Desktop is running, then navigate to your project directory:

```bash
cd "C:\Users\anush\Distributed Systems\Lab-2"
```

Start the Docker containers:

```bash
docker-compose up -d
```

Verify all containers are running:

```bash
docker ps
```

Expected output:
```
CONTAINER ID   IMAGE       COMMAND                  CREATED         STATUS         PORTS                      NAMES
99515c41bbdc   mongo:8.0   "docker-entrypoint.s…"   4 seconds ago   Up 4 seconds   0.0.0.0:27018->27017/tcp   mongo2
e0c2bff9a467   mongo:8.0   "docker-entrypoint.s…"   4 seconds ago   Up 4 seconds   0.0.0.0:27017->27017/tcp   mongo1
2da8e0f979cc   mongo:8.0   "docker-entrypoint.s…"   4 seconds ago   Up 4 seconds   0.0.0.0:27019->27017/tcp   mongo3
```

### Step 3: Initialize the Replica Set

Connect to the primary MongoDB instance:

```bash
docker exec -it mongo1 mongosh
```

Initialize the replica set:

```javascript
rs.initiate({
  _id: "rs0",
  members: [
    { _id: 0, host: "mongo1:27017" },
    { _id: 1, host: "mongo2:27017" },
    { _id: 2, host: "mongo3:27017" }
  ]
})
```

Expected output:
```javascript
{
  ok: 1,
  '$clusterTime': {
    clusterTime: Timestamp({ t: 1761521328, i: 1 }),
    ...
  },
  operationTime: Timestamp({ t: 1761521328, i: 1 })
}
```

Check replica set status:

```javascript
rs.status()
```

You should see one PRIMARY and two SECONDARY nodes. Exit the MongoDB shell:

```javascript
exit
```

## Running the Demos

### 1. Seed the Database

```bash
python seed.py
```

**Output:**
```
Seed data inserted successfully!
```

### 2. Eventual Consistency Demo

```bash
python eventual_consistency_demo.py
```

**Expected Behavior:**
- Inserts a document with timestamp 0
- Performs 5 consecutive reads from secondary nodes
- Shows how data propagates across the replica set

**Sample Output:**
```
Inserted document, checking secondary replication...
Check 1: {'_id': ObjectId('68feaec63a92c04cf363a69d'), 'test': 'eventual_consistency', 'timestamp': 0}
Check 2: {'_id': ObjectId('68feaec63a92c04cf363a69d'), 'test': 'eventual_consistency', 'timestamp': 0}
Check 3: {'_id': ObjectId('68feaec63a92c04cf363a69d'), 'test': 'eventual_consistency', 'timestamp': 0}
Check 4: {'_id': ObjectId('68feaec63a92c04cf363a69d'), 'test': 'eventual_consistency', 'timestamp': 0}
Check 5: {'_id': ObjectId('68feaec63a92c04cf363a69d'), 'test': 'eventual_consistency', 'timestamp': 0}
```

### 3. Strong Consistency Demo

```bash
python strong_consistency_demo.py
```

**Features:**
- Uses `WriteConcern("majority")` for writes
- Uses `ReadConcern("majority")` for reads
- Ensures linearizable consistency across the replica set

**Sample Output:**
```
Waiting 2 seconds for replication...
Strong Consistency Demo Result: {'_id': ObjectId('68feaecdac2b4a7a8c0bd5ff'), 'test': 'strong_consistency', 'timestamp': 0}
```

### 4. Failover Demo

```bash
python failover_demo.py
```

**What it does:**
1. Inserts a document before simulated failure
2. Waits for replication
3. Prompts to manually stop the primary node
4. Attempts to insert another document after failover
5. Displays all documents to verify data integrity

**Sample Output:**
```
Simulate failover: Insert before primary failure
Waiting 2 seconds for replication...
Simulate stopping primary node manually (check Docker)
Documents after failover simulation:
{'_id': ObjectId('68feaec63a92c04cf363a69d'), 'test': 'eventual_consistency', 'timestamp': 0}
{'_id': ObjectId('68feaecdac2b4a7a8c0bd5ff'), 'test': 'strong_consistency', 'timestamp': 0}
{'_id': ObjectId('68feaed07e90332d41a1c8a2'), 'failover_test': 'before_failure'}
{'_id': ObjectId('68feaed27e90332d41a1c8a3'), 'failover_test': 'after_failure'}
```

## Docker Compose Configuration

The `docker-compose.yml` file creates a 3-node MongoDB replica set:

- **mongo1** (Primary): Port 27017
- **mongo2** (Secondary): Port 27018
- **mongo3** (Secondary): Port 27019

All nodes are connected via a Docker bridge network and use persistent volumes for data storage.

## MongoDB Connection

The Python scripts connect using:
```
mongodb://localhost:27017,localhost:27018,localhost:27019/?replicaSet=rs0
```

## Key Concepts Demonstrated

### Eventual Consistency
- Reads may return stale data from secondary nodes
- Data eventually propagates to all replicas
- Lower latency but weaker consistency guarantees
- Suitable for read-heavy workloads where slight staleness is acceptable

### Strong Consistency
- Majority read/write concerns ensure data is acknowledged by most replica set members
- Guarantees linearizable reads (read-your-writes consistency)
- Higher latency but stronger consistency guarantees
- Essential for critical data where accuracy is paramount

### Replication
- Automatic data synchronization from primary to secondary nodes
- Configurable replication lag tolerance
- Built-in redundancy for high availability
- Oplog-based replication mechanism

### Failover
- Automatic election of new primary when current primary fails
- Election uses Raft consensus protocol
- Minimal downtime during failover process (typically 10-30 seconds)
- Data integrity maintained across failure scenarios
- Write availability requires majority of nodes to be healthy

## Useful Docker Commands

### View Container Status
```bash
docker ps
docker-compose ps
```

### View Logs
```bash
# All containers
docker-compose logs

# Specific container
docker-compose logs mongo1

# Follow logs in real-time
docker-compose logs -f
```

### Stop and Start
```bash
# Stop all containers
docker-compose stop

# Start stopped containers
docker-compose start

# Restart specific container
docker-compose restart mongo1
```

### Clean Up
```bash
# Stop and remove containers (keeps data)
docker-compose down

# Stop and remove everything including volumes
docker-compose down -v
```

### Access MongoDB Shell
```bash
# Connect to any node
docker exec -it mongo1 mongosh
docker exec -it mongo2 mongosh
docker exec -it mongo3 mongosh
```

### Check Replica Set Status
```bash
docker exec -it mongo1 mongosh --eval "rs.status()"
```

## Troubleshooting

### Issue: Containers won't start
**Error:** `Conflict. The container name "/mongo1" is already in use`

**Solution:**
```bash
# Remove existing containers
docker rm -f mongo1 mongo2 mongo3

# Or use docker-compose
docker-compose down

# Start fresh
docker-compose up -d
```

### Issue: No PRIMARY node
All nodes show as SECONDARY in `rs.status()`.

**Solution:** Wait 10-30 seconds for election to complete, then check again:
```bash
docker exec -it mongo1 mongosh --eval "rs.status()"
```

### Issue: "already initialized" error
**Error:** `MongoServerError: already initialized`

**Explanation:** The replica set is already configured. This is normal if you've already run `rs.initiate()`. You can proceed with running the Python scripts.

### Issue: Connection refused from Python
**Solution:**
1. Verify containers are running: `docker ps`
2. Check replica set is initialized: `docker exec -it mongo1 mongosh --eval "rs.status()"`
3. Ensure your connection string is correct
4. Wait 10-15 seconds after initialization before running Python scripts

### Issue: ModuleNotFoundError
**Error:** `ModuleNotFoundError: No module named 'pymongo'`

**Solution:**
```bash
pip install -r requirements.txt
```

### Issue: ImportError for ReadConcern
**Error:** `ImportError: cannot import name 'ReadConcern' from 'pymongo'`

**Solution:** Update `strong_consistency_demo.py`:
```python
from pymongo import WriteConcern
from pymongo.read_concern import ReadConcern  # Correct import
```

### Issue: Port already in use
**Solution:**
```bash
# Windows - check what's using the port
netstat -ano | findstr :27017

# Kill the process or change ports in docker-compose.yml
```

## Replica Set Architecture

```
┌─────────────────────────────────────────┐
│         Your Python Scripts             │
│  (seed, demos, consistency tests)       │
└──────────────┬──────────────────────────┘
               │
               │ Connection String:
               │ mongodb://localhost:27017,27018,27019/?replicaSet=rs0
               │
       ┌───────┴────────┬────────────┐
       │                │            │
┌──────▼──────┐  ┌──────▼──────┐  ┌─▼──────────┐
│   mongo1    │  │   mongo2    │  │   mongo3   │
│  :27017     │◄─┤  :27018     │◄─┤  :27019    │
│  PRIMARY    │─►│  SECONDARY  │─►│  SECONDARY │
│             │  │             │  │            │
│ Replica Set │  │ Replica Set │  │Replica Set │
│    rs0      │  │    rs0      │  │   rs0      │
└──────┬──────┘  └──────┬──────┘  └─┬──────────┘
       │                │            │
┌──────▼──────┐  ┌──────▼──────┐  ┌─▼──────────┐
│  Volume 1   │  │  Volume 2   │  │  Volume 3  │
│ (Persistent)│  │ (Persistent)│  │(Persistent)│
└─────────────┘  └─────────────┘  └────────────┘
```

## Learning Outcomes

After completing this lab, you should understand:

**CAP Theorem Trade-offs**: The practical implications of choosing consistency over availability or vice versa

**Replication Mechanisms**: How MongoDB uses oplog-based replication to maintain data consistency

**Consensus Protocols**: How MongoDB uses Raft-like consensus for leader election

**Read/Write Concerns**: How to configure different consistency levels based on application needs

**Failover Behavior**: How distributed databases handle node failures automatically

**Consistency Models**: The difference between eventual and strong consistency in practice

## Dependencies

- **pymongo 4.15.3** - MongoDB Python driver
- **dnspython 2.8.0** - DNS toolkit for Python (required by pymongo for SRV connection strings)

See `requirements.txt` for the complete dependency list.

## Common Use Cases

### When to Use Eventual Consistency
- Social media feeds
- Analytics dashboards
- Caching layers
- Read-heavy applications
- Non-critical user data

### When to Use Strong Consistency
- Financial transactions
- Inventory management
- User authentication
- Critical business logic
- Legal/compliance data

## References

- [MongoDB Replication Documentation](https://docs.mongodb.com/manual/replication/)
- [Read Concern Documentation](https://docs.mongodb.com/manual/reference/read-concern/)
- [Write Concern Documentation](https://docs.mongodb.com/manual/reference/write-concern/)
- [PyMongo Documentation](https://pymongo.readthedocs.io/)
- [Docker Compose Documentation](https://docs.docker.com/compose/)

## License

This project is for educational purposes as part of a Distributed Systems course lab assignment.

---

**Created by:** Anush 
**Course:** Distributed Systems - Lab 2  
**Date:** October 2025