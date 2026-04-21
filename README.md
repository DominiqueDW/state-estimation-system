# Real-Time AI Vision System for Parking Occupancy

## Overview

This project implements a real-time AI vision system that detects and tracks vehicles from video input, maintains a persistent world state, and determines parking occupancy. The system is designed with a strong emphasis on **AI systems engineering principles**, separating perception from state estimation and logic.

> **Core Philosophy**  
> *World State is the product. AI provides observations.*

---

## Features

- Real-time vehicle detection (YOLO)
- Multi-object tracking (ByteTrack)
- State estimation using a Kalman Filter
- Homography-based world coordinate mapping
- Parking zone occupancy detection with temporal smoothing
- Dual visualization:
  - Camera view (pixel space)
  - Top-down world view
- REST API exposing system state (FastAPI)

---

## System Architecture

- Camera/Video
- Perception Layer (YOLO + ByteTrack)
- State Estimation Layer (Kalman Filter)
- Geometry Layer (Homography Mapping)
- Logic Layer (Occupancy Engine)
- API Layer (FastAPI)

---

## Key Concepts

### 1. Perception vs State

- **Perception** produces noisy observations (detections + track IDs)
- **State** maintains a stable belief of the world over time

---

### 2. World Coordinates

Pixel coordinates are transformed into **world coordinates** using homography:

- Enables consistent motion modeling
- Makes zone logic physically meaningful
- Removes perspective distortion

---

### 3. State Estimation

Each entity is modeled using a **Kalman Filter**:

- Predicts motion when observations are missing
- Smooths noisy detections
- Maintains velocity and uncertainty

---

### 4. Occupancy Logic

Parking zones are defined as polygons in world space.

Occupancy is determined by: entity inside zone -> occupied

To prevent flickering, a **temporal confidence model** is used:
- Confidence increases when a vehicle is present
- Decreases when absent
- Thresholds define stable occupancy

---

## Running the System

### 1. Install Dependencies

```bash
pip install ultralytics opencv-python supervision fastapi uvicorn numpy
```
### 2. Start the System

Run the API server (this also starts the main loop)

```bash
uvicorn api.server:app --reload
```

### 3. View API
 
 Open: http://127.0.0.1:8000/docs

 Avaliable endpoints:
 - /occupany
 - /entities
 - /health

 ---

 ## Perfromance Considerations

 The system is currently CPU-bound due to model inference.

 Performance depends on:
 - Model size (YOLO variant)
 - Input resolution
 - Hardware (CPU vs GPU)

 ---

 ## Current Limitations

 - Track IDs are not globally persistent (ByteTrack limitation)
 - Homography valid only within selected region
 - Single-camera system
 - No long-term identity re-identification

 ---

 ## Author Notes

 This project focuses not just on building a working system, but on understanding:
 - How perception integrates into larger systems
 - How to manage uncertainty over time
 - How to design maintainable AI pipelines

 ---
