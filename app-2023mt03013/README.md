# Devops for Cloud Assignment — Strict Pack (Roll: 2023mt03013)

This pack implements only the required features, matching the assignment exactly.

## Local run
```
cd app-2023mt03013
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python main.py
# http://localhost:8000/get_info
# http://localhost:8000/metrics
```

## Docker
```
docker build -t img-2023mt03013:strict .
docker run --rm -p 8000:8000 --name cnr-2023mt03013   -e APP_VERSION=1.0 -e APP_TITLE="Devops for Cloud Assignment"   img-2023mt03013:strict
```

## AWS ECR + EKS
1) Create ECR and push image:
```
aws ecr create-repository --repository-name img-2023mt03013
aws ecr get-login-password --region <REGION> | docker login --username AWS --password-stdin <ACCOUNT_ID>.dkr.ecr.<REGION>.amazonaws.com

docker tag img-2023mt03013:strict <ACCOUNT_ID>.dkr.ecr.<REGION>.amazonaws.com/img-2023mt03013:strict
docker push <ACCOUNT_ID>.dkr.ecr.<REGION>.amazonaws.com/img-2023mt03013:strict
```

2) Edit `k8s/dep-2023mt03013.yaml` to set your ECR image (line 'image:').

3) Apply manifests:
```
kubectl apply -f k8s/config-2023mt03013.yaml
kubectl apply -f k8s/dep-2023mt03013.yaml
kubectl apply -f k8s/svc-2023mt03013.yaml
kubectl get pods -o wide
kubectl get svc svc-2023mt03013
```

## Prometheus
```
kubectl apply -f prometheus/prometheus-config.yaml
kubectl apply -f prometheus/prometheus-deploy.yaml
kubectl -n monitoring port-forward svc/prometheus 9090:9090
# Then query:
#   get_info_requests_total
#   process_cpu_percent
#   process_rss_bytes
```

## Structure
```
app-2023mt03013/
  main.py
  requirements.txt
  Dockerfile
  k8s/
    config-2023mt03013.yaml
    dep-2023mt03013.yaml
    svc-2023mt03013.yaml
  prometheus/
    prometheus-config.yaml
    prometheus-deploy.yaml
  README.md
```
