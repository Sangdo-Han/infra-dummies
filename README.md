# Infra for dummies

For dummies deploy wierd jobs (local) 

## programming language
- python

## test by using
- docker
- minikube
- metallb (for external)

## Docker Hub

docker build -t sanhan2/dummiest-streamlit-front .
docker push sanhan2/dummiest-streamlit-front

docker build -t sanhan2/dummiest-fastapi1 . 
docker push sanhan2/dummiest-fastapi1

docker build -t sanhan2/dummiest-fastapi2 .
docker push sanhan2/dummiest-fastapi2

### K8S

minikube 

on-premise lb 설정 (metallb)
```bash
kubectl apply -f https://raw.githubusercontent.com/metallb/metallb/v0.13.7/config/manifests/metallb-native.yaml
```

metallb 범위 설정
```yaml
apiVersion: metallb.io/v1beta1
kind: IPAddressPool
metadata:
  name: first-pool
  namespace: metallb-system
spec:
  addresses:
  - 192.168.49.50-192.168.49.200  # minikube IP (192.168.49.1) 제외, 192.168.49.2 부터 사용
---
apiVersion: metallb.io/v1beta1
kind: L2Advertisement
metadata:
  name: first-adv
  namespace: metallb-system
spec:
  ipAddressPools:
  - first-pool
---
apiVersion: metallb.io/v1beta1
kind: L2Advertisement
metadata:
  name: first-adv
  namespace: metallb-system
spec:
  ipAddressPools:
  - first-pool
```

namespace 설정

```yaml
apiVersion: v1
kind: Namespace
metadata:
  name: dummiest
```

FastAPI 1 서비스
fastapi1-deployment.yaml:
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: fastapi-1-deployment
  namespace: dummiest
spec:
  replicas: 1
  selector:
    matchLabels:
      app: fastapi1
  template:
    metadata:
      labels:
        app: fastapi1
    spec:
      containers:
      - name: fastapi1
        image: sanhan2/dummiest-fastapi1
        ports:
        - containerPort: 8000
        resources:
          requests:
            memory: "256Mi"   # 최소 메모리 요청
            cpu: "250m"       # 최소 CPU 요청
          limits:
            memory: "512Mi"   # 최대 메모리 제한
            cpu: "500m"       # 최대 CPU 제한
---
apiVersion: v1
kind: Service
metadata:
  name: fastapi-1-service
  namespace: dummiest
spec:
  selector:
    app: fastapi1
  ports:
  - protocol: TCP
    port: 8000
    targetPort: 8000
  type: ClusterIP
```

FastAPI 2 서비스
fastapi2-deployment.yaml:

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: fastapi-2-deployment
  namespace: dummiest
spec:
  replicas: 1
  selector:
    matchLabels:
      app: fastapi2
  template:
    metadata:
      labels:
        app: fastapi2
    spec:
      containers:
      - name: fastapi2
        image: sanhan2/dummiest-fastapi2
        ports:
        - containerPort: 8000
        resources:
          requests:
            memory: "256Mi"   # 최소 메모리 요청
            cpu: "250m"       # 최소 CPU 요청
          limits:
            memory: "512Mi"   # 최대 메모리 제한
            cpu: "500m"       # 최대 CPU 제한
---
apiVersion: v1
kind: Service
metadata:
  name: fastapi-2-service
  namespace: dummiest
spec:
  selector:
    app: fastapi2
  ports:
  - protocol: TCP
    port: 8000
    targetPort: 8000
  type: ClusterIP
```

Streamlit 서비스 리소스 정의
streamlit-deployment.yaml:

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: streamlit-deployment
  namespace: dummiest
spec:
  replicas: 1
  selector:
    matchLabels:
      app: streamlit
  template:
    metadata:
      labels:
        app: streamlit
    spec:
      containers:
      - name: streamlit
        image: sanhan2/dummiest-streamlit-front
        ports:
        - containerPort: 8501
        resources:
          requests:
            memory: "256Mi"   # 최소 메모리 요청
            cpu: "250m"       # 최소 CPU 요청
          limits:
            memory: "512Mi"   # 최대 메모리 제한
            cpu: "500m"       # 최대 CPU 제한
---
apiVersion: v1
kind: Service
metadata:
  name: streamlit-service
  namespace: dummiest
spec:
  selector:
    app: streamlit
  ports:
  - protocol: TCP
    port: 30080  # 서비스 포트를 30080으로 변경 (30000번대)
    targetPort: 8501
    nodePort: 30080 # 노드 포트도 명시적으로 30080으로 지정 (선택 사항)
  type: LoadBalancer  # 외부에 노출
  loadBalancerIP: 192.168.49.103 # MetalLB 고정 IP
```
