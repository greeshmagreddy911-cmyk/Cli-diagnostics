# System Architecture

## Overview

The Student Report Generator is an automated Python application that processes student marks and generates result reports.

## Architecture Flow

```text
students.csv
     |
     v
Data Loader
     |
     v
Report Processor
     |
     v
Result Calculator
     |
     +------> student_report.json
     |
     v
FastAPI Backend
     |
     v
REST API /report

Scheduler
     |
     v
Automated Report Generation

CLI
     |
     v
Manual Report Generation
