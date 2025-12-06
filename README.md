# Django Blog Deployment

Production-ready Django blog demonstrating advanced DevOps skills in containerization, CI/CD, GitOps and monitoring.

---

## 🚀 Skills Demonstrated

### **Infrastructure as Code & GitOps**

* Docker multi-service architecture (Docker Compose)
* Ansible automation for provisioning and application deployment
* GitOps workflow for automated staging deployments
* Infrastructure configuration as code (Nginx, Prometheus, Grafana)

### **Monitoring & Observability**

* Prometheus metrics collection (application + infrastructure)
* Grafana dashboards and alerting
* Health-check monitoring
* Log aggregation and service insights

### **Production Deployment**

* Nginx reverse proxy with load balancing support
* Gunicorn WSGI server with worker optimization
* Multi-container Docker orchestration
* Persistent storage via Docker volumes

### **CI/CD Pipeline**

* GitLab CI/CD pipeline for automated testing, building, and deployment
* Docker-in-Docker execution environment
* Multi-stage Docker image builds
* Automated deployment to staging environments

### **Configuration Management**

* Ansible roles for clean, reproducible infrastructure
* Environment-specific staging/production configs
* Secrets via environment variables
* Automated server provisioning

---

## 🛠️ Tech Stack

| Component             | Technology                      |
| --------------------- | ------------------------------- |
| **Application**       | Django 4.x + Gunicorn           |
| **Web Server**        | Nginx                           |
| **Containers**        | Docker + Docker Compose         |
| **CI/CD**             | GitLab CI/CD                    |
| **Monitoring**        | Prometheus + Grafana            |
| **Database**          | PostgreSQL (prod), SQLite (dev) |
| **Config Management** | Ansible                         |
| **Infrastructure**    | GitOps workflow                 |

---

## 📁 Project Structure

```
django-blog-production/
├── src/                          # Django application
├── infra/                        # Infrastructure as Code
│   ├── ansible/                  # Ansible automation (IaC)
│   ├── docker/                   # Docker configuration
│   ├── monitoring/               # Prometheus & Grafana
│   └── nginx/                    # Nginx proxy configuration
├── .gitlab-ci.yml                # GitLab CI/CD pipeline
└── README.md                     # Documentation
```

---

## 🔄 GitOps Workflow with Ansible

### Automated Staging Deployment

```bash
ansible-playbook -i infra/ansible/inventories/hosts.ini \
                 infra/ansible/staging-deploy.yaml
```

### Ansible Roles

* **setup-server** — base server config, users, firewall
* **docker** — Docker CE installation + Compose
* **app** — Django deployment, env vars, service orchestration

### Infrastructure States

* **Staging:** fully automated deployment via GitLab CI/CD
* **Production:** CI/CD-ready environment

---

## 🚦 CI/CD Pipeline

### GitLab Stages

```yaml
stages:
  - test
  - build
  - deploy
```

### Pipeline Features

* ✔ Automated unit tests on push
* ✔ Docker image build + optimization
* ✔ Deployment to staging via GitOps
* ✔ Health checks and service validation

---

## 📊 Monitoring Stack

### Prometheus

* Django app metrics (django-prometheus)
* cAdvisor container metrics
* Node Exporter server metrics

### Grafana

* Performance dashboards
* Infrastructure health visualization
* Custom alerting rules

---

## 🔮 Future Enhancements

* Kubernetes deployment manifests
* Terraform for cloud provisioning
* Loki + Tempo for logging and distributed tracing

---

## 👤 Author

**Mikhail Ivchuk — DevOps Engineer**
