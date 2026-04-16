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

  const createCluster = async () => {
    setLoading(true);
    setLogs("🚀 Creating cluster...\n");

    try {
      const payload = {
        clusterName: form.clusterName,
        workers: Number(form.workers),
        instanceType: form.instanceType,
        region: form.region,
        k8sVersion: "1.29",
        deployApp: false,
      };

      const res = await fetch(`${API}/create-cluster`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(payload),
      });

      const data = await res.json();

      if (data.status === "success") {
        setLogs(data.logs || "✅ Cluster created successfully");
        setMasterIp(data.master.public_ip);
      } else {
        setLogs("❌ " + JSON.stringify(data));
      }
    } catch (err) {
      setLogs("❌ " + err.message);
    }

    setLoading(false);
  };

  const getStatus = async () => {
    if (!masterIp) return alert("Create cluster first");

    const res = await fetch(`${API}/cluster-status/${masterIp}`);
    const data = await res.json();

    setStatus(`NODES:\n${data.nodes}\n\nPODS:\n${data.pods}`);
  };

  const downloadConfig = () => {
    if (!masterIp) return alert("Create cluster first");
    window.open(`${API}/download-kubeconfig/${masterIp}`);
  };

  const deleteCluster = async () => {
    if (!form.clusterName) return alert("Enter cluster name");

    await fetch(`${API}/delete-cluster/${form.clusterName}`, {
      method: "DELETE",
    });

    alert("Deleted");
  };

  return (
    <div className="min-h-screen bg-gray-50 p-6 flex justify-center">
      <div className="w-full max-w-4xl space-y-6">

        <h1 className="text-3xl font-bold">
          🚀 K8s SaaS Dashboard
        </h1>

        {/* FORM */}
        <div className="bg-white shadow rounded-2xl p-6 grid gap-4">
          <input
            name="clusterName"
            placeholder="Cluster Name"
            onChange={handleChange}
            className="border rounded-xl px-3 py-2"
          />

          <input
            name="workers"
            type="number"
            value={form.workers}
            onChange={handleChange}
            className="border rounded-xl px-3 py-2"
          />

          <select
            name="instanceType"
            onChange={handleChange}
            className="border rounded-xl px-3 py-2"
          >
            <option value="t2.micro">t2.micro</option>
            <option value="t2.medium">t2.medium</option>
          </select>

          <select
            name="region"
            onChange={handleChange}
            className="border rounded-xl px-3 py-2"
          >
            <option value="us-east-1">us-east-1</option>
            <option value="us-west-2">us-west-2</option>
          </select>
        </div>

        {/* BUTTONS */}
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
          <button
            onClick={createCluster}
            className="bg-blue-600 text-white py-2 rounded-xl"
          >
            {loading ? "Creating..." : "Create"}
          </button>

          <button
            onClick={getStatus}
            className="bg-indigo-500 text-white py-2 rounded-xl"
          >
            Status
          </button>

          <button
            onClick={downloadConfig}
            className="bg-green-500 text-white py-2 rounded-xl"
          >
            Kubeconfig
          </button>

          <button
            onClick={deleteCluster}
            className="bg-red-500 text-white py-2 rounded-xl"
          >
            Delete
          </button>
        </div>

        {/* LOGS */}
        <textarea
          value={logs}
          readOnly
          className="w-full h-40 bg-black text-green-400 p-3 rounded-xl"
        />

        {/* STATUS */}
        <textarea
          value={status}
          readOnly
          className="w-full h-40 border p-3 rounded-xl"
        />

      </div>
    </div>
  );
}
