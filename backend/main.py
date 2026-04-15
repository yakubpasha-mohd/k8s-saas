from fastapi import FastAPI
from datetime import datetime
import subprocess
import boto3
import paramiko

from models import ClusterRequest
from database import clusters_collection
from aws import create_instance
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.responses import StreamingResponse
app = FastAPI()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

KEY_PATH = "/app/key.pem"


# =========================
# SSH HELPER
# =========================
def run_ssh_command(ip, command):
    key = paramiko.RSAKey.from_private_key_file(KEY_PATH)

    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(ip, username="ec2-user", pkey=key)

    stdin, stdout, stderr = ssh.exec_command(command)

    output = stdout.read().decode()
    error = stderr.read().decode()

    ssh.close()

    return output, error

# =========================
# STREAM LOGS FUNCTION
# =========================
def stream_k8s_logs(master_ip, worker_ips):
    process = subprocess.Popen(
        ["bash", "k8s-cluster.sh", master_ip, worker_ips],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        bufsize=1
    )

    for line in iter(process.stdout.readline, ''):
        yield line
# =========================
# CREATE CLUSTER
# =========================
@app.post("/create-cluster")
def create_cluster(req: ClusterRequest):
    try:
        master = create_instance(
            req.instanceType,
            f"{req.clusterName}-master",
            req.region
        )

        workers = []
        for i in range(req.workers):
            w = create_instance(
                req.instanceType,
                f"{req.clusterName}-worker-{i+1}",
                req.region
            )
            workers.append(w)

        worker_ips = ",".join([w["public_ip"] for w in workers])

        result = subprocess.run(
            ["bash", "k8s-cluster.sh", master["public_ip"], worker_ips],
            capture_output=True,
            text=True
        )

        clusters_collection.insert_one({
            "clusterName": req.clusterName,
            "master": master,
            "workers": workers,
            "logs": result.stdout,
            "errors": result.stderr,
            "createdAt": datetime.utcnow()
        })

        return {
            "status": "success",
            "master": master,
            "workers": workers,
            "logs": result.stdout,
            "errors": result.stderr
        }

    except Exception as e:
        return {"status": "error", "error": str(e)}

# =========================
# STREAM CLUSTER LOGS
# =========================
@app.get("/stream-cluster")
def stream_cluster(master_ip: str, worker_ips: str):
    return StreamingResponse(
        stream_k8s_logs(master_ip, worker_ips),
        media_type="text/plain"
    )
# =========================
# CLUSTER STATUS
# =========================
@app.get("/cluster-status/{ip}")
def cluster_status(ip: str):
    try:
        nodes, _ = run_ssh_command(ip, "kubectl get nodes -o wide")
        pods, _ = run_ssh_command(ip, "kubectl get pods -A")

        return {
            "nodes": nodes,
            "pods": pods,
            "health": "healthy"
        }

    except Exception as e:
        return {"status": "error", "error": str(e)}


# =========================
# DOWNLOAD KUBECONFIG
# =========================
@app.get("/download-kubeconfig/{ip}")
def download_kubeconfig(ip: str):
    key = paramiko.RSAKey.from_private_key_file(KEY_PATH)

    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(ip, username="ec2-user", pkey=key)

    sftp = ssh.open_sftp()
    sftp.get("/home/ec2-user/.kube/config", "/tmp/kubeconfig")

    ssh.close()

    return FileResponse("/tmp/kubeconfig", filename="kubeconfig")


# =========================
# DELETE CLUSTER
# =========================
@app.delete("/delete-cluster/{name}")
def delete_cluster(name: str):
    ec2 = boto3.client("ec2")

    res = ec2.describe_instances(
        Filters=[
            {"Name": "tag:Name", "Values": [f"{name}*"]}
        ]
    )

    ids = []
    for r in res["Reservations"]:
        for i in r["Instances"]:
            ids.append(i["InstanceId"])

    if ids:
        ec2.terminate_instances(InstanceIds=ids)

    return {"status": "deleted", "instances": ids}


# =========================
# GET ALL CLUSTERS
# =========================
@app.get("/clusters")
def get_clusters():
    return list(clusters_collection.find({}, {"_id": 0}))
