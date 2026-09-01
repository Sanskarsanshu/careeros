export default function Dashboard() {
  return (
    <div className="p-8">
      <h2 className="text-2xl font-semibold mb-4">Dashboard (Phase 1 Foundation)</h2>
      <p className="text-gray-600 mb-8">
        Welcome to CareerOS. The backend, database, and auth foundation are established.
        Product features (Resume Builder, ATS, RAG) will be built in subsequent phases.
      </p>
      
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="border p-6 rounded-lg shadow-sm">
          <h3 className="font-bold text-lg mb-2">Resume Builder</h3>
          <p className="text-sm text-gray-500">Coming in Phase 2</p>
        </div>
        <div className="border p-6 rounded-lg shadow-sm">
          <h3 className="font-bold text-lg mb-2">ATS Engine</h3>
          <p className="text-sm text-gray-500">Coming in Phase 4</p>
        </div>
        <div className="border p-6 rounded-lg shadow-sm">
          <h3 className="font-bold text-lg mb-2">AI Assistant (RAG)</h3>
          <p className="text-sm text-gray-500">Coming in Phase 5</p>
        </div>
      </div>
    </div>
  );
}
