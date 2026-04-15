from pydantic import BaseModel

class ClusterRequest(BaseModel):
    clusterName: str
    workers: int
    instanceType: str
    k8sVersion: str
    region: str
    deployApp: bool
