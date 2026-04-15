import { useState } from "react";

const API = "http://34.204.82.138:8000";

export default function App() {
  const [logs, setLogs] = useState("");
  const [status, setStatus] = useState("");
  const [loading, setLoading] = useState(false);
  const [masterIp, setMasterIp] = useState("");

  const [form, setForm] = useState({
    clusterName: "",
    workers: 1,
    instanceType: "t2.medium",
    region: "us-east-1",
  });

  const handleChange = (e) => {
    const { name, value } = e.target;
    setForm({
      ...form,
      [name]: name === "workers" ? Number(value) : value,
    });
  };

  // =========================
  // CREATE CLUSTER
  // =========================
  const createCluster = async () => {
    setLoading(true);
    setLogs("🚀 Creating cluster...\n");

    try {
      const payload = {
        clusterName: form.clusterName,
        workers: Number(form.workers), // ✅ important fix
        instanceType: form.instanceType,
        region: form.region,
	k8sVersion: "1.29", 
	deployApp: false
      };

      console.log("📦 Payload:", payload);

      const res = await fetch(`${API}/create-cluster`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(payload),
      });

      const data = await res.json();

      console.log("📥 Response:", data);

      if (data.status === "success") {
        setLogs(data.logs || "✅ Cluster created successfully");

        // ✅ store master IP automatically
        setMasterIp(data.master.public_ip);
      } else {
        setLogs("❌ " + JSON.stringify(data));
      }
    } catch (err) {
      setLogs("❌ Request failed: " + err.message);
    }

    setLoading(false);
  };

  // =========================
  // GET STATUS
  // =========================
  const getStatus = async () => {
    if (!masterIp) {
      alert("⚠️ Create cluster first!");
      return;
    }

    const res = await fetch(`${API}/cluster-status/${masterIp}`);
    const data = await res.json();

    setStatus(`
NODES:
${data.nodes}

PODS:
${data.pods}
    `);
  };

  // =========================
  // DOWNLOAD KUBECONFIG
  // =========================
  const downloadConfig = () => {
    if (!masterIp) {
      alert("⚠️ Create cluster first!");
      return;
    }

    window.open(`${API}/download-kubeconfig/${masterIp}`);
  };

  // =========================
  // DELETE CLUSTER
  // =========================
  const deleteCluster = async () => {
    if (!form.clusterName) {
      alert("Enter cluster name");
      return;
    }

    await fetch(`${API}/delete-cluster/${form.clusterName}`, {
      method: "DELETE",
    });

    alert("🗑️ Cluster Deleted");
  };

  return (
    <div style={{ padding: 30 }}>
      <h1>🚀 K8s SaaS Dashboard</h1>

      {/* FORM */}
      <input
        name="clusterName"
        placeholder="Cluster Name"
        onChange={handleChange}
      />
      <br /><br />

      <input
        name="workers"
        type="number"
        value={form.workers}
        onChange={handleChange}
      />
      <br /><br />

      <select name="instanceType" onChange={handleChange}>
        <option value="t2.micro">t2.micro</option>
        <option value="t2.medium">t2.medium</option>
      </select>
      <br /><br />

      <select name="region" onChange={handleChange}>
        <option value="us-east-1">us-east-1</option>
        <option value="us-west-2">us-west-2</option>
      </select>

      <br /><br />

      {/* ACTION BUTTONS */}
      <button onClick={createCluster} disabled={loading}>
        {loading ? "Creating..." : "Create Cluster"}
      </button>

      <br /><br />

      <button onClick={getStatus}>📊 Get Status</button>
      <button onClick={downloadConfig}>⬇️ Download kubeconfig</button>
      <button onClick={deleteCluster}>🗑️ Delete Cluster</button>

      <br /><br />

      {/* SHOW MASTER IP */}
      {masterIp && (
        <p>
          🌐 Master IP: <b>{masterIp}</b>
        </p>
      )}

      {/* LOGS */}
      <h3>📜 Logs</h3>
      <textarea
        value={logs}
        readOnly
        rows={15}
        style={{
          width: "100%",
          background: "black",
          color: "lime",
          padding: "10px",
          fontFamily: "monospace",
        }}
      />

      {/* STATUS */}
      <h3>📊 Cluster Status</h3>
      <textarea
        value={status}
        readOnly
        rows={15}
        style={{ width: "100%" }}
      />
    </div>
  );
}
