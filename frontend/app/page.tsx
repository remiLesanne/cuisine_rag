"use client";

import { useState } from "react";

export default function Home() {
  const [query, setQuery] = useState("");
  const [answer, setAnswer] = useState("");
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(false);

  const handleAsk = async () => {
    if (!query.trim()) return;
    setLoading(true);
    setAnswer("");
    setResults([]);
    try {
      const response = await fetch("http://localhost:8000/ask", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ 
          question: query
        }),
      });
      const data = await response.json();
      setAnswer(data.answer);
      setResults(data.source);
    } catch (error) {
      console.error("Erreur:", error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <main className="min-h-screen bg-orange-50 p-6 md:p-12 text-gray-900">
      <div className="max-w-3xl mx-auto">
        <header className="text-center mb-10">
          <h1 className="text-4xl font-extrabold text-orange-800 mb-2">Cuisine RAG</h1>
          <p className="text-orange-600">Assistant Culinaire Intelligent</p>
        </header>

        <div className="bg-white p-4 rounded-2xl shadow-lg flex gap-2 border-2 border-orange-100 mb-8">
          <input
            type="text"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            onKeyDown={(e) => e.key === "Enter" && handleAsk()}
            placeholder="Quelle recette cherchez-vous ?"
            className="flex-grow p-3 text-lg rounded-lg outline-none text-gray-900 placeholder-gray-400 bg-transparent"
          />
          <button 
            onClick={handleAsk} 
            className="bg-orange-600 hover:bg-orange-700 text-white font-bold px-8 py-3 rounded-lg transition-colors"
            disabled={loading}
          >
            {loading ? "Réflexion..." : "Demander"}
          </button>
        </div>

        {/* Réponse de l'IA */}
        {answer && (
          <div className="bg-orange-100 p-8 rounded-2xl shadow-sm border border-orange-200 mb-8 animate-in fade-in slide-in-from-bottom-4 duration-500">
            <h3 className="text-lg font-bold text-orange-800 mb-3 flex items-center gap-2">
              <span className="text-2xl">👨‍🍳</span> Réponse du Chef
            </h3>
            <div className="prose prose-orange text-gray-800 whitespace-pre-wrap leading-relaxed">
              {answer}
            </div>
          </div>
        )}

        {/* Sources / Résultats de recherche */}
        {results.length > 0 && (
          <div className="mt-12">
            <h3 className="text-xl font-bold text-orange-900 mb-6 flex items-center gap-2">
               Sources et Recettes Trouvées
            </h3>
            <div className="space-y-6">
              {results.map((r: any, i) => (
                <div key={i} className="bg-white p-6 rounded-2xl shadow-sm border border-orange-100">
                  <h2 className="text-2xl font-bold text-orange-900 mb-2">{r.title}</h2>
                  
                  <div className="space-y-3">
                    <p className="text-gray-700">
                      <strong className="text-orange-700">Ingrédients:</strong> {Array.isArray(r.ingredients) ? r.ingredients.join(", ") : r.ingredients}
                    </p>
                    <p className="text-gray-700">
                      <strong className="text-orange-700">Instructions:</strong> {r.instructions}
                    </p>
                  </div>

                  {/* Bloc Débogage */}
                  <details className="mt-4">
                    <summary className="text-xs font-bold text-gray-400 cursor-pointer uppercase tracking-wider mb-2 hover:text-orange-400 transition-colors">
                      Données Brutes (Débogage)
                    </summary>
                    <pre className="bg-gray-900 text-green-400 p-4 rounded-lg text-xs overflow-x-auto mt-2">
                      {JSON.stringify(r, null, 2)}
                    </pre>
                  </details>
                </div>
              ))}
            </div>
          </div>
        )}

        {!loading && !answer && results.length === 0 && (
          <div className="text-center text-gray-400 mt-12 py-12 border-2 border-dashed border-orange-100 rounded-3xl">
            <p className="text-lg">Posez une question sur une recette ou des ingrédients !</p>
          </div>
        )}
      </div>
    </main>
  );
}
