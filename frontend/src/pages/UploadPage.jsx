import { useState } from "react";

import client from "../api/client";

export default function UploadPage() {
  const [file, setFile] = useState(null);
  const [sourceType, setSourceType] = useState("SAP");
  const [companyId, setCompanyId] = useState("1");
  const [message, setMessage] = useState("");

  const onSubmit = async (e) => {
    e.preventDefault();
    const form = new FormData();
    form.append("file", file);
    form.append("source_type", sourceType);
    form.append("company_id", companyId);
    try {
      await client.post("/upload/", form);
      setMessage("Upload completed and normalization started.");
    } catch (err) {
      setMessage(err.response?.data?.detail || "Upload failed");
    }
  };

  return (
    <section className="rounded-lg border bg-white p-6 shadow-sm">
      <h2 className="text-xl font-semibold">Upload Source File</h2>
      <form className="mt-4 grid gap-4 md:max-w-lg" onSubmit={onSubmit}>
        <select className="rounded border p-2" value={sourceType} onChange={(e) => setSourceType(e.target.value)}>
          <option value="SAP">SAP</option>
          <option value="UTILITY">UTILITY</option>
          <option value="TRAVEL">TRAVEL</option>
        </select>
        <input className="rounded border p-2" value={companyId} onChange={(e) => setCompanyId(e.target.value)} placeholder="Company ID" />
        <input className="rounded border p-2" type="file" onChange={(e) => setFile(e.target.files?.[0])} required />
        <button className="rounded bg-blue-600 px-4 py-2 text-white" type="submit">
          Upload CSV
        </button>
      </form>
      {message && <p className="mt-4 text-sm">{message}</p>}
    </section>
  );
}
