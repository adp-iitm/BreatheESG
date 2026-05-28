import { useEffect, useState } from "react";

import client from "../api/client";
import ReviewModal from "../components/ReviewModal";
import StatCard from "../components/StatCard";

export default function DashboardPage() {
  const [stats, setStats] = useState({});
  const [activities, setActivities] = useState([]);
  const [selected, setSelected] = useState(null);

  const load = async () => {
    const [dashboardRes, activitiesRes] = await Promise.all([client.get("/dashboard/"), client.get("/activities/")]);
    setStats(dashboardRes.data);
    setActivities(activitiesRes.data);
  };

  useEffect(() => {
    load();
  }, []);

  const act = async (id, action) => {
    await client.post(`/activities/${id}/${action}/`);
    setSelected(null);
    load();
  };

  return (
    <section className="space-y-6">
      <div className="grid gap-4 md:grid-cols-4">
        <StatCard label="Total Ingested" value={stats.total_rows || 0} />
        <StatCard label="Failed" value={stats.failed_rows || 0} />
        <StatCard label="Flagged" value={stats.flagged_rows || 0} />
        <StatCard label="Approved" value={stats.approved_rows || 0} />
      </div>
      <div className="overflow-auto rounded-lg border bg-white shadow-sm">
        <table className="min-w-full text-sm">
          <thead className="bg-slate-100 text-left">
            <tr>
              <th className="p-3">Source</th>
              <th className="p-3">Scope</th>
              <th className="p-3">Quantity</th>
              <th className="p-3">Status</th>
              <th className="p-3">Suspicious</th>
            </tr>
          </thead>
          <tbody>
            {activities.map((a) => (
              <tr className="cursor-pointer border-t hover:bg-slate-50" key={a.id} onClick={() => setSelected(a)}>
                <td className="p-3">{a.source_type}</td>
                <td className="p-3">{a.scope}</td>
                <td className="p-3">
                  {a.normalized_quantity} {a.normalized_unit}
                </td>
                <td className="p-3">{a.review_status}</td>
                <td className="p-3">{a.validation_issues?.length ? "Yes" : "No"}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
      <ReviewModal
        activity={selected}
        onClose={() => setSelected(null)}
        onApprove={(id) => act(id, "approve")}
        onReject={(id) => act(id, "reject")}
      />
    </section>
  );
}
