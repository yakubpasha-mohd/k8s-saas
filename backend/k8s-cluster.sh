#!/bin/bash

set -e

MASTER_IP=$1
WORKER_IPS=$2

KEY_PATH="/app/key.pem"
SSH_USER="ec2-user"

echo "🚀 Starting Kubernetes Cluster Setup"
echo "MASTER: $MASTER_IP"
echo "WORKERS: $WORKER_IPS"

# =========================
# WAIT FOR SSH
# =========================
echo "⏳ Waiting for SSH to be ready..."

until ssh -i $KEY_PATH -o StrictHostKeyChecking=no $SSH_USER@$MASTER_IP "echo connected" 2>/dev/null; do
  echo "Waiting for master SSH..."
  sleep 5
done

# =========================
# FUNCTION: SETUP NODE
# =========================
setup_node() {
  NODE=$1

  echo "🔧 Setting up node: $NODE"

  ssh -i $KEY_PATH -o StrictHostKeyChecking=no $SSH_USER@$NODE "
    set -xe

    echo '📦 Updating system'
    sudo yum update -y

    echo '📦 Installing Docker'
    sudo amazon-linux-extras install docker -y
    sudo systemctl enable docker
    sudo systemctl start docker

    echo '🛑 Disabling swap'
    sudo swapoff -a

    echo '📦 Adding Kubernetes repo'
    sudo bash -c 'cat > /etc/yum.repos.d/kubernetes.repo <<EOT
[kubernetes]
name=Kubernetes
baseurl=https://pkgs.k8s.io/core:/stable:/v1.29/rpm/
enabled=1
gpgcheck=0
EOT'

    echo '📦 Installing Kubernetes tools'
    sudo yum install -y kubelet kubeadm kubectl

    echo '🚀 Starting kubelet'
    sudo systemctl enable kubelet
    sudo systemctl start kubelet

    echo '✅ kubectl location:'
    which kubectl || echo 'kubectl not found'
  "
}

# =========================
# SETUP MASTER + WORKERS
# =========================
setup_node $MASTER_IP

IFS=',' read -ra WORKERS <<< "$WORKER_IPS"
for ip in "${WORKERS[@]}"; do
  setup_node $ip
done

# =========================
# INIT MASTER
# =========================
echo "⚙️ Initializing Kubernetes Master..."

ssh -i $KEY_PATH -o StrictHostKeyChecking=no $SSH_USER@$MASTER_IP "
  set -xe

  echo '🚀 Running kubeadm init'

  sudo kubeadm init --pod-network-cidr=10.244.0.0/16 | tee /home/ec2-user/kube-init.log

  echo '📁 Setting kubeconfig'

  mkdir -p \$HOME/.kube
  sudo cp /etc/kubernetes/admin.conf \$HOME/.kube/config
  sudo chown ec2-user:ec2-user \$HOME/.kube/config

  echo '🌐 Installing Flannel network'

  kubectl apply -f https://raw.githubusercontent.com/coreos/flannel/master/Documentation/kube-flannel.yml

  echo '🔑 Creating join command'

  kubeadm token create --print-join-command > /home/ec2-user/join.sh
"

# =========================
# COPY JOIN COMMAND
# =========================
scp -i $KEY_PATH -o StrictHostKeyChecking=no $SSH_USER@$MASTER_IP:/home/ec2-user/join.sh ./join.sh

JOIN_CMD=$(cat join.sh)

echo "🔗 Join command: $JOIN_CMD"

# =========================
# JOIN WORKERS
# =========================
for ip in "${WORKERS[@]}"; do
  echo "🔗 Joining worker: $ip"

  ssh -i $KEY_PATH -o StrictHostKeyChecking=no $SSH_USER@$ip "
    sudo $JOIN_CMD
  "
done

echo "🎉 Kubernetes Cluster Setup Complete!"
