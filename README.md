# 🚀 Dockerized Python and PostgreSQL Analytics App

A simple two-container application using **Docker Compose** to run a Python analytics script against a PostgreSQL database.

---

## 📌 What it Does
This project sets up a complete environment with two services:

- **PostgreSQL Service**:  
  A container running a PostgreSQL database, automatically initialized with a `trips` table and sample data on startup.

- **Python Service**:  
  A container that runs a Python script to:
  - Connect to the database  
  - Calculate statistics (total trips, average fare, top trips by duration)  
  - Save the results  

---

## 🛠️ How to Run

### Prerequisites
- [Docker](https://docs.docker.com/get-docker/)  
- [Docker Compose](https://docs.docker.com/compose/) (Included with Docker Desktop)

### 1. Build and Run the Stack
Open your terminal in the project’s root directory and run your preferred command:`

**using Docker Compose directly:**

```bash
docker compose up --build
```

### 2. Stop and Clean Up

To stop the containers and remove all associated networks and volumes, run:

```bash
make down
```

---

## ✅ Example Output

After the services start, the Python script will print the following JSON summary to your console (`stdout`):

```json
=== Trip Summary ===
{
  "total_trips": 6,
  "avg_fare_by_city": [
    {
      "city": "Charlotte",
      "avg_fare": 16.25
    },
    {
      "city": "New York",
      "avg_fare": 19.0
    },
    {
      "city": "San Francisco",
      "avg_fare": 20.25
    }
  ],
  "top_5_longest_trips": [
    {
      "city": "San Francisco",
      "minutes": 28,
      "fare": 29.3
    },
    {
      "city": "New York",
      "minutes": 26,
      "fare": 27.1
    },
    {
      "city": "Charlotte",
      "minutes": 21,
      "fare": 20.0
    },
    {
      "city": "Charlotte",
      "minutes": 12,
      "fare": 12.5
    },
    {
      "city": "San Francisco",
      "minutes": 11,
      "fare": 11.2
    }
  ]
}
```

---

## 📁 Output File Location

The final JSON summary is also saved as a file in the `out/` directory at the root of the project:

```
./out/summary.json
```

---

## 🔍 Troubleshooting

* **DB not ready**:
  The Python application includes a connection retry mechanism. If it fails, ensure no other service is using port `5432` on your machine.

* **Permission on `out/`**:
  If you see a permission error when the app tries to write the summary file, ensure you have write permissions for the `out/` directory on your host machine.



