import { Link, Route, Routes } from "react-router-dom";

import DashboardPage from "./pages/DashboardPage";
import UploadPage from "./pages/UploadPage";

export default function App() {
  return (
    <div className="min-h-screen">
      <header className="border-b bg-white">
        <nav className="mx-auto flex max-w-6xl gap-4 p-4 text-sm font-medium">
          <Link to="/" className="hover:text-blue-600">
            Dashboard
          </Link>
          <Link to="/upload" className="hover:text-blue-600">
            Upload
          </Link>
        </nav>
      </header>
      <main className="mx-auto max-w-6xl p-4">
        <Routes>
          <Route path="/" element={<DashboardPage />} />
          <Route path="/upload" element={<UploadPage />} />
        </Routes>
      </main>
    </div>
  );
}
