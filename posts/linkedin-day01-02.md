# LinkedIn Post — RAG Learning (Day 1-2)

---

I'm a frontend developer. This week I started learning RAG (Retrieval-Augmented Generation) from scratch — and honestly, it clicked faster than I expected. Here's why. 👇

As a React/Angular dev, I already think in a familiar loop every day:

**user action → fetch() → render()**

Turns out, RAG is almost the same story:

**user query → retrieve relevant docs → LLM generates the answer**

The "server" is just a vector database, and the "render engine" is an LLM. Same mental model, new tools.

Two days in, three things genuinely surprised me:

🔹 **1. LLMs don't know your data — and that's the whole point of RAG.**
An LLM is like a brilliant developer locked in a room with no internet. It can't answer questions about *your* company's docs. Retraining it is insanely expensive (think: rebuilding + redeploying your entire app for every tiny change). RAG skips all that — you just hand the model the right document at runtime.

🔹 **2. Keyword search quietly fails.**
Search for "refund" in a doc that says "paisa wapas" (money back) and plain keyword matching finds nothing — zero shared words. This is where **embeddings** come in: they convert text into a list of numbers (a vector) that captures *meaning*, not just words. Similar meanings end up close together in space.

🔹 **3. I built cosine similarity from scratch — and it stopped being magic.**
Instead of trusting a library, I computed the similarity score by hand (dot product ÷ magnitudes). My scratch version matched the library's output exactly. That "aha" moment — when a black box becomes just arithmetic — is the best part of learning.

The most valuable lesson wasn't when things worked. It was when my retrieval got it *wrong* — a weak model ranked the wrong document first because it fixated on a surface word instead of the meaning. Seeing the failure taught me more than any success would.

My approach: **build the concept from scratch first, then use the real tools.** Every RAG idea mapped to something I already knew from frontend — embeddings ≈ serialization, retrieval ≈ fetch, vector DB ≈ a cache layer.

23 days to go. Building in public, one small concept at a time.

Code + notes + diagrams here 👉 github.com/ranavj/rag-mastery

If you're a frontend/web dev curious about GenAI: you already know more than you think. Start building.

#RAG #GenAI #MachineLearning #LLM #WebDevelopment #LearningInPublic #AI #React #BuildInPublic
