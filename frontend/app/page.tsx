"use client";

import { useState } from "react";

interface Message {
  role: "user" | "assistant";
  content: string;
}

interface Recipe {
  title: string;
  ingredients: string[];
  instructions: string;
  score: number;
}

export default function Home() {
  const [query, setQuery] = useState("");
  const [sources, setSources] = useState<Recipe[]>([]);
  const [history, setHistory] = useState<Message[]>([]);
  const [loading, setLoading] = useState(false);
  const [streaming, setStreaming] = useState(false);

  const handleAsk = async () => {
    if (!query.trim() || loading || streaming) return;

    const userMessage = query;
    setQuery("");
    setLoading(true);
    setSources([]);

    // Ajouter le message user dans l'historique immédiatement
    setHistory(prev => [...prev, { role: "user", content: userMessage }]);

    try {
      // 1. Récupérer les sources
      const sourcesRes = await fetch("http://localhost:8000/search", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ question: userMessage }),
      });
      const sourcesData = await sourcesRes.json();
      setSources(sourcesData);
      setLoading(false);

      // 2. Streamer la réponse avec l'historique
      setStreaming(true);
      let fullAnswer = "";

      // Ajouter un message assistant vide pour le streaming
      setHistory(prev => [...prev, { role: "assistant", content: "" }]);

      const response = await fetch("http://localhost:8000/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          question: userMessage,
          history: history,   // ← historique des échanges précédents
        }),
      });

      if (!response.body) throw new Error("Stream non supporté");

      const reader = response.body.getReader();
      const decoder = new TextDecoder();

      while (true) {
        const { done, value } = await reader.read();
        if (done) break;
        const chunk = decoder.decode(value);
        fullAnswer += chunk;

        // Mettre à jour le dernier message assistant en temps réel
        setHistory(prev => [
          ...prev.slice(0, -1),
          { role: "assistant", content: fullAnswer }
        ]);
      }

    } catch (error) {
      console.error("Erreur:", error);
      setLoading(false);
    } finally {
      setStreaming(false);
    }
  };

  const clearHistory = () => {
    setHistory([]);
    setSources([]);
  };

  return (
    <main className="min-h-screen bg-orange-50 p-6 md:p-12 text-gray-900">
      <div className="max-w-3xl mx-auto">

        <header className="text-center mb-10">
          <h1 className="text-4xl font-extrabold text-orange-800 mb-2">Cuisine RAG</h1>
          <p className="text-orange-600">Assistant Culinaire Intelligent</p>
        </header>

        {/* Historique de conversation */}
        {history.length > 0 && (
          <div className="bg-white rounded-2xl shadow-sm border border-orange-100 mb-6 overflow-hidden">
            <div className="flex justify-between items-center p-4 border-b border-orange-100">
              <h3 className="font-bold text-orange-800">Conversation</h3>
              <button
                onClick={clearHistory}
                className="text-xs text-gray-400 hover:text-red-400 transition-colors"
              >
                Effacer
              </button>
            </div>
            <div className="p-4 space-y-4 max-h-96 overflow-y-auto">
              {history.map((msg, i) => (
                <div
                  key={i}
                  className={`flex ${msg.role === "user" ? "justify-end" : "justify-start"}`}
                >
                  <div className={`max-w-[80%] p-3 rounded-2xl text-sm whitespace-pre-wrap ${
                    msg.role === "user"
                      ? "bg-orange-600 text-white rounded-tr-none"
                      : "bg-orange-50 text-gray-800 border border-orange-100 rounded-tl-none"
                  }`}>
                    {msg.role === "assistant" && (
                      <span className="text-lg mr-1">👨‍🍳</span>
                    )}
                    {msg.content}
                    {/* Curseur clignotant sur le dernier message assistant en streaming */}
                    {streaming && i === history.length - 1 && msg.role === "assistant" && (
                      <span className="inline-block w-2 h-4 bg-orange-400 animate-pulse ml-1" />
                    )}
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Input */}
        <div className="bg-white p-4 rounded-2xl shadow-lg flex gap-2 border-2 border-orange-100 mb-8">
          <input
            type="text"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            onKeyDown={(e) => e.key === "Enter" && handleAsk()}
            placeholder="Quelle recette cherchez-vous ?"
            className="flex-grow p-3 text-lg rounded-lg outline-none text-gray-900 placeholder-gray-400 bg-transparent"
            disabled={loading || streaming}
          />
          <button
            onClick={handleAsk}
            className="bg-orange-600 hover:bg-orange-700 text-white font-bold px-8 py-3 rounded-lg transition-colors disabled:opacity-50"
            disabled={loading || streaming}
          >
            {loading ? "Recherche..." : streaming ? "Réflexion..." : "Demander"}
          </button>
        </div>

        {/* Sources */}
        {sources.length > 0 && (
          <div className="mt-4">
            <h3 className="text-xl font-bold text-orange-900 mb-6">
              Sources et Recettes Trouvées
            </h3>
            <div className="space-y-6">
              {sources.map((r, i) => (
                <div key={i} className="bg-white p-6 rounded-2xl shadow-sm border border-orange-100">
                  <h2 className="text-2xl font-bold text-orange-900 mb-2">{r.title}</h2>
                  <div className="space-y-3">
                    <p className="text-gray-700">
                      <strong className="text-orange-700">Ingrédients:</strong>{" "}
                      {Array.isArray(r.ingredients) ? r.ingredients.join(", ") : r.ingredients}
                    </p>
                    <p className="text-gray-700">
                      <strong className="text-orange-700">Instructions:</strong> {r.instructions}
                    </p>
                  </div>
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

        {!loading && !streaming && history.length === 0 && (
          <div className="text-center text-gray-400 mt-12 py-12 border-2 border-dashed border-orange-100 rounded-3xl">
            <p className="text-lg">Posez une question sur une recette ou des ingrédients !</p>
          </div>
        )}

      </div>
    </main>
  );
}