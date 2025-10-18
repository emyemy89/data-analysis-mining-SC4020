import os
import re
import csv

# ==============================
# CONFIGURATION
# ==============================
DATASET_FOLDER = "mini"   # folder containing .txt files
BETA = 0.8                # damping factor
MAX_ITER = 20             # number of iterations
EPSILON = 1e-6            # convergence tolerance
TOP_K = 10                # how many top pages to display

# ==============================
# STEP 1: BUILD LINK MATRIX (M)
# ==============================

M_lines = []
pages = set()

for root, dirs, files in os.walk(DATASET_FOLDER):
    for file in files:
        if file.endswith(".txt"):
            with open(os.path.join(root, file), "r", encoding="utf-8") as f:
                text = f.read()
                # Extract source title
                y = text.split("</title>")
                z = y[0].split("<title>")
                source = z[1].strip() if len(z) > 1 else None

                # Find [[...]] links
                destinations = re.findall(r"\[\[(.*?)\]\]", text)
                destinations = list(set([d.strip() for d in destinations if d.strip()]))

                if source and destinations:
                    M_lines.append((source, len(destinations), destinations))
                    pages.add(source)
                    for d in destinations:
                        pages.add(d)

# Save M.txt for inspection (optional)
with open("M.txt", "w", encoding="utf-8") as f:
    for src, deg, dests in M_lines:
        f.write(f"{src}||#{deg}||#{dests}\n")

N = len(pages)
print(f"✅ Total pages found (N): {N}")

# ==============================
# STEP 2: INITIALIZE PAGERANKS
# ==============================

r_old = {page: 1 / N for page in pages}
print("✅ Initial PageRank values set to 1/N")

# ==============================
# STEP 3: ITERATE PAGE RANK
# ==============================

for iteration in range(MAX_ITER):
    r_new = {page: (1 - BETA) / N for page in pages}

    # Read from M.txt to propagate ranks
    with open("M.txt", "r", encoding="utf-8") as f:
        for line in f:
            src, deg, dests = line.strip().split("||#")
            deg = int(deg)
            dests = eval(dests)
            share = BETA * (r_old[src] / deg)
            for d in dests:
                if d in r_new:
                    r_new[d] += share
                else:
                    r_new[d] = (1 - BETA) / N + share

    # Check convergence
    diff = sum(abs(r_new[p] - r_old[p]) for p in pages)
    print(f"Iteration {iteration+1}: Δ = {diff:.8f}")
    if diff < EPSILON:
        print("✅ Converged!")
        break
    r_old = r_new

# ==============================
# STEP 4: PRINT + SAVE RESULTS
# ==============================

sorted_ranks = sorted(r_old.items(), key=lambda x: x[1], reverse=True)

# ---- PRINT ONLY TOP K ----
print(f"\n📊 Top {TOP_K} Most Important Pages:")
for page, rank in sorted_ranks[:TOP_K]:
    print(f"{page:30s} → {rank:.6f}")

# ---- SAVE ALL RESULTS TO CSV ----
csv_file = "pagerank_results.csv"
with open(csv_file, "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["Page", "PageRank"])
    writer.writerows(sorted_ranks)

print(f"\n✅ All results saved to {csv_file}")
