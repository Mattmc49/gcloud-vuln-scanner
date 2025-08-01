# gcloud-vuln-scanner 

A lightweight, extensible Python tool to discover common misconfigurations in your Google Cloud Platform (GCP) projects. Run it interactively in Cloud Shell or automate it via GitHub Actions to get continuous visibility into firewall rules, public buckets, IAM issues, and more.

---

## 🚀 Features

- **Firewall auditing**  
  Detects rules allowing 0.0.0.0/0 (all-open ingress/egress).

- **Cloud Storage inspection**  
  Lists buckets with `allUsers` or `allAuthenticatedUsers` ACLs.

- **Service account checks**  
  Flags disabled or overly-privileged service accounts.

- **JSON & human-readable output**  
  Write detailed `report.json` and view summary tables on the console.

- **GitHub Actions workflow**  
  Schedule weekly or on-push scans and archive scan reports as CI artifacts.

---

## 🔧 Prerequisites

- **Google Cloud SDK** (pre-installed in Cloud Shell)  
- **Python 3.9+**  
- **A GCP Project** with the following IAM permissions granted to your service account or user:
  - `compute.firewalls.list`
  - `storage.buckets.list`
  - `storage.buckets.getIamPolicy`
  - `iam.serviceAccounts.list`
- **GitHub repository** (for CI integration)

---

## ⚙️ Installation

1. **Clone the repo**  
> git clone https://github.com/<your-org>/gcloud-vuln-scanner.git
> cd gcloud-vuln-scanner
2. **Create & activate a virtual environment**
> python3 -m venv .venv
>  source .venv/bin/activate
3. **Install dependencies**
> pip install --upgrade pip
> pip install -r requirements.txt

## 🔑 Authentication:
Launch the Interactive Cloud Shell:

> gcloud auth login
> gcloud config set project YOUR_GCP_PROJECT_ID

--project: (your GCP project ID)
--output: path to write the JSON report (default: report.json)

1. Create a JSON key for a service account with the required roles.
2. Add the JSON as a GitHub secret named GCP_SA_KEY.
3. (Workflow will decode and activate it.)

## 🏃 Usage: 
```bash 
Copy
Edit
python3 -m scanner.scanner \
  --project YOUR_GCP_PROJECT_ID \
  --output report.json
--project: your GCP project ID
--output: path to write the JSON report (default: report.json)

**Sample Output:** 
text
Copy
Edit
=== firewalls (2) ===
NAME           DIRECTION    ALLOWS
default-allow HTTP:80,443    INGRESS
my-everywhere ALL:0–65535     INGRESS

=== public_buckets (1) ===
NAME              ROLE
public-assets     READER

=== disabled_service_accounts (0) ===
None found.

Report written to report.json
