import os
import re
import csv
import math

# ==============================
# CONFIGURATION
# ==============================
DATASET_FOLDER = "mini"   # folder containing .txt files
MAX_ITER = 20             # number of iterations
EPSILON = 1e-6            # convergence tolerance
TOP_K = 10                # how many top pages to display

# ==============================
# STEP 1: BUILD GRAPH STRUCTURE
# ==============================

out_links = {}  # source -> list of destinations
in_links = {}   # destination -> list of sources
pages = set()

for root, dirs, files in os.walk(DATASET_FOLDER):
    for file in files:
        if file.endswith(".txt"):
            with open(os.path.join(root, file), "r", encoding="utf-8") as f:
                text = f.read()
                # Extract <title>...</title>
                y = text.split("</title>")
                z = y[0].split("<title>")
                source = z[1].strip() if len(z) > 1 else None

                # Extract [[...]] links
                destinations = re.findall(r"\[\[(.*?)\]\]", text)
                destinations = list(set([d.strip() for d in destinations if d.strip()]))

                if source:
                    pages.add(source)
                    out_links[source] = destinations
                    for d in destinations:
                        pages.add(d)
                        in_links.setdefault(d, []).append(source)

# Ensure all pages appear in both dicts
for p in pages:
    out_links.setdefault(p, [])
    in_links.setdefault(p, [])

print(f"✅ Total pages found (N): {len(pages)}")

# ==============================
# STEP 2: INITIALIZE SCORES
# ==============================
authority = {p: 1.0 for p in pages}
hub = {p: 1.0 for p in pages}

print("✅ Initialized authority and hub scores to 1.0")

# ==============================
# STEP 3: ITERATIVE UPDATES
# ==============================
for iteration in range(MAX_ITER):
    new_authority = {}
    new_hub = {}

    # --- Update authority scores ---
    for p in pages:
        new_authority[p] = sum(hub[q] for q in in_links[p])

    # --- Update hub scores ---
    for p in pages:
        new_hub[p] = sum(new_authority[q] for q in out_links[p])

    # --- Normalize ---
    norm_a = math.sqrt(sum(a*a for a in new_authority.values()))
    norm_h = math.sqrt(sum(h*h for h in new_hub.values()))
    for p in pages:
        new_authority[p] = new_authority[p] / norm_a if norm_a > 0 else 0
        new_hub[p] = new_hub[p] / norm_h if norm_h > 0 else 0

    # --- Check convergence ---
    diff = sum(abs(new_authority[p] - authority[p]) + abs(new_hub[p] - hub[p]) for p in pages)
    print(f"Iteration {iteration+1}: Δ = {diff:.8f}")

    authority, hub = new_authority, new_hub
    if diff < EPSILON:
        print("✅ Converged!")
        break

# ==============================
# STEP 4: PRINT + SAVE RESULTS
# ==============================
sorted_authorities = sorted(authority.items(), key=lambda x: x[1], reverse=True)
sorted_hubs = sorted(hub.items(), key=lambda x: x[1], reverse=True)

print(f"\n📊 Top {TOP_K} Authorities:")
for page, score in sorted_authorities[:TOP_K]:
    print(f"{page:30s} → {score:.6f}")

print(f"\n🔗 Top {TOP_K} Hubs:")
for page, score in sorted_hubs[:TOP_K]:
    print(f"{page:30s} → {score:.6f}")

# ---- SAVE TO CSV ----
with open("hits_results.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["Page", "Authority", "Hub"])
    for p in pages:
        writer.writerow([p, authority[p], hub[p]])

print("\n✅ All results saved to hits_results.csv")