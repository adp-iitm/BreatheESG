export default function ReviewModal({ activity, onClose, onApprove, onReject }) {
  if (!activity) return null;
  return (
    <div className="fixed inset-0 z-10 flex items-center justify-center bg-black/40 p-4">
      <div className="max-h-[90vh] w-full max-w-3xl overflow-auto rounded-lg bg-white p-6">
        <h3 className="text-lg font-semibold">Review Activity #{activity.id}</h3>
        <div className="mt-4 grid gap-4 md:grid-cols-2">
          <div>
            <p className="font-medium">Original Raw Row</p>
            <pre className="mt-2 overflow-auto rounded bg-slate-100 p-3 text-xs">{JSON.stringify(activity.raw_row, null, 2)}</pre>
          </div>
          <div>
            <p className="font-medium">Normalized Row</p>
            <pre className="mt-2 overflow-auto rounded bg-slate-100 p-3 text-xs">{JSON.stringify(activity, null, 2)}</pre>
          </div>
        </div>
        <div className="mt-4">
          <p className="font-medium">Validation Issues</p>
          <ul className="mt-2 list-disc pl-5 text-sm">
            {(activity.validation_issues || []).map((issue) => (
              <li key={issue}>{issue}</li>
            ))}
            {(!activity.validation_issues || activity.validation_issues.length === 0) && <li>No issues</li>}
          </ul>
        </div>
        <div className="mt-6 flex gap-2">
          <button className="rounded bg-emerald-600 px-4 py-2 text-white" onClick={() => onApprove(activity.id)}>
            Approve
          </button>
          <button className="rounded bg-rose-600 px-4 py-2 text-white" onClick={() => onReject(activity.id)}>
            Reject
          </button>
          <button className="rounded border px-4 py-2" onClick={onClose}>
            Close
          </button>
        </div>
      </div>
    </div>
  );
}
