import { useEffect, useRef, useState } from "react";

const API =
  import.meta.env.VITE_API_URL ||
  "http://34.204.82.138:8000";

const REGIONS = [
  "us-east-1",
  "us-east-2",
  "us-west-2",
  "eu-west-1",
  "eu-central-1",
  "ap-south-1",
  "ap-southeast-1",
];

export default function App() {
  // =====================================================
  // STATE
  // =====================================================
  const [dark, setDark] =
    useState(false);

  const [loading, setLoading] =
    useState(false);

  const [logs, setLogs] =
    useState("");

  const [status, setStatus] =
    useState("");

  const [jobId, setJobId] =
    useState("");

  const [jobData, setJobData] =
    useState(null);

  const [jobStatus, setJobStatus] =
    useState("idle");

  const [masterIp, setMasterIp] =
    useState("");

  const streamRef = useRef(null);
  const pollRef = useRef(null);
  const logRef = useRef(null);

  const [form, setForm] =
    useState({
      clusterName: "",
      workers: 1,
      instanceType:
        "t3.medium",
      region: "us-east-1",
    });

  const [
    selectedRegions,
    setSelectedRegions,
  ] = useState([
    "us-east-1",
    "us-east-2",
  ]);

  // =====================================================
  // THEME
  // =====================================================
  const page = dark
    ? "bg-slate-950 text-white"
    : "bg-slate-100 text-slate-900";

  const card = dark
    ? "bg-slate-900 border-slate-800"
    : "bg-white border-slate-200";

  const input = dark
    ? "bg-slate-950 border-slate-700 text-white"
    : "bg-white border-slate-300";

  // =====================================================
  // CLEANUP
  // =====================================================
  useEffect(() => {
    return () => {
      if (
        streamRef.current
      )
        streamRef.current.close();

      if (
        pollRef.current
      )
        clearInterval(
          pollRef.current
        );
    };
  }, []);

  useEffect(() => {
    if (logRef.current) {
      logRef.current.scrollTop =
        logRef.current
          .scrollHeight;
    }
  }, [logs]);

  // =====================================================
  // FORM
  // =====================================================
  const handleChange = (e) => {
    const {
      name,
      value,
    } = e.target;

    setForm({
      ...form,
      [name]:
        name ===
        "workers"
          ? Number(
              value
            )
          : value,
    });
  };

  const toggleRegion = (
    region
  ) => {
    if (
      selectedRegions.includes(
        region
      )
    ) {
      setSelectedRegions(
        selectedRegions.filter(
          (r) =>
            r !== region
        )
      );
    } else {
      setSelectedRegions([
        ...selectedRegions,
        region,
      ]);
    }
  };

  // =====================================================
  // COMMON
  // =====================================================
  const resetJob = () => {
    setLogs("");
    setStatus("");
    setJobData(null);
    setJobId("");
    setLoading(true);
    setJobStatus(
      "running"
    );
  };

  // =====================================================
  // SINGLE REGION
  // =====================================================
  const createCluster =
    async () => {
      resetJob();

      try {
        const res =
          await fetch(
            `${API}/create-cluster`,
            {
              method:
                "POST",
              headers: {
                "Content-Type":
                  "application/json",
              },
              body: JSON.stringify(
                {
                  clusterName:
                    form.clusterName,
                  workers:
                    Number(
                      form.workers
                    ),
                  instanceType:
                    form.instanceType,
                  region:
                    form.region,
                  k8sVersion:
                    "1.29",
                  deployApp:
                    false,
                }
              ),
            }
          );

        const data =
          await res.json();

        if (
          data.jobId
        ) {
          setJobId(
            data.jobId
          );

          startPolling(
            data.jobId
          );

          startLogs(
            data.jobId
          );
        } else {
          setLogs(
            "❌ Failed to start job"
          );

          setLoading(
            false
          );
        }
      } catch (e) {
        setLogs(
          "❌ " +
            e.message
        );

        setLoading(
          false
        );
      }
    };

  // =====================================================
  // MULTI REGION
  // =====================================================
const createMultiRegion = async () => {
  resetJob();
  setLoading(true);

  try {
    const payload = {
      clusterName: form.clusterName,
      workers: Number(form.workers),
      instanceType: form.instanceType,
      regions: selectedRegions,
      k8sVersion: form.k8sVersion || "1.29",
    };

    console.log("Multi-region payload:", payload);

    const res = await fetch(
      `${API}/create-multi-region`,
      {
        method: "POST",
        headers: {
          "Content-Type":
            "application/json",
        },
        body: JSON.stringify(
          payload
        ),
      }
    );

    const data =
      await res.json();

    if (data.jobId) {
      setJobId(data.jobId);

      startPolling(
        data.jobId
      );

      startLogs(
        data.jobId
      );
    } else {
      setLogs(
        "❌ Failed to start job"
      );

      setLoading(false);
    }
  } catch (e) {
    setLogs(
      "❌ " + e.message
    );

    setLoading(false);
  }
};
  // =====================================================
  // POLLING
  // =====================================================
  const startPolling = (
    id
  ) => {
    if (
      pollRef.current
    ) {
      clearInterval(
        pollRef.current
      );
    }

    pollRef.current =
      setInterval(
        async () => {
          try {
            const res =
              await fetch(
                `${API}/jobs/${id}`
              );

            const data =
              await res.json();

            setJobData(
              data
            );

            if (
              data
                .master_ip
            ) {
              setMasterIp(
                data.master_ip
              );
            }

            if (
              data.status ===
              "completed"
            ) {
              setLoading(
                false
              );

              setJobStatus(
                "completed"
              );

              clearInterval(
                pollRef.current
              );
            }

            if (
              data.status ===
              "failed"
            ) {
              setLoading(
                false
              );

              setJobStatus(
                "failed"
              );

              clearInterval(
                pollRef.current
              );
            }
          } catch {}
        },
        3000
      );
  };

  // =====================================================
  // LIVE LOGS
  // =====================================================
const startLogs = (id) => {
  if (streamRef.current) {
    streamRef.current.close();
  }

  const es = new EventSource(
    `${API}/jobs/${id}/stream`
  );

  es.onopen = () => {
    setLogs(
      "Connected to live stream...\n"
    );
  };

  es.onmessage = (event) => {
    const line =
      event.data?.trim();

    if (!line) return;

    setLogs((prev) =>
      prev + line + "\n"
    );

    // ---------------------------------
    // FINAL SUCCESS (single region)
    // ---------------------------------
    if (
      line.includes(
        "🎉 Single cluster deployment complete"
      )
    ) {
      setLoading(false);
      setJobStatus("completed");
      es.close();
      return;
    }

    // ---------------------------------
    // FINAL SUCCESS (multi region)
    // ---------------------------------
    if (
      line.includes(
        "🌍 Multi-region deployment complete"
      )
    ) {
      setLoading(false);
      setJobStatus("completed");
      es.close();
      return;
    }

    // ---------------------------------
    // FAILURE
    // ---------------------------------
    if (
      line.includes("❌ ERROR") ||
      line.includes("failed")
    ) {
      setLoading(false);
      setJobStatus("failed");
      es.close();
      return;
    }
  };

  es.onerror = () => {
    es.close();
  };

  streamRef.current = es;
};
  // =====================================================
  // ACTIONS
  // =====================================================
  const getStatus =
    async () => {
      if (!masterIp)
        return;

      const res =
        await fetch(
          `${API}/cluster-status/${masterIp}`
        );

      const data =
        await res.json();

      setStatus(`
NODES:
${data.nodes}

PODS:
${data.pods}
`);
    };

  const downloadConfig =
    () => {
      if (!masterIp)
        return;

      window.open(
        `${API}/download-kubeconfig/${masterIp}`
      );
    };

  const deleteCluster =
    async () => {
      if (
        !form.clusterName
      )
        return;

      await fetch(
        `${API}/delete-cluster/${form.clusterName}`,
        {
          method:
            "DELETE",
        }
      );

      alert(
        "Cluster Deleted"
      );
    };

  // =====================================================
  // HELPERS
  // =====================================================
  const progress =
    loading
      ? 65
      : jobStatus ===
        "completed"
      ? 100
      : 0;

  const badge = (
    val
  ) => {
    if (
      val ===
      "completed"
    )
      return "bg-green-500";

    if (
      val ===
      "failed"
    )
      return "bg-red-500";

    if (
      val ===
      "running"
    )
      return "bg-blue-500";

    return "bg-slate-400";
  };

  // =====================================================
  // UI
  // =====================================================
  return (
    <div
      className={`min-h-screen ${page}`}
    >
      <div className="flex">

        {/* SIDEBAR */}
        <aside
          className={`hidden lg:flex w-72 min-h-screen border-r p-6 flex-col gap-6 ${card}`}
        >
          <div>
            <h1 className="text-2xl font-bold">
              ☸ K8s SaaS
            </h1>

            <p className="text-sm opacity-70">
              Enterprise Platform
            </p>
          </div>

          <nav className="space-y-2">
            {[
              "Dashboard",
              "Clusters",
              "Logs",
              "Monitoring",
              "Settings",
            ].map(
              (
                item
              ) => (
                <div
                  key={
                    item
                  }
                  className="p-3 rounded-xl hover:bg-blue-600 hover:text-white cursor-pointer"
                >
                  {
                    item
                  }
                </div>
              )
            )}
          </nav>

          <button
            onClick={() =>
              setDark(
                !dark
              )
            }
            className="mt-auto py-3 rounded-xl bg-slate-700 text-white"
          >
            {dark
              ? "☀ Light"
              : "🌙 Dark"}
          </button>
        </aside>

        {/* MAIN */}
        <main className="flex-1 p-6 space-y-6">

          {/* HEADER */}
          <div
            className={`rounded-2xl border p-6 ${card}`}
          >
            <h2 className="text-3xl font-bold">
              🚀 Premium Cluster Dashboard
            </h2>

            <p className="opacity-70 mt-2">
              Real-Time Kubernetes Provisioning Platform
            </p>
          </div>

          {/* METRICS */}
          <div className="grid md:grid-cols-4 gap-4">
            <Metric
              title="Progress"
              value={`${progress}%`}
              color="bg-purple-600"
              card={
                card
              }
            />

            <Metric
              title="Regions"
              value={
                selectedRegions.length
              }
              color="bg-blue-600"
              card={
                card
              }
            />

            <Metric
              title="Job"
              value={
                jobStatus
              }
              color={badge(
                jobStatus
              )}
              card={
                card
              }
            />

            <Metric
              title="Logs"
              value={
                logs
                  .split(
                    "\n"
                  )
                  .filter(
                    Boolean
                  ).length
              }
              color="bg-orange-600"
              card={
                card
              }
            />
          </div>

          {/* FORM */}
          <div className="grid xl:grid-cols-2 gap-6">

            <div
              className={`rounded-2xl border p-6 space-y-4 ${card}`}
            >
              <h3 className="text-xl font-semibold">
                Create Cluster
              </h3>

              <input
                name="clusterName"
                placeholder="Cluster Name"
                onChange={
                  handleChange
                }
                className={`w-full border rounded-xl px-4 py-3 ${input}`}
              />

              <input
                name="workers"
                type="number"
                value={
                  form.workers
                }
                onChange={
                  handleChange
                }
                className={`w-full border rounded-xl px-4 py-3 ${input}`}
              />

              <select
                name="instanceType"
                onChange={
                  handleChange
                }
                className={`w-full border rounded-xl px-4 py-3 ${input}`}
              >
                <option>
                  t3.medium
                </option>
                <option>
                  t3.large
                </option>
                <option>
                  t2.medium
                </option>
              </select>

              <select
                name="region"
                onChange={
                  handleChange
                }
                className={`w-full border rounded-xl px-4 py-3 ${input}`}
              >
                {REGIONS.map(
                  (
                    r
                  ) => (
                    <option
                      key={
                        r
                      }
                    >
                      {r}
                    </option>
                  )
                )}
              </select>

              <div className="grid grid-cols-2 gap-4">
                <button
                  onClick={
                    createCluster
                  }
                  className="py-3 rounded-xl bg-blue-600 text-white hover:scale-105 transition"
                >
                  Single Region
                </button>

                <button
                  onClick={
                    createMultiRegion
                  }
                  className="py-3 rounded-xl bg-purple-600 text-white hover:scale-105 transition"
                >
                  Multi Region
                </button>
              </div>
            </div>

            {/* REGIONS */}
            <div
              className={`rounded-2xl border p-6 ${card}`}
            >
              <h3 className="text-xl font-semibold mb-4">
                Select Regions
              </h3>

              <div className="grid grid-cols-2 gap-3">
                {REGIONS.map(
                  (
                    region
                  ) => (
                    <label
                      key={
                        region
                      }
                      className="border rounded-xl p-4 flex gap-2"
                    >
                      <input
                        type="checkbox"
                        checked={selectedRegions.includes(
                          region
                        )}
                        onChange={() =>
                          toggleRegion(
                            region
                          )
                        }
                      />

                      {
                        region
                      }
                    </label>
                  )
                )}
              </div>
            </div>
          </div>

          {/* PRIMARY / STANDBY */}
          <div className="grid md:grid-cols-2 gap-4">
            <Card
              title="Primary Cluster"
              value={
                form.region
              }
              status={
                loading
                  ? "Provisioning"
                  : jobStatus ===
                    "completed"
                  ? "Ready"
                  : "Idle"
              }
              card={
                card
              }
            />

            <Card
              title="Standby Cluster"
              value={
                selectedRegions[1] ||
                "us-east-2"
              }
              status="Standby"
              card={
                card
              }
            />
          </div>

          {/* PROGRESS */}
          <div
            className={`rounded-2xl border p-6 ${card}`}
          >
            <h3 className="font-semibold text-lg">
              Deployment Status
            </h3>

            <div className="mt-4 h-3 bg-slate-300 rounded-full overflow-hidden">
              <div
                className="h-full bg-blue-600 transition-all duration-700"
                style={{
                  width: `${progress}%`,
                }}
              />
            </div>

            <p className="mt-2 text-sm opacity-70">
              {loading
                ? "Provisioning in progress..."
                : jobStatus ===
                  "completed"
                ? "Cluster Ready"
                : "Idle"}
            </p>
          </div>

          {/* ACTIONS */}
          <div className="grid md:grid-cols-3 gap-4">
            <button
              onClick={
                getStatus
              }
              className="py-3 rounded-xl bg-indigo-600 text-white"
            >
              Cluster Status
            </button>

            <button
              onClick={
                downloadConfig
              }
              className="py-3 rounded-xl bg-green-600 text-white"
            >
              Download Config
            </button>

            <button
              onClick={
                deleteCluster
              }
              className="py-3 rounded-xl bg-red-600 text-white"
            >
              Delete Cluster
            </button>
          </div>

          {/* LOGS */}
          <div
            className={`rounded-2xl border p-6 ${card}`}
          >
            <h3 className="text-xl font-semibold mb-4">
              📜 Live Logs
            </h3>

            <pre
              ref={logRef}
              className="bg-black text-green-400 rounded-xl p-4 h-96 overflow-auto text-sm whitespace-pre-wrap"
            >
              {logs ||
                "Waiting for deployment..."}
            </pre>
          </div>

          {/* STATUS */}
          <div
            className={`rounded-2xl border p-6 ${card}`}
          >
            <h3 className="text-xl font-semibold mb-4">
              📊 Cluster Status
            </h3>

            <textarea
              rows="12"
              readOnly
              value={
                status
              }
              className={`w-full border rounded-xl p-4 ${input}`}
            />
          </div>
        </main>
      </div>
    </div>
  );
}

// =====================================================
// REUSABLE COMPONENTS
// =====================================================
function Metric({
  title,
  value,
  color,
  card,
}) {
  return (
    <div
      className={`rounded-2xl border p-5 ${card}`}
    >
      <div className="text-sm opacity-70">
        {title}
      </div>

      <div className="text-3xl font-bold mt-2">
        {value}
      </div>

      <div
        className={`h-1 rounded-full mt-4 ${color}`}
      />
    </div>
  );
}

function Card({
  title,
  value,
  status,
  card,
}) {
  return (
    <div
      className={`rounded-2xl border p-6 ${card}`}
    >
      <h3 className="text-xl font-semibold">
        {title}
      </h3>

      <p className="mt-3 opacity-80">
        Region: {value}
      </p>

      <p className="mt-1">
        Status: {status}
      </p>
    </div>
  );
}
